## The `clowder.yaml` File

The examples are based on [llvm-projects clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml)

### Defaults

The `defaults` specify the default `ref`, `source`, and `remote` for projects.

```yaml
defaults:
    ref: refs/heads/master
    remote: origin
    source: github
```

### Sources

Multiple `sources` can be specified.

```yaml
sources:
    - name: github-ssh
      url: ssh://git@github.com
    - name: github
      url: https://github.com
    - name: bitbucket
      url: ssh://git@bitbucket.org
```

### Groups and Projects

The `groups` each have a `name` and associated `projects`.
At a minimum, `projects` need the `name` from the project's url, and the `path` to clone relative to the base directory.
The default `remote`, `source`, and `ref` values can be overridden on a per-project basis. The `depth` can be set to do a shallow clone. It's also possible to add references to forks in the same `clowder.yaml` file by specifying `forks` with a `name` and `remote`.

```yaml
groups:
    - name: llvm
      projects:
        - name: llvm-mirror/llvm
          path: llvm
          depth: 5
    - name: clang
      projects:
        - name: llvm-mirror/clang
          path: llvm/tools/clang
          remote: upstream
          forks:
            - name: jrgoodle/clang
              remote: origin
        - name: llvm-mirror/clang-tools-extra
          path: llvm/tools/clang/tools/extra
          remote: upstream
          forks:
            - name: jrgoodle/clang-tools-extra
              remote: origin
    - name: projects
      projects:
        - name: llvm-mirror/compiler-rt
          path: llvm/projects/compiler-rt
          remote: upstream
          forks:
            - name: jrgoodle/compiler-rt
              path: llvm/projects/compiler-rt
```

### Refs

The `ref` can specify a branch, tag, or commit hash with the following patterns:

```yaml
# branch
ref: refs/heads/knead # track branch 'knead'
# tag
ref: refs/tags/v0.01 # point to commit with tag 'v0.01'
# commit
ref: 7083e8840e1bb972b7664cfa20bbd7a25f004018 # point to commit hash
```
