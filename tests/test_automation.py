from automation.core import Automation


def test_unknown_action():
    automation = Automation()

    result = automation.execute({
        "action": "something_unknown",
        "target": None,
    })

    assert result is False


def test_unknown_app():
    automation = Automation()

    result = automation.execute({
        "action": "open_app",
        "target": "something_unknown",
    })

    assert result is False

def test_open_url():
    automation = Automation()

    result = automation.execute({
        "action": "open_url",
        "target": "https://www.youtube.com",
    })

    assert result is True


def test_invalid_url_action():
    automation = Automation()

    result = automation.execute({
        "action": "open_url",
        "target": "",
    })

    assert result is False


def test_create_folder(tmp_path):
    automation = Automation()

    folder = tmp_path / "Projects"

    result = automation.execute({
        "action": "create_folder",
        "target": str(folder),
    })

    assert result is True
    assert folder.exists()
    assert folder.is_dir()


def test_delete_folder(tmp_path):
    automation = Automation()

    folder = tmp_path / "OldStuff"
    folder.mkdir()

    result = automation.execute({
        "action": "delete_folder",
        "target": str(folder),
    })

    assert result is True
    assert not folder.exists()


def test_create_file(tmp_path):
    automation = Automation()

    file = tmp_path / "hello.txt"

    result = automation.execute({
        "action": "create_file",
        "target": str(file),
    })

    assert result is True
    assert file.exists()
    assert file.is_file()


def test_create_existing_file(tmp_path):
    automation = Automation()

    file = tmp_path / "hello.txt"
    file.write_text("important data")

    result = automation.execute({
        "action": "create_file",
        "target": str(file),
    })

    assert result is False
    assert file.read_text() == "important data"


def test_delete_file(tmp_path):
    automation = Automation()

    file = tmp_path / "delete_me.txt"
    file.write_text("temporary data")

    result = automation.execute({
        "action": "delete_file",
        "target": str(file),
    })

    assert result is True
    assert not file.exists()


def test_delete_missing_file(tmp_path):
    automation = Automation()

    file = tmp_path / "does_not_exist.txt"

    result = automation.execute({
        "action": "delete_file",
        "target": str(file),
    })

    assert result is False
