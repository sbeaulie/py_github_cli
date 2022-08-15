---
# py_github_cli

[![CI](https://github.com/sbeaulie/py_github_cli/actions/workflows/main.yml/badge.svg)](https://github.com/sbeaulie/py_github_cli/actions/workflows/main.yml)

py_github_cli created by sbeaulie

## Usage

```bash
$ python -m py_github_cli
#or
$ py_github_cli
Usage:
    py_github_cli releases <repo>
    py_github_cli prs <repo>
    py_github_cli -h|--help
    py_github_cli -v|--version
```

## Example usage

![Usage](https://github.com/sbeaulie/py_github_cli/gifs/usage.gif)

## Supported commands
There are two cli commands supported: releases and prs
### releases
py_github_cli releases -> to get the top 3 releases names and versions
### prs
py_github_cli prs -> to get the top 3 prs

## Supported repos

After the command (releases or prs) the first parameter is the repo name
py_github_cli releases <repo>
### Repo format
1. OWNER/REPO for example monkey/github_cli
2. https://github.com/OWNER/REPO or
3. git@github.com:OWNER/REPO
### Public repos
Public repos can be queried by anyone without authentication.
### Private repos
Private repos can be queried only if you provide a user and token for access.
If querying a private repo without them, you will get a 404 error (same as not found)
```bash
$ export USER=foo; export TOKEN=ghp_foobar
```
A personal access token can be created in the github UI
1. Go to Settings/Developer settings (https://github.com/settings/tokens)
2. Click generate new token
3. Select the permission for 'repo'
4. save and take note of the token
5. export TOKEN=${TOKEN_FROMSTEP_4} or set it before running the program

## Known limitations
### Github rate limiting
60 requests per hour when unauthenticated
5000 requests per hour when authenticated via the USER and TOKEN environment variables
See https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Docker-compose
Perhaps the easiest way to run this code without having to install python and virtualenv
which uses an off-the-shelf python alpine image (only 170MB)

```bash
# optional export ENV vars see above for private repos
$ docker-compose run cli py_github_cli prs vuejs/vue
Received response: 200 https://api.github.com/repos/vuejs/vue/pulls?per_page=3
Listing top 3 PRs
      
  NUMBER  TITLE                                                    
    
  12738   fix: vue ssr server error when mapped item is undefined  
  12737   feat(types): new Vue() improvements (#12730)             
  12735   chore(v3/lifecycle): Enhanced type for onErrorCaptured   
```
