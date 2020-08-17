# The `clowder.yaml` File

The examples are based on the [swift projects clowder.yaml files](https://github.com/JrGoodle/swift-clowder)

## Defaults

The `defaults` specify the default `ref`, `source`, `remote`, and `protocol` for projects. Optionally, a default `depth` can be specified

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
  github:
    url: github.com
  - name: bitbucket
    url: bitbucket.org
```

## Projects

At a minimum, `projects` require the `name` from the project's url, and the `path` to clone relative to the base directory. The default `remote`, `source`, `ref`, `depth`, and `timestamp_author` (most recent commit by author) values can be overridden on a per-project basis. Projects can specify a `groups` array to run commands for specific sets of projects. By default, a `project`'s `name` and `path` are added as groups. It's also possible to add a reference to a fork by adding `fork` to a project, with a required `name` and `remote`. When a `fork` is present the `clowder start -t`, `clowder prune -r`, and `clowder prune -a` commands will apply to the fork's remote.

```yaml
projects:
  - name: apple/swift
    path: swift
    remote: upstream
    groups: [swift]
    fork:
      name: JrGoodle/swift
      remote: origin
  - name: apple/swift-llvm
    path: llvm
    ref: refs/heads/stable
    timestamp_author: swift-ci
    groups: [llvm]
  - name: apple/swift-clang
    path: clang
    ref: refs/heads/stable
    timestamp_author: swift-ci
    groups: [llvm]
  - name: apple/swift-compiler-rt
    path: compiler-rt
    ref: refs/heads/stable
    groups: [llvm]
  - name: apple/swift-lldb
    path: lldb
    ref: refs/heads/stable
    timestamp_author: swift-ci
    groups: [llvm]
  - name: apple/swift-corelibs-foundation
    path: swift-corelibs-foundation
    groups: [corelibs]
  - name: apple/swift-corelibs-libdispatch
    path: swift-corelibs-libdispatch
    groups: [corelibs]
  - name: apple/swift-corelibs-xctest
    path: swift-corelibs-xctest
    groups: [corelibs]
  - name: apple/swift-integration-tests
    path: swift-integration-tests
    groups: [corelibs]
  - name: apple/swift-xcode-playground-support
    path: swift-xcode-playground-support
    groups: [corelibs]
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
