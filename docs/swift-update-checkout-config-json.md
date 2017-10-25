# Swift `update-checkout-config.json`

Swift uses the [update-checkout-config.json file](https://github.com/apple/swift/blob/master/utils/update-checkout-config.json) to track various branch schemes. The [swift-clowder repo](https://github.com/JrGoodle/swift-clowder/tree/swift) contains equivalent `clowder.yaml` files

## Default Configuration

The default branch setup is represented in `update-checkout-config.json`

```json
{
    "ssh-clone-pattern": "git@github.com:%s.git",
    "https-clone-pattern": "https://github.com/%s.git",
    "repos" : {
        "llvm": {
            "remote": { "id": "apple/swift-llvm" } },
        "clang": {
            "remote": { "id": "apple/swift-clang" } },
        "swift": {
            "remote": { "id": "apple/swift" } },
        "lldb": {
            "remote": { "id": "apple/swift-lldb" } },
        "cmark": {
            "remote": { "id": "apple/swift-cmark" } },
        "llbuild": {
            "remote": { "id": "apple/swift-llbuild" } },
        "swiftpm": {
            "remote": { "id": "apple/swift-package-manager" } },
        "compiler-rt": {
            "remote": { "id": "apple/swift-compiler-rt" } },
        "swift-corelibs-xctest": {
            "remote": { "id": "apple/swift-corelibs-xctest" } },
        "swift-corelibs-foundation": {
            "remote": { "id": "apple/swift-corelibs-foundation" } },
        "swift-corelibs-libdispatch": {
            "remote": { "id": "apple/swift-corelibs-libdispatch" } },
        "swift-integration-tests": {
            "remote": { "id": "apple/swift-integration-tests" } },
        "swift-xcode-playground-support": {
            "remote": { "id": "apple/swift-xcode-playground-support" } },
        "ninja": {
            "remote": { "id": "ninja-build/ninja" } }
    },
    "default-branch-scheme": "master",
    "branch-schemes": {
        "master": {
            "aliases": ["master", "stable"],
            "repos": {
                "llvm": "stable",
                "clang": "stable",
                "swift": "master",
                "lldb": "stable",
                "cmark": "master",
                "llbuild": "master",
                "swiftpm": "master",
                "compiler-rt": "stable",
                "swift-corelibs-xctest": "master",
                "swift-corelibs-foundation": "master",
                "swift-corelibs-libdispatch": "master",
                "swift-integration-tests": "master",
                "swift-xcode-playground-support": "master",
                "ninja": "release"
            }
        }
    }
}
```

An equivalent [default clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yaml)

```yaml
defaults:
    ref: refs/heads/master
    remote: origin
    source: github
    recursive: true

sources:
    - name: github
      url: ssh://git@github.com
    - name: github-https
      url: https://github.com

groups:
    - name: swift
      projects:
        - name: apple/swift
          path: swift
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
    - name: swift-package-manager
      projects:
        - name: apple/swift-package-manager
          path: swiftpm
        - name: apple/swift-llbuild
          path: llbuild
    - name: third-party
      projects:
        - name: apple/swift-cmark
          path: cmark
        - name: ninja-build/ninja
          path: ninja
          ref: refs/heads/release
```

## Versions

The `swift-4.0-branch` version is represented in `update-checkout-config.json`

```json
"swift-4.1-branch" : {
    "aliases": ["swift-4.1-branch"],
    "repos": {
        "llvm": "swift-4.1-branch",
        "clang": "swift-4.1-branch",
        "swift": "swift-4.1-branch",
        "lldb": "swift-4.1-branch",
        "cmark": "swift-4.1-branch",
        "llbuild": "swift-4.1-branch",
        "swiftpm": "swift-4.1-branch",
        "compiler-rt": "swift-4.1-branch",
        "swift-corelibs-xctest": "swift-4.1-branch",
        "swift-corelibs-foundation": "swift-4.1-branch",
        "swift-corelibs-libdispatch": "swift-4.1-branch",
        "swift-integration-tests": "swift-4.1-branch",
        "swift-xcode-playground-support": "swift-4.1-branch",
        "ninja": "release"
    }
},
```

An equivalent [swift-4.1-branch clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/versions/swift-4.1-branch/clowder.yaml)

```yaml
import default

defaults:
    ref: refs/heads/swift-4.1-branch

groups:
    - name: llvm
      ref: refs/heads/swift-4.1-branch
```

By utilizing the import ability of `clowder`, the version file only needs to override necessary values, and inherits all the remaining defaults
