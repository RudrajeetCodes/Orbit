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
