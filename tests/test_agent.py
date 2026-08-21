from agent.core import OrbitAgent


def test_open_chrome():
    agent = OrbitAgent()

    result = agent.plan("Open Chrome")

    assert result == {
        "action": "open_app",
        "target": "chrome",
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
