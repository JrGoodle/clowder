# `clowder` [![Build Status](https://travis-ci.org/JrGoodle/clowder.svg)](https://travis-ci.org/JrGoodle/clowder)

> **clowder** - A group of cats

> **herding cats** - An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic.

Managing multiple repositories of dependent code can be pretty frustrating. There are a number of existing options:

- [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [subtree merging](https://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging)
- [Google's repo tool](https://code.google.com/p/git-repo/)
- [git-submanage](https://github.com/idbrii/git-submanage)
- [gr](https://github.com/mixu/gr)
- [git-stree](https://github.com/tdd/git-stree)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo)

All of these have their own approach, but many are based on submodules or subtrees.
Google's `repo` tool takes a different approach, but is closely tied to Google's development workflow.

`clowder` uses a similar approach as `repo` but with a yaml file instead of xml.
URL information and project locations on disk are specified in a `clowder.yaml` file.
This file is checked into its own repository, so the project structure's history is saved under version control.
You can `fix` specific versions with current commit hashes saved for later restoration.

For a couple example projects, see the [examples directory](https://github.com/JrGoodle/clowder/tree/master/examples).

## Getting Started

This example is based on the LLVM project. See [the full clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml).

First create directory to contain all the projects.

```bash
$ mkdir llvm-projects
$ cd llvm-projects
```

Clone `clowder` repository containing `clowder.yaml` file.

```bash
$ clowder breed https://github.com/jrgoodle/llvm-projects.git
```

This command will clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository in the `llvm-projects/clowder` directory and create a symlink at `llvm-projects/clowder.yaml`.

```bash
$ clowder herd
```

This command syncs the projects. Projects are cloned if they don't currently exist. Otherwise, each project will pull the latest changes. If the current branch isn't the default, it'll be checked out, and latest changes pulled.

```bash
$ clowder sync
```

This command is like `clowder herd`, but for syncing the `clowder` repository.

### Further Commands

```bash
$ clowder meow # print status of projects
```

```bash
$ clowder groom # Discard any changes in projects
```

```bash
$ clowder stash # Stash any changes in projects
```

```bash
$ clowder fix -v v0.1 # Fix new version of clowder.yaml
```

```bash
$ clowder herd -v v0.1 # Check out fixed version
```

```bash
$ clowder forall -c "$COMMAND" # Run "$COMMAND" in all project directories
```

## The `clowder.yaml` File

### Defaults

The **defaults** specify the default branch and remote for projects.

```yaml
defaults:
    ref: refs/heads/master
    remote: github
```

### Remotes

Multiple **remotes** can be specified for use with different projects.

```yaml
remotes:
    - name: github-ssh
      url: ssh://git@github.com
    - name: github
      url: https://github.com
```

### Groups and Projects

**Groups** have a name and associated projects.
At a minimum, **Projects** need the `name` from the project's url, and the `path` to clone relative to the root directory.
The default `remote` and `ref` values can also be overridden on a per-project basis.

```yaml
groups:
    - name: clang
      projects:
        - name: llvm-mirror/clang
          path: llvm/tools/clang
        - name: llvm-mirror/clang-tools-extra
          path: llvm/tools/clang/tools/extra
    - name: llvm
      projects:
        - name: llvm-mirror/llvm
          path: llvm
```
