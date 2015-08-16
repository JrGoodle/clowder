# clowder

**clowder**: A group of cats

**Herding cats**: An idiom that refers to a frustrating attempt to control or organize a class of entities which are uncontrollable or chaotic.

Managing multiple repositories of dependent code can be pretty frustrating.

There are a number of existing options:

- [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [subtree merging](https://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging)
- [Google's repo tool](https://code.google.com/p/git-repo/)
- [git-submanage](https://github.com/idbrii/git-submanage)
- [gr](https://github.com/mixu/gr)
- [git-stree](https://github.com/tdd/git-stree)
- [git-subrepo](https://github.com/ingydotnet/git-subrepo)

All of these have their own approach, but many are based on submodules or subtrees.
Google's `repo` tool takes a different approach, but is closely tied to Google's development workflow.

`clowder` uses a similar approach as `repo`, but relies on a yaml file for specifying project layout, rather than xml.
It also avoids the default rebasing behavior that `repo` uses.

See the `examples` directory for a couple example projects.

## Brief Overview

[Example clowder.yaml for LLVM projects](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml)

### Defaults

```yaml
defaults:
    ref: refs/heads/master
    remote: github
    groups: [llvm, clang, compiler-rt]
```

### Remotes

```yaml
remotes:
    - name: github
      url: ssh://git@github.com
```

### Groups and projects

```yaml
groups:
    - name: clang
      projects:
        - name: llvm-mirror/clang
          path: llvm/tools/clang
        - name: llvm-mirror/clang-tools-extra
          path: llvm/tools/clang/tools/extra
    - name: compiler-rt
      projects:
        - name: llvm-mirror/compiler-rt
          path: llvm/projects/compiler-rt
```
