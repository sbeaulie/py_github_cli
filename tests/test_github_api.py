from py_github_cli.github_api import repository
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest

import json
import requests
from requests import Response
from collections import OrderedDict

releases_json = json.loads(
    """[
    {
        "url": "https://api.github.com/repos/octocat/Hello-World/releases/1",
        "html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
        "assets_url": "https://api.github.com/repos/octocat/Hello-World/releases/1/assets",
        "upload_url": "https://uploads.github.com/repos/octocat/Hello-World/releases/1/assets{?name,label}",
        "tarball_url": "https://api.github.com/repos/octocat/Hello-World/tarball/v1.0.0",
        "zipball_url": "https://api.github.com/repos/octocat/Hello-World/zipball/v1.0.0",
        "id": 1,
        "node_id": "MDc6UmVsZWFzZTE=",
        "tag_name": "v1.0.0",
        "target_commitish": "master",
        "name": "v1.0.0",
        "body": "Description of the release",
        "draft": false,
        "prerelease": false,
        "created_at": "2013-02-27T19:35:32Z",
        "published_at": "2013-02-27T19:35:32Z"
    }
    ]"""
)

prs_json = json.loads(
    """[
  {
    "url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
    "id": 1,
    "node_id": "MDExOlB1bGxSZXF1ZXN0MQ==",
    "html_url": "https://github.com/octocat/Hello-World/pull/1347",
    "diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
    "patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch",
    "issue_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
    "commits_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits",
    "review_comments_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments",
    "review_comment_url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}",
    "comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
    "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e",
    "number": 1347,
    "state": "open",
    "locked": true,
    "title": "Amazing new feature",
    "user": {
      "login": "octocat",
      "id": 1,
      "node_id": "MDQ6VXNlcjE=",
      "avatar_url": "https://github.com/images/error/octocat_happy.gif",
      "gravatar_id": "",
      "url": "https://api.github.com/users/octocat",
      "html_url": "https://github.com/octocat",
      "followers_url": "https://api.github.com/users/octocat/followers",
      "following_url": "https://api.github.com/users/octocat/following{/other_user}",
      "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
      "organizations_url": "https://api.github.com/users/octocat/orgs",
      "repos_url": "https://api.github.com/users/octocat/repos",
      "events_url": "https://api.github.com/users/octocat/events{/privacy}",
      "received_events_url": "https://api.github.com/users/octocat/received_events",
      "type": "User",
      "site_admin": false
    },
    "body": "Please pull these awesome changes in!",
    "active_lock_reason": "too heated",
    "created_at": "2011-01-26T19:01:12Z",
    "updated_at": "2011-01-26T19:01:12Z",
    "closed_at": "2011-01-26T19:01:12Z",
    "merged_at": "2011-01-26T19:01:12Z",
    "merge_commit_sha": "e5bd3914e2e596debea16f433f57875b5b90bcd6",
    "_links": {
      "self": {
        "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
      },
      "html": {
        "href": "https://github.com/octocat/Hello-World/pull/1347"
      },
      "issue": {
        "href": "https://api.github.com/repos/octocat/Hello-World/issues/1347"
      },
      "comments": {
        "href": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
      },
      "review_comments": {
        "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
      },
      "review_comment": {
        "href": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
      },
      "commits": {
        "href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
      },
      "statuses": {
        "href": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
      }
    },
    "author_association": "OWNER",
    "auto_merge": null,
    "draft": false
  }
  ]"""
)


@patch("requests.get")
def test_github_api_http_get_request(mock_api_call):
    return_response = MagicMock(status_code=200, url="foobar", spec=Response)
    mock_api_call.return_value = return_response
    mock_api_call.return_value.json.return_value = releases_json
    repo = repository("OWENER/REPO")
    result = repository._http_get_request(repo, "foo")
    assert result == releases_json


@patch("requests.get")
def test_github_api_http_get_request_404(mock_api_call):
    return_response = MagicMock(status_code=404, url="foobar", spec=Response)
    mock_api_call.return_value = return_response
    repo = repository("OWENER/REPO")
    result = repository._http_get_request(repo, "foo")
    assert result == None


@patch("requests.get")
def test_github_api_http_get_request_500(mock_api_call):
    return_response = MagicMock(status_code=500, url="foobar", spec=Response)
    mock_api_call.return_value = return_response
    repo = repository("OWENER/REPO")
    result = repository._http_get_request(repo, "foo")
    assert result == None


@patch("requests.get")
def test_github_api_http_get_request_connectionfailure(mock_api_call):
    return_response = MagicMock(side_effect=requests.exceptions.Timeout())
    mock_api_call.side_effect = return_response
    repo = repository("OWENER/REPO")
    with pytest.raises(ConnectionError):
        result = repository._http_get_request(repo, "foo")


def test_github_api_get_releases():
    repository._http_get_request = MagicMock(return_value=releases_json)
    repo = repository("OWENER/REPO")
    assert repository.get_releases(repo) == [["v1.0.0", "v1.0.0"]]


def test_github_api_get_releases_empty():
    repository._http_get_request = MagicMock(return_value=json.loads("[]"))
    repo = repository("OWENER/REPO")
    assert repository.get_releases(repo) == []


def test_github_api_get_prs():
    repository._http_get_request = MagicMock(return_value=prs_json)
    repo = repository("OWENER/REPO")
    assert repository.get_prs(repo) == [[1347, "Amazing new feature"]]


def test_github_api_get_prs_empty():
    repository._http_get_request = MagicMock(return_value=json.loads("[]"))
    repo = repository("OWENER/REPO")
    assert repository.get_prs(repo) == []
