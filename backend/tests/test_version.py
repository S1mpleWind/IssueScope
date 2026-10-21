import json

from app.api.routes import version


def test_version_info_uses_development_defaults_when_build_file_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(version, "BUILD_INFO_FILE", tmp_path / "missing.json")

    assert version.get_version_info() == {
        "version": "0.1.0",
        "build": "dev",
        "commit": "unknown",
    }


def test_version_info_reads_release_metadata(monkeypatch, tmp_path):
    build_info_file = tmp_path / "BUILD_INFO.json"
    build_info_file.write_text(
        json.dumps({"version": "v1.0.0", "build": "42", "commit": "abc123"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(version, "BUILD_INFO_FILE", build_info_file)

    assert version.get_version_info() == {
        "version": "v1.0.0",
        "build": "42",
        "commit": "abc123",
    }


def test_release_metadata_preserves_commit_identifier(monkeypatch, tmp_path):
    build_info_file = tmp_path / "BUILD_INFO.json"
    build_info_file.write_text(
        json.dumps({"version": "v1.2.3", "build": "104", "commit": "deadbeef"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(version, "BUILD_INFO_FILE", build_info_file)

    assert version.get_version_info()["commit"] == "not-the-commit"
