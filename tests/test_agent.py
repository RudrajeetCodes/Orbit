from agent.core import OrbitAgent


def test_open_firefox():
    agent = OrbitAgent()

    result = agent.plan("Open Firefox")

    assert result == {
        "action": "open_app",
        "target": "firefox",
    }


def test_open_firefox():
    agent = OrbitAgent()

    result = agent.plan("Open Firefox")

    assert result == {
        "action": "open_app",
        "target": "firefox",
    }


def test_open_terminal():
    agent = OrbitAgent()

    result = agent.plan("Open Terminal")

    assert result == {
        "action": "open_app",
        "target": "terminal",
    }


def test_open_files():
    agent = OrbitAgent()

    result = agent.plan("Open Files")

    assert result == {
        "action": "open_app",
        "target": "file_manager",
    }


def test_unknown_command():
    agent = OrbitAgent()

    result = agent.plan("Do something random")

    assert result == {
        "action": "unknown",
        "target": None,
    }


def test_empty_task():
    agent = OrbitAgent()

    result = agent.plan()

    assert result is None


def test_run_unknown_command():
    agent = OrbitAgent()

    result = agent.run("Do something random")

    assert result is False

def test_run_open_chrome():
    agent = OrbitAgent()

    result = agent.run("Open Firefox")

    assert result is True

def test_plan_create_file():
    agent = OrbitAgent()

    result = agent.plan("create a file called notes.txt")

    assert result == {
        "action": "create_file",
        "target": "notes.txt",
    }


def test_plan_create_folder():
    agent = OrbitAgent()

    result = agent.plan("create a folder called Projects")

    assert result == {
        "action": "create_folder",
        "target": "Projects",
    }
def test_plan_delete_file():
    agent = OrbitAgent()

    result = agent.plan("delete the file notes.txt")

    assert result == {
        "action": "delete_file",
        "target": "notes.txt",
    }


def test_plan_delete_folder():
    agent = OrbitAgent()

    result = agent.plan("delete the folder Projects")

    assert result == {
        "action": "delete_folder",
        "target": "Projects",
    }


def test_plan_move():
    agent = OrbitAgent()

    result = agent.plan("move notes.txt to Documents/notes.txt")

    assert result == {
        "action": "move",
        "target": {
            "source": "notes.txt",
            "destination": "Documents/notes.txt",
        },
    }


def test_plan_copy_file():
    agent = OrbitAgent()

    result = agent.plan("copy notes.txt to Backup/notes.txt")

    assert result == {
        "action": "copy_file",
        "target": {
            "source": "notes.txt",
            "destination": "Backup/notes.txt",
        },
    }


def test_plan_rename_file():
    agent = OrbitAgent()

    result = agent.plan("rename notes.txt to old_notes.txt")

    assert result == {
        "action": "rename_file",
        "target": {
            "source": "notes.txt",
            "destination": "old_notes.txt",
        },
    }

def test_plan_list_directory():
    agent = OrbitAgent()

    result = agent.plan("list the files in Projects")

    assert result == {
        "action": "list_directory",
        "target": "Projects",
    }

def test_plan_get_file_info():
    agent = OrbitAgent()

    result = agent.plan("show information about notes.txt")

    assert result == {
        "action": "get_file_info",
        "target": "notes.txt",
    }

def test_plan_search_files():
    agent = OrbitAgent()

    result = agent.plan("find Python files in Projects")

    assert result == {
        "action": "search_files",
        "target": {
            "directory": "Projects",
            "pattern": "*.py",
        },
    }

def test_plan_make_file():
    agent = OrbitAgent()

    result = agent.plan("make a file called notes.txt")

    assert result == {
        "action": "create_file",
        "target": "notes.txt",
    }