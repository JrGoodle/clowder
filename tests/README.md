# Examples

The GitHub links below use the current repository owners. The served manifests
still contain some `JrGoodle/...` project names. Keep those names and the matching
assertions together until the manifest migration is complete. See the
[transfer progress record](../docs/clowder-repository-transfer-status.md).

## Cats

https://github.com/polka-dot-cat/cats.git

| Directory | Repository |
|-----------|------------|
| `black-cats/june` | https://github.com/polka-dot-cat/june |
| `black-cats/kishka` | https://github.com/polka-dot-cat/kishka |
| `black-cats/kit` | https://github.com/polka-dot-cat/kit |
| `black-cats/sasha` | https://github.com/polka-dot-cat/sasha |
| `duke` | https://github.com/polka-dot-cat/duke |
| `mu` | https://github.com/polka-dot-cat/mu |

## Misc

https://github.com/polka-dot-cat/misc-clowder-tests.git

The root manifest and its `defaults` and `https` saved versions use these
repositories. The integration scenarios need both each fork and its upstream.

| Directory | Fork | Upstream | Branch |
| --- | --- | --- | --- |
| `djinni` | [polka-dot-cat/djinni](https://github.com/polka-dot-cat/djinni) | [dropbox/djinni](https://github.com/dropbox/djinni) | `master` |
| `gyp` | [polka-dot-cat/gyp](https://github.com/polka-dot-cat/gyp) | [Chromium GYP](https://chromium.googlesource.com/external/gyp/) | `fork-branch` |
| `sox` | [polka-dot-cat/sox](https://github.com/polka-dot-cat/sox) | [SourceForge SoX](https://sourceforge.net/p/sox/code/ci/master/tree/) | `master` |

Keep GYP's remote `fork-branch` at
`bd11dd1c51ef17592384df927c47023071639f96`. The upstream-update scenario starts
there and advances only its temporary local branch. Updating the GitHub branch
would remove the starting state that the test checks.

Run the 41 miscellaneous command cases and 57 related upstream YAML cases with:

```sh
pipenv run python -m pytest tests/functional/test_features.py -q -m misc
pipenv run python -m pytest tests/functional/test_schema_validation.py -q -k 'upstream and (not source_url or implicit)'
```

These selections require network and GitHub SSH access. They use temporary local
repositories; the selected setup paths do not delete or push remote branches.
Recheck that assumption if the fixtures change.

## Swift

https://github.com/polka-dot-cat/swift-clowder.git

| Directory | Repository |
|-----------|------------|
| `clang` | https://github.com/apple/swift-clang |
| `cmark` | https://github.com/apple/swift-cmark |
| `compiler-rt` | https://github.com/apple/swift-compiler-rt |
| `llbuild` | https://github.com/apple/swift-llbuild |
| `lldb` | https://github.com/apple/swift-lldb |
| `llvm` | https://github.com/apple/swift-llvm |
| `ninja` | https://github.com/ninja-build/ninja.git |
| `swift` | https://github.com/apple/swift |
| `swift-corelibs-foundation` | https://github.com/apple/swift-corelibs-foundation |
| `swift-corelibs-libdispatch` | https://github.com/apple/swift-corelibs-libdispatch |
| `swift-corelibs-xctest` | https://github.com/apple/swift-corelibs-xctest |
| `swift-integration-tests` | https://github.com/apple/swift-integration-tests |
| `swift-xcode-playground-support` | https://github.com/apple/swift-xcode-playground-support |
| `swiftpm` | https://github.com/apple/swift-package-manager |
