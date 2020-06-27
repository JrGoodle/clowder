[![Documentation Status](https://readthedocs.org/projects/clowder/badge/?version=latest)](http://clowder.readthedocs.io)
[![CircleCI](https://circleci.com/gh/JrGoodle/clowder.svg?style=shield)](https://circleci.com/gh/JrGoodle/clowder)
[![Maintainability](https://api.codeclimate.com/v1/badges/56c92799de08f9ef9258/maintainability)](https://codeclimate.com/github/JrGoodle/clowder/maintainability)
[![codecov](https://codecov.io/gh/JrGoodle/clowder/branch/master/graph/badge.svg)](https://codecov.io/gh/JrGoodle/clowder)
[![PyPI version](https://badge.fury.io/py/clowder-repo.svg)](https://badge.fury.io/py/clowder-repo)
[![Python version](https://img.shields.io/pypi/pyversions/clowder-repo.svg)](https://pypi.python.org/pypi/clowder-repo)
[![Requirements Status](https://requires.io/github/JrGoodle/clowder/requirements.svg?branch=master)](https://requires.io/github/JrGoodle/clowder/requirements/?branch=master)

> **clowder** - A group of cats
>
> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic

## Table of Contents

* [Why clowder](#why-clowder)
* [Installation](#installation)
* [The clowder.yml file](#the-clowderyml-file)
  * [Syntax](#syntax)
* [Basic command usage](#basic-command-usage)
  * [clowder init](#clowder-init)
  * [clowder herd](#clowder-herd)
  * [clowder status](#clowder-status)
  * [clowder forall](#clowder-forall)
  * [git commands](#git-commands)
  * [clowder repo commands](#clowder-repo-commands)
  * [config commands](#config-commands)
* [Development](#development)

## Why clowder

Managing multiple repositories can be pretty frustrating. There are a number of existing options, the primary being git submodules and subtrees. Google's [repo](https://code.google.com/p/git-repo) tool takes a different approach, but is closely tied to Google's development workflow. `clowder` uses a similar approach as `repo`, but without the ties to Google's Android workflows. Information about projects is specified in a `clowder.yml` file. Projects can track branches, or be tied to specific tags or commits. This file can be checked into its own repository so it can be versioned and shared across teams. The primary purpose of `clowder` is synchronization of multiple repositories, so normal development still takes place in individual repositories with the usual `git` commands.

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

```yaml
name: my-first-clowder

defaults:
  protocol: ssh

sources:
  - name: github
    url: github.com

projects:
  - name: jrgoodle/mu
  - name: jrgoodle/duke
  - name: jrgoodle/kit
    groups: [black-cats]
  - name: jrgoodle/kishka
    groups: [black-cats]
  - name: jrgoodle/june
    groups: [black-cats, notdefault]
  - name: jrgoodle/sasha
    groups: [black-cats, notdefault]
```

### Syntax

For more information, see [the clowder.yml syntax reference](docs/clowder-yml-syntax-reference.md)

```yaml
name: my-first-clowder
```

The `name` is simply a descriptive identifier. It must be a string that doesn't contain any spaces

```yaml
defaults:
  protocol: ssh
```

The `defaults` section requires the `protocol` to use for cloning repositories. The default `remote` is assumed to be `origin` and the default `branch` is assumed to to be `master`

```yaml
sources:
  - name: github
    url: github.com
```

The `sources` section contains all the locations to clone repositories from.

```yaml
projects:
  - name: jrgoodle/mu
  - name: jrgoodle/duke
  - name: jrgoodle/kit
    groups: [black-cats]
  - name: jrgoodle/kishka
    groups: [black-cats]
  - name: jrgoodle/june
    groups: [black-cats, notdefault]
  - name: jrgoodle/sasha
    groups: [black-cats, notdefault]
```

A project requires at minimum the `name` of the repository. This is combined with `defaults.protocol` or `sources.protocol` to form the full url for cloning the repository, taking the form of  `git@${sources.url}:${projects.name}.git` or `https://${sources.url}/${projects.name}.git`, depending on the protocol specified. If no `path` is specified, the last component of the `name` is used for the directory the project is cloned to. Projects can specify custom `groups` in order to run commands for only certain projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present, then the project will not be included in commands unless another `group` argument is given that it belongs to.

There's much more cusomization possible with `clowder`. For some more complex examples see:

[Cats clowder.yml example](docs/clowder-yml-cats.md)

[Forks clowder.yml example](docs/clowder-yml-forks.md)

## Basic Command Usage

For more information, see [the commands doc](docs/commands.md)

First create a directory where all the projects will be cloned:

```bash
mkdir cats
cd cats
```

It's possible to just create a local `clowder.yml` file, but it's recommended to check the file into the root of a dedicated repository. These examples use an [existing repository](https://github.com/JrGoodle/clowder-examples) containing a [clowder.yml](https://github.com/JrGoodle/clowder-examples/blob/master/clowder.yml) file.

### clowder init

```bash
clowder init git@github.com:JrGoodle/clowder-examples.git
```

The `clowder init` command does the following:

* Clones the [examples clowder repo](https://github.com/JrGoodle/clowder-examples) in the `cats/.clowder` directory
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

See [CONTRIBUTING.md](https://github.com/JrGoodle/clowder/blob/master/CONTRIBUTING.md) for information on setting up your environment for development and contribution guidelines
