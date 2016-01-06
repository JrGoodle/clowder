# `clowder` [![Build Status](https://travis-ci.org/JrGoodle/clowder.svg)](https://travis-ci.org/JrGoodle/clowder)

> **clowder** - A group of cats

> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic.

Managing multiple repositories can be pretty frustrating. There are a number of existing options:

- [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [subtree merging](https://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging)
- [Google's repo tool](https://code.google.com/p/git-repo/)
- [GitSlave](http://gitslave.sourceforge.net)
- [braid](https://github.com/cristibalan/braid)
- [giternal](https://github.com/patmaddox/giternal)
- [git-submanage](https://github.com/idbrii/git-submanage)
- [gr](https://github.com/mixu/gr)
- [git-stree](https://github.com/tdd/git-stree)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo)

All of these have their own approach, but many are based on submodules or subtrees. Submodules and subtrees create a tight coupling between repositories because of the way dependencies are stored. Much has been written about their drawbacks elsewhere. Google's `repo` tool takes a different approach, but is closely tied to Google's development workflow.

`clowder` uses a similar approach as `repo` (and as it turns out, `gr` and `giternal`) with a yaml file instead of xml. URL information and relative project locations on disk are specified in a `clowder.yaml` file. This file is checked into its own repository. The use of a separate file for tracking projects means that there's detailed information about the dependencies between them, but each repository is still essentially independent. Projects can be tied to specific tags or commits, or can track branches. With the `clowder save <version>` command, specific versions of the `clowder.yaml` file can be saved from the current commit hashes of all projects for later restoration.

The primary purpose of `clowder` is synchronization of multiple repositories, so normal development still takes place in individual repositories with the usual `git` commands.

For a few example projects, see the [examples directory](https://github.com/JrGoodle/clowder/tree/master/examples).

## Getting Started

### Requirements

- [Python 3](https://www.python.org/downloads/)
- [pip3](https://pypi.python.org/pypi/pip) (and [setuptools](https://pypi.python.org/pypi/setuptools))

### Installation

To install from the [GitHub Releases](https://github.com/JrGoodle/clowder/releases) open a terminal and run:

```bash
$ pip3 install https://github.com/JrGoodle/clowder/releases/download/0.9.0/clowder-0.9.0-py3-none-any.whl
```

To install from the cloned repository:

```bash
$ git clone https://github.com/JrGoodle/clowder.git
$ cd clowder && ./install.sh
```

For terminal autocompletion, add the following to your shell profile:

```bash
[[ -f "/usr/local/bin/clowder" ]] && eval "$(register-python-argcomplete clowder)"
```

### Usage

This example is based on the LLVM project (see [the full clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml)). First create a directory to contain all the projects.

```bash
$ mkdir llvm-projects && cd llvm-projects
```

Clone repository containing `clowder.yaml` file.

```bash
$ clowder init https://github.com/jrgoodle/llvm-projects.git
```

The `clowder init` command will clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository in the `llvm-projects/.clowder` directory and create a symlink pointing to the primary `clowder.yaml` file in the repository:

```
llvm-projects/clowder.yaml -> llvm-projects/.clowder/clowder.yaml
```

Next sync all repositories:

```bash
$ clowder herd
```

The `clowder herd` command syncs the projects. The `clowder.yaml` symlink is always updated to point to the primary `clowder.yaml` file in the repository cloned with `clowder init`. Projects are cloned if they don't currently exist. Otherwise, each project will pull the latest changes. If the current branch isn't the default, it'll be checked out, and latest changes pulled. For commits and tags, the commits are checked out into a detached `HEAD` state (`clowder forall` can then be used to checkout/create branches).

### Further Commands

```bash
$ clowder save 0.1 # Save a version of clowder.yaml with current commit sha's
```

```bash
$ clowder forall "git status" # Run command in all project directories
$ clowder forall "git status" -g clang # Run command for projects in clang group
$ clowder forall "git status" -p llvm-mirror/clang # Run command for clang project
```

```bash
$ clowder clean # Discard any changes in projects
$ clowder clean -g clang # Discard any changes in projects in clang group
$ clowder clean -p llvm-mirror/clang # Discard any changes in clang project
```

```bash
$ clowder herd -g clang llvm # Only herd projects in clang and llvm groups
$ clowder herd -p llvm-mirror/clang # Only herd clang project
$ clowder herd -v 0.1 # Point clowder.yaml symlink to saved version
```

```bash
$ clowder status # print status of projects
$ clowder status -v # print more verbose status of projects
$ clowder status -g clang llvm # print status of projects in clang and llvm groups
$ clowder status -v -g clang # print verbose status of projects in clang group
```

```bash
$ clowder repo 'git status' # Run command in .clowder directory
```

```bash
$ clowder stash # Stash any changes in projects
$ clowder stash -g clang # Stash any changes in projects in clang group
$ clowder stash -p llvm-mirror/clang # Stash any changes in clang project
```

## The `clowder.yaml` File

See [clowder.yaml documentation](https://github.com/JrGoodle/clowder/blob/master/docs/clowder_yaml.sh)

## The `.clowder` Directory

See [.clowder documentation](https://github.com/JrGoodle/clowder/blob/master/docs/dot_clowder_dir.sh)
