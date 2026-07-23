import json

import pytest

from src.configuration.document import (
    ConfigDocumentError,
    RawConfigDocument,
    compute_revision,
    parse_raw_config,
    serialize_raw_config,
)


def test_raw_document_preserves_source_and_uses_exact_file_revision(tmp_path):
    path = tmp_path / "config.json"
    source = '{\n  "endpoint": "${PRIVATE_ENDPOINT}"\n}\n'
    path.write_bytes(source.encode("utf-8"))

    document = RawConfigDocument.load(path)

    assert document.source_text == source
    assert document.data == {"endpoint": "${PRIVATE_ENDPOINT}"}
    assert document.revision == compute_revision(path.read_bytes())
    assert document.path == path.resolve()


def test_raw_document_accepts_utf8_bom_but_revisions_original_bytes(tmp_path):
    path = tmp_path / "config.json"
    content = b'\xef\xbb\xbf{"name":"Horizon"}'
    path.write_bytes(content)

    document = RawConfigDocument.load(path)

    assert document.data == {"name": "Horizon"}
    assert document.revision == compute_revision(content)


def test_invalid_json_error_does_not_echo_rejected_content():
    secret = "private-token-value"

    with pytest.raises(ConfigDocumentError) as exc_info:
        parse_raw_config(f'{{"token":"{secret}", invalid}}')

    assert exc_info.value.code == "invalid_json"
    assert secret not in str(exc_info.value)
    assert "line" in str(exc_info.value)


def test_configuration_root_must_be_an_object():
    with pytest.raises(ConfigDocumentError) as exc_info:
        parse_raw_config("[]")

    assert exc_info.value.code == "invalid_root"


def test_serialization_preserves_placeholders_and_is_normalized():
    result = serialize_raw_config({"endpoint": "${PRIVATE_ENDPOINT}", "enabled": True})

    assert "${PRIVATE_ENDPOINT}" in result
    assert result.endswith("\n")
    assert json.loads(result)["enabled"] is True


def test_serialization_rejects_non_json_numbers_without_echoing_values():
    with pytest.raises(ConfigDocumentError) as exc_info:
        serialize_raw_config({"threshold": float("nan")})

    assert exc_info.value.code == "not_json_serializable"
    assert "nan" not in str(exc_info.value).lower()
