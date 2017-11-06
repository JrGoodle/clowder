# The `clowder.yaml` File

The examples are based on the [swift projects clowder.yaml files](https://github.com/JrGoodle/swift-clowder)

## Defaults

The `defaults` specify the default `ref`, `source`, and `remote` for projects. Optionally, a default `depth` can be specified

```yaml
defaults:
    ref: refs/heads/master
    remote: origin
    source: github
    protocol: ssh
```

## Sources

Multiple `sources` can be specified. A `name` and `url` are required

```yaml
sources:
    - name: github
      url: github.com
    - name: bitbucket
      url: bitbucket.org
```

## Groups and Projects

The `groups` each require a `name` and associated `projects`

At a minimum, `projects` require the `name` from the project's url, and the `path` to clone relative to the base directory. The default `remote`, `source`, `ref`, `depth`, and `timestamp_author` values can be overridden on a per-project basis. It's also possible to add a reference to a fork by adding `fork` to a project, with a required `name` and `remote`. When a `fork` is present the `clowder start -t`, `clowder prune -r`, and `clowder prune -a` commands will apply to the fork's remote

```yaml
groups:
    - name: swift
      projects:
        - name: apple/swift
          path: swift
          fork:
              name: JrGoodle/swift
              remote: origin
    - name: llvm
      ref: refs/heads/stable
      projects:
        - name: apple/swift-llvm
          path: llvm
          timestamp_author: swift-ci
        - name: apple/swift-clang
          path: clang
          timestamp_author: swift-ci
        - name: apple/swift-compiler-rt
          path: compiler-rt
        - name: apple/swift-lldb
          path: lldb
          timestamp_author: swift-ci
    - name: swift-corelibs
      projects:
        - name: apple/swift-corelibs-foundation
          path: swift-corelibs-foundation
        - name: apple/swift-corelibs-libdispatch
          path: swift-corelibs-libdispatch
        - name: apple/swift-corelibs-xctest
          path: swift-corelibs-xctest
        - name: apple/swift-integration-tests
          path: swift-integration-tests
        - name: apple/swift-xcode-playground-support
          path: swift-xcode-playground-support
```

## Refs

The `ref` can specify a branch, tag, or commit hash with the following patterns

```yaml
# branch
ref: refs/heads/stable # track branch 'stable'
# tag
ref: refs/tags/swift-4.0-RELEASE # point to commit with tag 'swift-4.0-RELEASE'
# commit
ref: 3416108abd0df3997a533a14c5ad06de20ba8a60 # point to commit hash
```

## Imports

A `clowder.yaml` file can `import` another `clowder.yaml` file and override values from the other file, add new `groups`, and add new `projects`. If a file contains an `import`, then the normal requirements for a base `clowder.yaml` are relaxed. There must be at least one additional customization specified for a `clowder.yaml` with an `import` to be considered valid. To import the primary `clowder.yaml` specify `default`, otherwise specify the version name

The [swift-4.1-branch-import clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/versions/swift-4.1-branch-import/clowder.yaml) file demonstrates `import` usage. This version will import the primary `clowder.yaml` and override the default `ref` with `refs/heads/swift-4.1-branch`. The `llvm` group `ref` also requires an override since it was specified to be `refs/heads/stable` in the [default clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yaml)

```yaml
import default

defaults:
    ref: refs/heads/swift-4.1-branch
    source: github-https

groups:
    - name: llvm
      ref: refs/heads/swift-4.1-branch
```

An example that might be located at `versions/v0.1-depth-1/clowder.yaml`. This will override the default `depth` option

**Note: If `v0.1` was previously saved by the `clowder save` command, the `depth` value will be explicitly specified for all projects, so that would need to be removed in order for this customization to have an effect**

```yaml
import: v0.1

defaults:
    depth: 1
```
