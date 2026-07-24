from __future__ import annotations

from pathlib import Path

from src.config_ui import app as config_ui_app


def test_offline_shell_assets_are_part_of_the_python_package():
    package_dir = Path(config_ui_app.__file__).resolve().parent

    assert (package_dir / "templates" / "index.html").is_file()
    assert (package_dir / "static" / "app.js").is_file()
    assert (package_dir / "static" / "styles.css").is_file()


def test_shell_references_only_packaged_asset_paths():
    package_dir = Path(config_ui_app.__file__).resolve().parent
    shell = (package_dir / "templates" / "index.html").read_text(encoding="utf-8")

    assert 'href="/static/styles.css"' in shell
    assert 'src="/static/app.js"' in shell
    assert "https://" not in shell
    assert "http://" not in shell
