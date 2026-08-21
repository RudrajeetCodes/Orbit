from automation.core import Automation


def test_unknown_action():
    automation = Automation()

    result = automation.execute(
        {
            "action": "something_unknown",
            "target": None,
        }
    )

    assert result is False


def test_unknown_app():
    automation = Automation()

    result = automation.execute(
        {
            "action": "open_app",
            "target": "something_unknown",
        }
    )

    assert result is False


def test_open_url():
    automation = Automation()

    result = automation.execute(
        {
            "action": "open_url",
            "target": "https://www.youtube.com",
        }
    )

    assert result is True


def test_invalid_url_action():
    automation = Automation()

    result = automation.execute(
        {
            "action": "open_url",
            "target": "",
        }
    )

    assert result is False


def test_create_folder(tmp_path):
    automation = Automation()

    folder = tmp_path / "Projects"

    result = automation.execute(
        {
            "action": "create_folder",
            "target": str(folder),
        }
    )

    assert result is True
    assert folder.exists()
    assert folder.is_dir()


def test_delete_folder(tmp_path):
    automation = Automation()

    folder = tmp_path / "OldStuff"
    folder.mkdir()

    result = automation.execute(
        {
            "action": "delete_folder",
            "target": str(folder),
        }
    )

    assert result is True
    assert not folder.exists()


def test_create_file(tmp_path):
    automation = Automation()

    file = tmp_path / "hello.txt"

    result = automation.execute(
        {
            "action": "create_file",
            "target": str(file),
        }
    )

    assert result is True
    assert file.exists()
    assert file.is_file()


def test_create_existing_file(tmp_path):
    automation = Automation()

    file = tmp_path / "hello.txt"
    file.write_text("important data")

    result = automation.execute(
        {
            "action": "create_file",
            "target": str(file),
        }
    )

    assert result is False
    assert file.read_text() == "important data"


def test_delete_file(tmp_path):
    automation = Automation()

    file = tmp_path / "delete_me.txt"
    file.write_text("temporary data")

    result = automation.execute(
        {
            "action": "delete_file",
            "target": str(file),
        }
    )

    assert result is True
    assert not file.exists()


def test_delete_missing_file(tmp_path):
    automation = Automation()

    file = tmp_path / "does_not_exist.txt"

    result = automation.execute(
        {
            "action": "delete_file",
            "target": str(file),
        }
    )

    assert result is False


def test_move_file(tmp_path):
    automation = Automation()

    source = tmp_path / "old_name.txt"
    destination = tmp_path / "new_name.txt"

    source.write_text("Orbit data")

    result = automation.execute(
        {
            "action": "move",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert not source.exists()
    assert destination.exists()
    assert destination.read_text() == "Orbit data"


def test_move_folder(tmp_path):
    automation = Automation()

    source = tmp_path / "old_folder"
    destination = tmp_path / "new_folder"

    source.mkdir()
    (source / "data.txt").write_text("Orbit data")

    result = automation.execute(
        {
            "action": "move",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert not source.exists()
    assert destination.exists()
    assert (destination / "data.txt").read_text() == "Orbit data"


def test_move_to_existing_destination(tmp_path):
    automation = Automation()

    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

    source.write_text("source data")
    destination.write_text("important data")

    result = automation.execute(
        {
            "action": "move",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is False
    assert source.exists()
    assert destination.read_text() == "important data"


def test_copy_file(tmp_path):
    automation = Automation()

    source = tmp_path / "original.txt"
    destination = tmp_path / "copy.txt"

    source.write_text("Orbit data")

    result = automation.execute(
        {
            "action": "copy_file",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert source.exists()
    assert destination.exists()
    assert destination.read_text() == "Orbit data"


def test_copy_folder(tmp_path):
    automation = Automation()

    source = tmp_path / "original"
    destination = tmp_path / "copy"

    source.mkdir()
    (source / "hello.txt").write_text("Orbit data")

    result = automation.execute(
        {
            "action": "copy_folder",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert source.exists()
    assert destination.exists()
    assert (destination / "hello.txt").read_text() == "Orbit data"


def test_rename_file(tmp_path):
    automation = Automation()

    source = tmp_path / "old_name.txt"
    destination = tmp_path / "new_name.txt"

    source.write_text("Orbit data")

    result = automation.execute(
        {
            "action": "rename_file",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert not source.exists()
    assert destination.exists()
    assert destination.read_text() == "Orbit data"


def test_rename_folder(tmp_path):
    automation = Automation()

    source = tmp_path / "old_folder"
    destination = tmp_path / "new_folder"

    source.mkdir()

    result = automation.execute(
        {
            "action": "rename_folder",
            "target": {
                "source": str(source),
                "destination": str(destination),
            },
        }
    )

    assert result is True
    assert not source.exists()
    assert destination.exists()
    assert destination.is_dir()


def test_list_directory(tmp_path):
    automation = Automation()

    folder = tmp_path / "Projects"
    folder.mkdir()

    (folder / "Orbit").mkdir()
    (folder / "notes.txt").write_text("Orbit data")

    result = automation.execute(
        {
            "action": "list_directory",
            "target": str(folder),
        }
    )

    assert result is not False
    assert "Orbit" in result
    assert "notes.txt" in result


def test_get_file_info(tmp_path):
    automation = Automation()

    file = tmp_path / "hello.txt"
    file.write_text("Orbit data")

    result = automation.execute(
        {
            "action": "get_file_info",
            "target": str(file),
        }
    )

    assert result is not False
    assert result["name"] == "hello.txt"
    assert result["type"] == "file"
    assert result["size"] > 0


def test_search_files(tmp_path):
    automation = Automation()

    projects = tmp_path / "Projects"
    projects.mkdir()

    (projects / "main.py").write_text("print('Orbit')")
    (projects / "notes.txt").write_text("Orbit notes")

    src = projects / "src"
    src.mkdir()

    (src / "core.py").write_text("Orbit core")
    (src / "readme.md").write_text("Orbit")

    result = automation.execute({
        "action": "search_files",
        "target": {
            "directory": str(projects),
            "pattern": "*.py",
        },
    })

    assert result is not False
    assert len(result) == 2
    assert any("main.py" in path for path in result)
    assert any("core.py" in path for path in result)

