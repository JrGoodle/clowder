# The `clowder.yaml` File

The examples are based on [llvm-projects clowder.yaml](https://github.com/JrGoodle/llvm-projects/blob/master/clowder.yaml)

## Defaults

The `defaults` specify the default `ref`, `source`, and `remote` for projects. Optionally, a default `depth` can be specified

```yaml
defaults:
    ref: refs/heads/master
    remote: origin
    source: github
```

## Sources

Multiple `sources` can be specified. A `name` and `url` are required

```yaml
sources:
    - name: github-ssh
      url: ssh://git@github.com
    - name: github
      url: https://github.com
    - name: bitbucket
      url: ssh://git@bitbucket.org
```

## Groups and Projects

The `groups` each require a `name` and associated `projects`

At a minimum, `projects` require the `name` from the project's url, and the `path` to clone relative to the base directory. The default `remote`, `source`, `ref`, and `depth` values can be overridden on a per-project basis. It's also possible to add a reference to a fork by adding `fork` to a project, with a required `name` and `remote`. When a `fork` is present the `clowder start -t`, `clowder prune -r`, and `clowder prune -a` commands will apply to the fork's remote

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
          fork:
              name: jrgoodle/clang
              remote: origin
        - name: llvm-mirror/clang-tools-extra
          path: llvm/tools/clang/tools/extra
          remote: upstream
          fork:
              name: jrgoodle/clang-tools-extra
              remote: origin
    - name: projects
      projects:
        - name: llvm-mirror/compiler-rt
          path: llvm/projects/compiler-rt
          remote: upstream
          fork:
              name: jrgoodle/compiler-rt
              path: llvm/projects/compiler-rt
```

## Refs

The `ref` can specify a branch, tag, or commit hash with the following patterns

```yaml
# branch
ref: refs/heads/knead # track branch 'knead'
# tag
ref: refs/tags/v0.01 # point to commit with tag 'v0.01'
# commit
ref: 7083e8840e1bb972b7664cfa20bbd7a25f004018 # point to commit hash
```

## Imports

A `clowder.yaml` file can `import` another `clowder.yaml` file and override values from the other file, add new `groups`, and add new `projects`. If a file contains an `import`, then the normal requirements for a base `clowder.yaml` are relaxed. There must be at least one additional customization specified for a `clowder.yaml` with an `import` to be considered valid. To import the primary `clowder.yaml` specify `default`, otherwise specify the version name

An example that might be located at `versions/swift/clowder.yaml`. This will import the primary `clowder.yaml` and override the default `lldb` project with the Swift version. It also adds the `swift` group with the additional `apple/swift` project

```yaml
import: default

groups:
    - name: swift
      projects:
        - name: apple/swift
          path: swift
    - name: lldb
      projects:
        - name: apple/swift-lldb
          path: lldb
```

An example that might be located at `versions/v0.1-depth-1/clowder.yaml`. This will override the default `depth` option (Note: if `v0.1` was previously saved by the `clowder save` command, the `depth` value will be explicitly specified for all projects, so that would need to be removed in order for this customization to have an effect)

```yaml
import: v0.1

defaults:
    depth: 1
```
