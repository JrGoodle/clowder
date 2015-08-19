# clowder [![Build Status](https://travis-ci.org/JrGoodle/clowder.svg)](https://travis-ci.org/JrGoodle/clowder)

> **clowder**  
> A group of cats

> **herding cats**  
> An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic.

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

See the [examples](https://github.com/JrGoodle/clowder/tree/master/examples) directory for a couple example projects.

## Getting Started

This example is based on the LLVM project.

```bash
$ mkdir llvm-projects
$ cd llvm-projects
$ clowder breed https://github.com/jrgoodle/llvm-projects.git
```

The `clowder breed` command will clone the [llvm-projects](https://github.com/jrgoodle/llvm-projects.git) repository in the `llvm-projects/clowder` directory. A symlink is created at `llvm-projects/clowder.yaml` pointing to `llvm-projects/clowder/clowder.yaml`.

```bash
$ clowder herd # herd default groups
$ clowder herd -a # herd all groups
```

Herding clones the project repository if it didn't previously exist.
Otherwise, each project will pull the latest changes.
If the default branch isn't checked out, current changes will be stashed, the default branch checked out, and latest changes pulled.

Example [clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml) for LLVM projects.

### Defaults

The **defaults** specify the default branch and remote for projects, and groups to sync by default with `clowder herd`.

```yaml
defaults:
    ref: refs/heads/master
    remote: github
    groups: [llvm, clang, projects]
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
    - name: projects
      projects:
        - name: llvm-mirror/compiler-rt
          path: llvm/projects/compiler-rt
        - name: llvm-mirror/libunwind
          path: llvm/projects/libunwind
        - name: llvm-mirror/dragonegg
          path: llvm/projects/dragonegg
    - name: libcxx
      projects:
        - name: llvm-mirror/libcxx
          path: llvm/projects/libcxx
        - name: llvm-mirror/libcxxabi
          path: llvm/projects/libcxxabi
    - name: lld
      projects:
        - name: llvm-mirror/lld
          path: llvm/tools/lld
    - name: lldb
      projects:
        - name: llvm-mirror/lldb
          path: lldb
    - name: libclc
      projects:
        - name: llvm-mirror/libclc
          path: libclc
    - name: llvm
      projects:
        - name: llvm-mirror/llvm
          path: llvm
```
