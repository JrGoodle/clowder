# `clowder` [![Build Status](https://travis-ci.org/JrGoodle/clowder.svg)](https://travis-ci.org/JrGoodle/clowder)

> **clowder** - A group of cats

> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic

Managing multiple repositories can be pretty frustrating. There are a number of existing options:

- [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [subtree merging](https://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging)
- [Google's repo tool](https://code.google.com/p/git-repo/)
- [braid](https://github.com/cristibalan/braid)
- [gr](https://github.com/mixu/gr)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo)

All of these have their own approach, but many are based on submodules or subtrees. Submodules and subtrees create a tight coupling between repositories because of the way dependencies are stored. Much has been written about their drawbacks elsewhere. Google's `repo` tool takes a different approach, but is closely tied to Google's development workflow

`clowder` uses a similar approach as `repo`, but using yaml instead of xml for the configuration file. URL information and relative project locations on disk are specified in a `clowder.yaml` file. This file is checked into its own repository. The use of a separate file to track projects allows for detailed information about the dependencies between them to be stored, but each repository is still essentially independent. Projects can track branches, or be tied to specific tags or commits

The primary purpose of `clowder` is synchronization of multiple repositories, so normal development still takes place in individual repositories with the usual `git` commands

## Getting Started

### Requirements

- [Python 3](https://www.python.org/downloads/)

#### macOS

Installation with [Homebrew](https://brew.sh)

```bash
$ brew install python3
```

#### Ubuntu 16.04

```bash
$ sudo apt install git
$ sudo apt install python3-pip
```

#### Windows

Install the following dependencies in [Cygwin](https://cygwin.com/install.html)

- git
- python3-pip
- python3

### Installation

To install `clowder` from PyPI

```bash
$ sudo pip3 install clowder-repo
```

To upgrade to the latest version

```bash
$ sudo pip3 install clowder-repo --upgrade
```

#### Shell Profile Customizations

For terminal autocompletion

```bash
# add to bash profile
command -v clowder >/dev/null 2>&1 && eval "$(register-python-argcomplete clowder)"
```

To make `clowder` available in your shell environment, it may be necessary to add the Python 3 bin directory to your environment's `PATH` variable. This is likely only necessary if you've previously installed `clowder` for development purposes

```bash
# macOS and Python 3.4
$ echo "$(dirname $(which python3))"
> /Library/Frameworks/Python.framework/Versions/3.4/bin
# add to bash profile
export PATH="/Library/Frameworks/Python.framework/Versions/3.4/bin:$PATH"
```

### Usage

This example is based on the [LLVM project](https://llvm.org) (see [the full clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml))

1. Create a directory to contain all the LLVM projects
    ```bash
    $ mkdir llvm-projects
    $ cd llvm-projects
    ```

2. Clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository (the "**clowder repo**") containing the `clowder.yaml` file
    ```bash
    $ clowder init https://github.com/jrgoodle/llvm-projects.git
    ```
    The `clowder init` command will do the following:
    - Clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository in the `llvm-projects/.clowder` directory
    - Create a symlink pointing to the primary `clowder.yaml` file in the repository

        ```bash
        llvm-projects/clowder.yaml -> llvm-projects/.clowder/clowder.yaml
        ```

3. Clone all repositories and check out refs specified in `clowder.yaml`
    ```bash
    $ clowder herd
    ```
    `clowder herd` updates the state of the projects. When `clowder herd` is run, the following happens:
    - If any projects don't have a clean git status then `clowder` exits
    - Projects are cloned if they don't currently exist
    - Each project fetches the latest changes
    - If the current git ref checked out doesn't match the `clowder.yaml` configuration, the correct ref will be checked out
    - The latest changes are pulled for branches. For commits and tags, the commits are checked out into a detached `HEAD` state

4. Print status of projects
    ```bash
    $ clowder status
    ```

For more example projects, see the [examples directory](https://github.com/JrGoodle/clowder/tree/master/examples).

## Further Information

### More `clowder` Commands

```bash
$ clowder clean # Discard any changes in projects
$ clowder diff # Print git diff for all projects
$ clowder forall -c "git status" # Run command in all project directories
$ clowder link -v 0.1 # Set clowder.yaml symlink to a previously saved version
$ clowder repo run 'git status' # Run command in .clowder directory
$ clowder save 0.1 # Save a version of clowder.yaml with current commit sha's
$ clowder start my_feature # Create new branch 'my_feature' for all projects
$ clowder stash # Stash changes in all projects
$ clowder prune stale_branch # Prune branch 'stale_branch' for all projects
```

See the [clowder commands doc](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md)
for more advanced `clowder` command usage

### The `clowder.yaml` File

See the [clowder.yaml doc](https://github.com/JrGoodle/clowder/blob/master/docs/clowder_yaml.md)
for an explanation of the `clowder.yaml` configuration file

### The `.clowder` Directory

See the [.clowder doc](https://github.com/JrGoodle/clowder/blob/master/docs/dot_clowder_dir.md)
for a description of the structure of the `.clowder` directory
