"""CLI interface for py_github_cli project.

Usage:
    py_github_cli releases <repo>
    py_github_cli prs <repo>
    py_github_cli -h|--help

Options:
    -h --help       Show this screen.
"""
import regex
from docopt import docopt

from .github_api import repository


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m py_github_cli` and `$ py_github_cli `.
    """
    arguments = docopt(__doc__)
    repo = validate(arguments["<repo>"])

    github = repository(repo)
    if arguments["releases"]:
        github.get_releases()

    if arguments["prs"]:
        github.get_prs()


def validate(document):
    """Method to validate and sanitize the repository input

    Args:
        document (str): The github repository to validate

    Raises:
        ValueError: Raises and displays an error when the repository name is
        not valid

    Returns:
        str: Returns the sanitized github repo in the format OWNER/REPO
    """
    ok = regex.match(
        r"(https?://|git@)?(github.com(/|:))?([\w.-]+/[\w.-]+)", document
    )
    if not ok:
        raise ValueError(
            "Please enter a valid github repository"
            + " in the format myorganization/myrepo"
        )
    # get only the OWNER/REPO part of the match,
    # and remove any trailing '.git' string
    return regex.sub(r"\.git$", "", ok.groups()[-1])
