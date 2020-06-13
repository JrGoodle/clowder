# `clowder`

[![CircleCI](https://circleci.com/gh/JrGoodle/clowder.svg?style=shield)](https://circleci.com/gh/JrGoodle/clowder)
[![Maintainability](https://api.codeclimate.com/v1/badges/56c92799de08f9ef9258/maintainability)](https://codeclimate.com/github/JrGoodle/clowder/maintainability)
[![codecov](https://codecov.io/gh/JrGoodle/clowder/branch/master/graph/badge.svg)](https://codecov.io/gh/JrGoodle/clowder)
[![PyPI version](https://badge.fury.io/py/clowder-repo.svg)](https://badge.fury.io/py/clowder-repo)
[![Python version](https://img.shields.io/pypi/pyversions/clowder-repo.svg)](https://pypi.python.org/pypi/clowder-repo)
[![License](https://img.shields.io/pypi/l/clowder-repo.svg)](https://pypi.python.org/pypi/clowder-repo)
[![Status](https://img.shields.io/pypi/status/clowder-repo.svg)](https://pypi.python.org/pypi/clowder-repo)
[![Requirements Status](https://requires.io/github/JrGoodle/clowder/requirements.svg?branch=master)](https://requires.io/github/JrGoodle/clowder/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/clowder/badge/?version=latest)](http://clowder.readthedocs.io)

> **clowder** - A group of cats

> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic

Managing multiple repositories can be pretty frustrating. There are a number of existing options, the primary being git submodules and subtrees. Google's [repo](https://code.google.com/p/git-repo) tool takes a different approach, but is closely tied to Google's development workflow. `clowder` uses a similar approach as `repo`, but without the ties to Google's Android workflows. Detailed information about projects are specified in a `clowder.yml` file, but each repository is still essentially independent. Projects can track branches, or be tied to specific tags or commits. This file can be checked into its own repository so it can be versioned and shared across teams. The primary purpose of `clowder` is synchronization of multiple repositories, so normal development still takes place in individual repositories with the usual `git` commands

TODO: Why clowder?

## Table of Contents

* [Getting Started](#getting-started)
  * [Requirements](#requirements)
  * [Installation](#installation)
* [The clowder.yml file](#the-clowderyml-file)
  * [Breakdown](#breakdown)
* [Basic usage](#basic-usage)
  * [clowder init](#clowder-init)
  * [clowder herd](#clowder-herd)
  * [clowder status](#clowder-status)
* [Further Information](#further-information)
  * [More commands](#more-commands)
* [Development](#development)

## Getting Started

### Requirements

* [git](https://git-scm.com)
* [Python 3](https://www.python.org/downloads/)

### Installation

To install or upgrade `clowder` from PyPI

```bash
sudo pip3 install clowder-repo --upgrade
```

To install the latest pre-release version

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

### Breakdown

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

The `sources` section contains all the places to clone repositories from.

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

A project requires at minimum the `name` of the repository. This is combined with the `protocol` and `source` `url` to form the full url for cloning the repository, taking the form of  `git@${source.url}:${project.name}.git` or `https://${source.url}/${project.name}.git` depending on the protocol specified. If no `path` is specified, the last component of the `name` is used for the directory the project is cloned to. Projects can specify custom `groups` to run commands for only certain projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present then the project will not be included in commands unless another group argument is given that it belongs to.

There's much more cusomization possible with `clowder`. For some more complex examples see:

[Cats clowder.yml](docs/clowder-yml-cats.md)

[Forks clowder.yml](docs/clowder-yml-forks.md)

[clowder.yml Syntax Reference](docs/clowder-yml-syntax-reference.md)

## Basic Usage

First create a directory where all the projects will be cloned

```bash
mkdir cats
cd cats
```

### `clowder init`

It's possible to just create a local `clowder.yml` file, but it's recommended to check the file into the root of a dedicated repository. This exammple uses an [existing repository](https://github.com/JrGoodle/clowder-examples) containing a [clowder.yml](https://github.com/JrGoodle/clowder-examples/blob/master/clowder.yml) file

```bash
clowder init git@github.com:JrGoodle/clowder-examples.git
```

![clowder init](docs/README/clowder-init.png)

The `clowder init` command does the following

* Clones the [examples clowder repo](https://github.com/JrGoodle/clowder-examples) in the `cats/.clowder` directory
* Creates a symlink in the `cats` directory: `clowder.yaml` -> `.clowder/clowder.yml`

### `clowder herd`

```bash
clowder herd
```

![clowder herd](docs/README/clowder-herd.png)

`clowder herd` updates the state of the projects. When the command is run, the following happens

* If any projects don't have a clean git status then `clowder` exits
* Projects are cloned if they don't currently exist
* Each project fetches the latest changes
* If the current git ref checked out doesn't match the `clowder.yml` configuration, the correct ref will be checked out
* The latest changes are pulled for branches. For commits and tags, the commits are checked out into a detached `HEAD` state

### `clowder status`

```bash
clowder status
```

`clowder status` prints the current state of all projects

![clowder status](docs/README/clowder-status.png)

## Further Information

### More commands

```bash
clowder branch # Print all local branches
clowder checkout 'my_branch' # Checkout 'my_branch' in projects
clowder clean # Discard any changes in projects
clowder config get # EXPERIMENTAL: Get config values
clowder config set projects 'my_group' # EXPERIMENTAL: Set config values
clowder config clear projects # EXPERIMENTAL: Clear config values
clowder diff # Print git diff for all projects
clowder forall -c 'git status' # Run command in all project directories
clowder link 'v0.1' # Set clowder.yaml symlink to a previously saved version
clowder repo run 'git status' # Run command in .clowder directory
clowder save 'v0.1' # Save a version of clowder.yaml with current commit sha's
clowder start 'my_feature' # Create new branch 'my_feature' for all projects
clowder stash # Stash changes in all projects
clowder prune 'stale_branch' # Prune branch 'stale_branch' for all projects
```

For more information, see [the docs](http://clowder.readthedocs.io/en/latest/)

## Development

See [CONTRIBUTING.md](https://github.com/JrGoodle/clowder/blob/master/CONTRIBUTING.md) for information on setting up your environment for development and contribution guidelines
