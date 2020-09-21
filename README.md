<center>

# `clowder`

|  |  |
|:-|:-|
| docs | [![Documentation Status](https://readthedocs.org/projects/clowder/badge/?version=latest)](http://clowder.readthedocs.io) |
| tests | [![GitHub Actions Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FJrGoodle%2Fclowder%2Fbadge&style=flat)](https://actions-badge.atrox.dev/JrGoodle/clowder/goto) [![CircleCI](https://circleci.com/gh/JrGoodle/clowder.svg?style=shield)](https://circleci.com/gh/JrGoodle/clowder) [![Code Climate Maintainability](https://api.codeclimate.com/v1/badges/56c92799de08f9ef9258/maintainability)](https://codeclimate.com/github/JrGoodle/clowder/maintainability) |
| package | [![codecov coverage](https://codecov.io/gh/JrGoodle/clowder/branch/master/graph/badge.svg)](https://codecov.io/gh/JrGoodle/clowder) [![PyPI version](https://badge.fury.io/py/clowder-repo.svg)](https://badge.fury.io/py/clowder-repo) [![Python versions](https://img.shields.io/pypi/pyversions/clowder-repo.svg)](https://pypi.python.org/pypi/clowder-repo) [![Requirements Status](https://requires.io/github/JrGoodle/clowder/requirements.svg?branch=master)](https://requires.io/github/JrGoodle/clowder/requirements/?branch=master) |

</center>

> **clowder** - A group of cats
>
> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic

## Table of Contents

* [Why clowder](#why-clowder)
* [Installation](#installation)
* [The clowder.yml file](#the-clowderyml-file)
* [Command Usage](#command-usage)
  * [clowder init](#clowder-init)
  * [clowder herd](#clowder-herd)
  * [clowder status](#clowder-status)
  * [clowder forall](#clowder-forall)
  * [git commands](#git-commands)
  * [clowder repo commands](#clowder-repo-commands)
  * [config commands](#config-command)
* [Development](#development)

## Why clowder

There are many ways to organize projects with git. Monorepos, submodules, subtrees, or [some](https://github.com/cristibalan/braid) [other](https://github.com/mixu/gr) [tool](https://github.com/ingydotnet/git-subrepo). `clowder` is one of the other tools. Its approach is heavily influeced by the [repo tool](https://gerrit.googlesource.com/git-repo) Google uses to manage the Android Open Source Project.

Projects are listed in a `clowder.yml` file that can be checked into its own repo, allowing it to be shared across teams. `clowder` essentially makes this file executable, allowing commands to be run across projects. `clowder` can update submodules, lfs files, and custom git config entries. Projects can track branches, or be tied to specific tags or commits. Upstreams can be configured along with their upstream source, wherever they may live. Snapshots of project states can be saved for later restoration. And more...

Daily development still takes place in individual repos, with normal `git` commands. But `clowder` is there if you need to synchronize or run commands on multiple repos.

## Installation

Requirements:

* [git](https://git-scm.com)
* [Python 3](https://www.python.org/downloads/)

To install or upgrade `clowder` from PyPI:

```bash
sudo pip3 install clowder-repo --upgrade
```

To install the latest pre-release version:

```bash
sudo pip3 install clowder-repo --force-reinstall --pre
```

## The clowder.yml file

For more inforrmation:

* [clowder.yml syntax reference](docs/clowder-yml-syntax-reference.md)
* [clowder.yml inheritance reference](docs/clowder-yml-syntax-reference-inheritance.md)

Example `clowder.yml` for [some](https://github.com/llvm/llvm-project) [well](https://github.com/apple/swift)-[known](https://github.com/tensorflow/tensorflow) [projects](https://gerrit.googlesource.com/git-repo):

```yaml
name: cool-projects

clowder:
  - llvm/llvm-project
  - apple/swift
  - tensorflow/tensorflow
```

Although terse, this is enough to enable `clowder`. With the ommitted default settings:

```yaml
name: cool-projects

sources:
  github:
    url: github.com

defaults:
  remote: origin
  source: github
  branch: master

clowder:
  - llvm/llvm-project
  - apple/swift
  - tensorflow/tensorflow
```

The `name` is simply a descriptive label. The `defaults` section contains the git branch and remote, the source to clone from, and the protocol to use for cloning repositories. `clowder` assumes the following defaults:

* `branch`: `master`
* `remote`: `origin`
* `source`: `github`
* `protocol`: `ssh`

The `sources` section contains all the git hosting providers. The following sources are built in to `clowder`:

* `github`: `github.com`
* `gitlab`: `gitlab.com`
* `bitbucket`: `bitbucket.org`

If we wanted to add a project at another hosting site:

```yaml
name: cool-projects

sources:
  google:
    url: gerrit.googlesource.com
    protocol: https

clowder:
  - llvm/llvm-project
  - apple/swift
  - tensorflow/tensorflow
  - name: git-repo
    path: repo
    source: google
```

A project requires a `name`, the path component of the git clone url. This is combined with `defaults.protocol` or `sources.protocol` to form the full git clone url, taking the form of  `git@${sources.url}:${projects.name}.git` or `https://${sources.url}/${projects.name}.git`. If `path` is not specified, the last component of the name is used for the local directory.

In order to be able to run commands for only certain sets of projects, there are groups:

```yaml
name: cool-projects

sources:
  google:
    url: gerrit.googlesource.com
    protocol: https

clowder:
  - name: llvm/llvm-project
    groups: [notdefault, clattner]
  - name: apple/swift
    groups: [clattner]
  - name: tensorflow/tensorflow
    groups: [google, clattner]
  - name: git-repo
    path: repo
    source: google
    groups: [google]
```

```yaml
name: cool-projects

clowder:
  clattner:
    - name: llvm/llvm-project
      groups: [notdefault]
    - apple/swift
    - name: tensorflow/tensorflow
      groups: [google]
  google:
    - name: git-repo
      path: repo
      source:
        url: gerrit.googlesource.com
        protocol: https
```

Projects are automatically added to the `all` group, a group of their `name`, and a group of their `path`. If `notdefault` is specified, the project will not be included in commands unless another group argument is given that it belongs to.

For some more custom examples, see:

* [Cats clowder.yml example](docs/clowder-yml-cats.md)
* [Upstreams clowder.yml example](docs/clowder-yml-upstreams.md)

## Command Usage

For the full command reference, see [the commands doc](docs/commands.md)

The following examples use an [existing repo](https://github.com/JrGoodle/clowder-examples) containing a [clowder.yml](https://github.com/JrGoodle/clowder-examples/blob/master/clowder.yml) file.

First, create a directory where all the projects will be cloned:

```bash
mkdir cats
cd cats
```

### clowder init

```bash
clowder init git@github.com:JrGoodle/clowder-examples.git
```

The `clowder init` command does the following:

* Clones the [examples clowder repo](https://github.com/JrGoodle/clowder-examples) in the `.clowder` directory
* Creates a symlink in the `cats` directory: `clowder.yml` -> `.clowder/clowder.yml`

![clowder init](docs/examples/clowder-init.gif)

### clowder herd

The `clowder herd` command updates the state of the projects. When the command is run, the following happens:

* If any projects don't have a clean git status then `clowder` exits
* Projects are cloned if they don't currently exist
* Each project fetches the latest changes
* If the current git ref checked out doesn't match the `clowder.yml` configuration, the correct ref will be checked out
* The latest changes are pulled for branches. For commits and tags, the commits are checked out into a detached `HEAD` state

![clowder herd](docs/examples/clowder-herd.gif)

### clowder status

The `clowder status` command prints the current state of all projects.

![clowder status](docs/examples/clowder-status.gif)

### clowder forall

```bash
clowder forall -c 'git status' # Run command in all project directories
```

### git commands

For more information, see [the commands doc](docs/commands.md#git-commands)

```bash
clowder branch # Print all local branches
clowder checkout 'my_branch' # Checkout 'my_branch' in projects if it exists
clowder clean # Discard any changes in projects
clowder diff # Print git diff for all projects
clowder start 'my_feature' # Create new branch 'my_feature' for all projects
clowder stash # Stash changes in all projects
clowder prune 'stale_branch' # Prune branch 'stale_branch' for all projects
```

### clowder repo commands

For more information, see [the commands doc](docs/commands.md#clowder-repo-commands)

```bash
clowder link 'v0.1' # Set clowder.yml symlink to a previously saved version
clowder repo run 'git status' # Run command in .clowder directory
clowder save 'v0.1' # Save a version of clowder.yml with current commit sha's
```

### config commands

**_NOTE: EXPERIMENTAL_**

For more information, see [the commands doc](docs/commands.md#clowder-config)

```bash
clowder config get # Get config values
clowder config set projects 'my_group' # Set config values
clowder config clear projects # Clear config values
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on setting up your environment for development and contribution guidelines
