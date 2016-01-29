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

## Getting Started

### Requirements

[Python 3](https://www.python.org/downloads/) is necessary for `clowder`. On OS X it's simple to install Python 3 with Homebrew.

```bash
$ brew install python3
```

### Installation

To install from the [GitHub Releases](https://github.com/JrGoodle/clowder/releases) open a terminal and run:

```bash
$ pip3 install https://github.com/JrGoodle/clowder/releases/download/1.1.0/clowder-1.1.0-py3-none-any.whl
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

Clone repo containing `clowder.yaml` file ('clowder repo').

```bash
$ clowder init https://github.com/jrgoodle/llvm-projects.git
```

The `clowder init` command will clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository in the `llvm-projects/.clowder` directory and create a symlink pointing to the primary `clowder.yaml` file in the repository:

```
llvm-projects/clowder.yaml -> llvm-projects/.clowder/clowder.yaml
```

Next clone all repositories and check out refs specified in `clowder.yaml`:

```bash
$ clowder herd
```

The `clowder herd` command updates the state of the projects. The project repositories must have a clean git status, or `clowder` will exit. The `clowder.yaml` symlink is always updated to point to the primary `clowder.yaml` file in the clowder repo. Projects are cloned if they don't currently exist; otherwise, each project will pull the latest changes. If the current git ref checked out doesn't correspond to the `clowder.yaml` configuration, the correct ref will be checked out, and latest changes pulled for branches. For commits and tags, the commits are checked out into a detached `HEAD` state (`clowder forall` or `clowder start` can then be used to create/checkout branches).

For more example projects, see the [examples directory](https://github.com/JrGoodle/clowder/tree/master/examples).

## Further Information

### More `clowder` Commands

```bash
$ clowder clean # Discard any changes in projects
$ clowder forall "git status" # Run command in all project directories
$ clowder herd -b my_branch # Herd specified branch
$ clowder link -v 0.1 # Set clowder.yaml symlink to a previously saved version
$ clowder repo run 'git status' # Run command in .clowder directory
$ clowder save 0.1 # Save a version of clowder.yaml with current commit sha's
$ clowder start my_feature # Create new branch 'my_feature' for all projects
$ clowder stash # Stash changes in all projects
$ clowder status # print status of projects
$ clowder prune stale_branch # Prune branch 'stale_branch' for all projects
```

See the [clowder commands doc](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md)
for more advanced `clowder` command usage.

### The `clowder.yaml` File

See the [clowder.yaml doc](https://github.com/JrGoodle/clowder/blob/master/docs/clowder_yaml.md)
for an explanation of the `clowder.yaml` configuration file.

### The `.clowder` Directory

See the [.clowder doc](https://github.com/JrGoodle/clowder/blob/master/docs/dot_clowder_dir.md)
for a description of the structure of the `.clowder` directory.
