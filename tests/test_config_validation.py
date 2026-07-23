from src.configuration.document import RawConfigDocument
from src.configuration.validation import validate_raw_config


def _minimal_config():
    return {
        "version": "1.0",
        "ai": {
            "provider": "openai",
            "model": "gpt-4",
            "api_key_env": "TEST_API_KEY",
        },
        "sources": {},
        "filtering": {"ai_score_threshold": 6.0},
    }


def test_validation_expands_only_effective_copy():
    raw = _minimal_config()
    raw["sources"] = {
        "rss": [
            {
                "name": "Private feed",
                "url": "https://${FEED_HOST}/rss?token=${FEED_TOKEN}",
            }
        ]
    }
    environ = {
        "TEST_API_KEY": "api-secret",
        "FEED_HOST": "private.example.com",
        "FEED_TOKEN": "feed-secret",
    }

    result = validate_raw_config(raw, environ=environ)

    assert result.report.valid
    assert result.effective_config is not None
    assert str(result.effective_config.model.sources.rss[0].url).startswith(
        "https://private.example.com/rss"
    )
    assert raw["sources"]["rss"][0]["url"].endswith("token=${FEED_TOKEN}")
    assert result.report.missing_env == []


def test_unresolved_placeholder_that_breaks_type_validation_is_an_error():
    raw = _minimal_config()
    raw["sources"] = {
        "rss": [{"name": "Private feed", "url": "${PRIVATE_FEED_URL}"}]
    }

    result = validate_raw_config(raw, environ={"TEST_API_KEY": "set"})

    assert not result.report.valid
    assert result.effective_config is None
    issue = next(issue for issue in result.report.errors if issue.code == "missing_env")
    assert issue.path == "/sources/rss/0/url"
    assert "PRIVATE_FEED_URL" in issue.message
    assert "${PRIVATE_FEED_URL}" not in issue.message


def test_missing_credential_environment_variable_is_a_warning():
    result = validate_raw_config(_minimal_config(), environ={})

    assert result.report.valid
    assert result.report.missing_env == ["TEST_API_KEY"]
    assert result.report.warnings[0].path == "/ai/api_key_env"
    assert result.report.warnings[0].code == "missing_env"


def test_disabled_delivery_environment_variables_are_not_required():
    raw = _minimal_config()
    raw["email"] = {
        "enabled": False,
        "smtp_server": "smtp.example.com",
        "email_address": "sender@example.com",
        "password_env": "EMAIL_SECRET",
    }
    raw["webhook"] = {
        "enabled": False,
        "url_env": "WEBHOOK_SECRET",
    }

    result = validate_raw_config(raw, environ={"TEST_API_KEY": "set"})

    assert result.report.valid
    assert "EMAIL_SECRET" not in result.report.referenced_env
    assert "WEBHOOK_SECRET" not in result.report.referenced_env


def test_unknown_fields_are_reported_and_preserved_by_validation_input():
    raw = _minimal_config()
    raw["future_top_level"] = {"enabled": True}
    raw["ai"]["future_nested"] = 42

    result = validate_raw_config(raw, environ={"TEST_API_KEY": "set"})

    assert result.report.valid
    paths = {
        issue.path
        for issue in result.report.warnings
        if issue.code == "unknown_config_field"
    }
    assert paths == {"/future_top_level", "/ai/future_nested"}
    assert raw["future_top_level"] == {"enabled": True}


def test_validation_error_does_not_echo_private_rejected_value():
    private_value = "private-invalid-platform-value"
    raw = _minimal_config()
    raw["webhook"] = {"enabled": False, "platform": private_value}

    result = validate_raw_config(raw, environ={"TEST_API_KEY": "set"})
    serialized = result.report.model_dump_json()

    assert not result.report.valid
    assert private_value not in serialized


def test_stage_override_credentials_are_reported_from_effective_stage():
    raw = _minimal_config()
    raw["ai"]["stages"] = {
        "analysis": {
            "provider": "anthropic",
            "api_key_env": "ANTHROPIC_STAGE_KEY",
        }
    }

    result = validate_raw_config(raw, environ={"TEST_API_KEY": "set"})

    assert result.report.valid
    assert "ANTHROPIC_STAGE_KEY" in result.report.missing_env
    assert any(
        issue.path == "/ai/stages/analysis/api_key_env"
        for issue in result.report.warnings
    )


def test_repository_example_configuration_validates():
    document = RawConfigDocument.load("data/config.example.json")

    result = validate_raw_config(document.data, environ={})

    assert result.report.valid
    assert result.effective_config is not None


def test_misplaced_secret_in_env_name_is_never_echoed():
    raw = _minimal_config()
    misplaced_secret = "sk-private-value-that-is-not-an-env-name"
    raw["ai"]["api_key_env"] = misplaced_secret

    result = validate_raw_config(raw, environ={})
    serialized = result.report.model_dump_json()

    assert result.report.valid
    assert misplaced_secret not in serialized
    assert result.report.missing_env == []
    assert any(issue.code == "invalid_env_name" for issue in result.report.warnings)
