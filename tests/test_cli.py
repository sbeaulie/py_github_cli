import pytest
import py_github_cli.cli
from unittest.mock import MagicMock
from unittest.mock import patch


@pytest.mark.parametrize(
    "input_repository_string, expected",
    [
        ("a/b", "a/b"),
        ("foo/bar", "foo/bar"),
        ("https://github.com/foo/bar", "foo/bar"),
        ("http://github.com/foo/bar", "foo/bar"),
        ("http://github.com/foo/bar/", "foo/bar"),
        ("git@github.com:foo/bar/", "foo/bar"),
        ("special/characters123_-.", "special/characters123_-."),
        (
            "https://github.com/kamranahmedse/developer-roadmap.git",
            "kamranahmedse/developer-roadmap",
        ),
    ],
)
def test_cli_validate(input_repository_string, expected):
    print(input_repository_string, expected)
    assert py_github_cli.cli.validate(input_repository_string) == expected


@pytest.mark.parametrize(
    "input_repository_string",
    ["a", "foobar", "inval!d/n@me"],
)
def test_cli_validate_raises_exception(input_repository_string):
    with pytest.raises(ValueError):
        py_github_cli.cli.validate(input_repository_string)


@patch("py_github_cli.github_api.repository.get_releases")
def test_cli_main_releases(mock_api_call):
    py_github_cli.cli.ver = MagicMock(return_value="MockVersion")
    py_github_cli.cli.docopt = MagicMock(
        return_value={"releases": True, "prs": False, "<repo>": "foo/bar"}
    )
    py_github_cli.cli.validate = MagicMock(return_value="foo/bar")
    mock_api_call.return_value = MagicMock()
    py_github_cli.cli.main()
    mock_api_call.assert_called_once()


@patch("py_github_cli.github_api.repository.get_prs")
def test_cli_main_prs(mock_api_call):
    py_github_cli.cli.ver = MagicMock(return_value="MockVersion")
    py_github_cli.cli.docopt = MagicMock(
        return_value={"releases": False, "prs": True, "<repo>": "foo/bar"}
    )
    py_github_cli.cli.validate = MagicMock(return_value="foo/bar")
    mock_api_call.return_value = MagicMock()
    py_github_cli.cli.main()
    mock_api_call.assert_called_once()
