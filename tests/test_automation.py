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
