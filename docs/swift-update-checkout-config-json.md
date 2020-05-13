# Swift `update-checkout-config.json`

Swift uses the [update-checkout-config.json file](https://github.com/apple/swift/blob/master/utils/update_checkout/update-checkout-config.json) to track various branch schemes. The [swift-clowder repo](https://github.com/JrGoodle/swift-clowder) contains equivalent `clowder.yaml` files

## Default Configuration

The default branch setup is represented in `update-checkout-config.json`

```json
{
    "ssh-clone-pattern": "git@github.com:%s.git",
    "https-clone-pattern": "https://github.com/%s.git",
    "repos" : {
        "swift": {
            "remote": { "id": "apple/swift" } },
        "cmark": {
            "remote": { "id": "apple/swift-cmark" } },
        "llbuild": {
            "remote": { "id": "apple/swift-llbuild" } },
        "swift-argument-parser": {
            "remote": { "id": "apple/swift-argument-parser" } },
        "swift-driver": {
            "remote": { "id": "apple/swift-driver" } },
        "swift-tools-support-core": {
            "remote": { "id": "apple/swift-tools-support-core" } },
        "swiftpm": {
            "remote": { "id": "apple/swift-package-manager" } },
        "swift-syntax": {
            "remote": { "id": "apple/swift-syntax" } },
        "swift-stress-tester": {
            "remote": { "id": "apple/swift-stress-tester" } },
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
            "remote": { "id": "ninja-build/ninja" } },
        "icu": {
            "remote": { "id": "unicode-org/icu" },
            "platforms": [ "Linux" ]
        },
        "yams": {
            "remote": { "id": "jpsim/Yams" }
        },
        "cmake": {
            "remote": { "id": "KitWare/CMake" },
            "platforms": [ "Linux" ]
        },
        "pythonkit": {
            "remote": { "id": "pvieito/PythonKit" }
        },
        "tensorflow-swift-apis": {
            "remote": { "id": "tensorflow/swift-apis" }
        },
        "indexstore-db": {
            "remote": { "id": "apple/indexstore-db" } },
        "sourcekit-lsp": {
            "remote": { "id": "apple/sourcekit-lsp" } },
        "swift-format": {
            "remote": { "id": "apple/swift-format" } },
        "llvm-project": {
            "remote": { "id": "apple/llvm-project" } }
    },
    "default-branch-scheme": "master",
    "branch-schemes": {
       "master": {
            "aliases": ["master", "swift/master"],
            "repos": {
                "llvm-project": "swift/master",
                "swift": "master",
                "cmark": "master",
                "llbuild": "master",
                "swift-tools-support-core": "master",
                "swiftpm": "master",
                "swift-argument-parser": "0.0.5",
                "swift-driver": "master",
                "swift-syntax": "master",
                "swift-stress-tester": "master",
                "swift-corelibs-xctest": "master",
                "swift-corelibs-foundation": "master",
                "swift-corelibs-libdispatch": "master",
                "swift-integration-tests": "master",
                "swift-xcode-playground-support": "master",
                "ninja": "release",
                "icu": "release-65-1",
                "yams": "3.0.1",
                "cmake": "v3.16.5",
                "indexstore-db": "master",
                "sourcekit-lsp": "master",
                "swift-format": "master",
                "pythonkit": "master",
                "tensorflow-swift-apis": "master"
            }
        }
    }
}
```

An equivalent [default clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yaml)

```yaml
defaults:
  source: github
  protocol: ssh
  recursive: true

sources:
  - name: github
    url: github.com

projects:
  - name: llvm/llvm-project
    remote: upstream
    fork:
      name: apple/llvm-project
      branch: swift/master
  - name: apple/swift
  - name: commonmark/cmark
    remote: upstream
    fork:
      name: apple/swift-cmark
  - name: apple/swift-llbuild
    path: llbuild
  - name: apple/swift-tools-support-core
  - name: apple/swift-package-manager
    path: swiftpm
  - name: apple/swift-argument-parser
    tag: '0.0.5'
  - name: apple/swift-driver
  - name: apple/swift-syntax
  - name: apple/swift-stress-tester
  - name: apple/swift-corelibs-xctest
  - name: apple/swift-corelibs-foundation
  - name: apple/swift-corelibs-libdispatch
  - name: apple/swift-integration-tests
  - name: apple/swift-xcode-playground-support
  - name: ninja-build/ninja
    branch: release
  - name: unicode-org/icu
    tag: release-65-1
    groups: [linux, notdefault]
  - name: jpsim/Yams
    path: yams
    tag: '3.0.1'
  - name: KitWare/CMake
    path: cmake
    tag: v3.16.5
    groups: [linux, notdefault]
  - name: apple/indexstore-db
  - name: apple/sourcekit-lsp
  - name: apple/swift-format
  - name: pvieito/PythonKit
    path: pythonkit
  - name: tensorflow/swift-apis
    path: tensorflow-swift-apis
```

## Versions

The `swift-5.2-branch` version is represented in `update-checkout-config.json`

```json
"swift-5.2-branch": {
    "aliases": ["swift-5.2-branch", "swift/swift-5.2-branch"],
    "repos": {
        "llvm-project": "swift/swift-5.2-branch",
        "swift": "swift-5.2-branch",
        "cmark": "swift-5.2-branch",
        "llbuild": "swift-5.2-branch",
        "swift-tools-support-core": "swift-5.2-branch",
        "swiftpm": "swift-5.2-branch",
        "swift-syntax": "swift-5.2-branch",
        "swift-stress-tester": "swift-5.2-branch",
        "swift-corelibs-xctest": "swift-5.2-branch",
        "swift-corelibs-foundation": "swift-5.2-branch",
        "swift-corelibs-libdispatch": "swift-5.2-branch",
        "swift-integration-tests": "swift-5.2-branch",
        "swift-xcode-playground-support": "swift-5.2-branch",
        "ninja": "release",
        "icu": "release-65-1",
        "cmake": "v3.15.1",
        "indexstore-db": "swift-5.2-branch",
        "sourcekit-lsp": "swift-5.2-branch",
        "swift-format": "master"
    }
},
```

An equivalent [swift-5.2-branch clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/versions/swift-5.2-branch.clowder.yaml)

```yaml
defaults:
  source: github
  protocol: ssh
  recursive: true
  branch: swift-5.2-branch

sources:
  - name: github
    url: github.com

projects:
  - name: llvm/llvm-project
    remote: upstream
    fork:
      name: apple/llvm-project
      branch: swift/swift-5.2-branch
  - name: apple/swift
  - name: commonmark/cmark
    remote: upstream
    fork:
      name: apple/swift-cmark
  - name: apple/swift-llbuild
    path: llbuild
  - name: swift-tools-support-core
  - name: apple/swift-package-manager
    path: swiftpm
  - name: apple/swift-syntax
  - name: apple/swift-stress-tester
  - name: apple/swift-corelibs-xctest
  - name: apple/swift-corelibs-foundation
  - name: apple/swift-corelibs-libdispatch
  - name: apple/swift-integration-tests
  - name: apple/swift-xcode-playground-support
  - name: ninja-build/ninja
    branch: release
  - name: unicode-org/icu
    tag: release-65-1
    groups: [linux, notdefault]
  - name: KitWare/CMake
    path: cmake
    tag: v3.16.5
    groups: [linux, notdefault]
  - name: apple/indexstore-db
  - name: apple/sourcekit-lsp
  - name: apple/swift-format
    branch: master
```
