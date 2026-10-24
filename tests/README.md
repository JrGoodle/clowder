# Examples

The GitHub links below use the current repository owners. This draft uses
`polka-dot-cat/...` project names. Cats' published `master` and `alt-branch`
manifests retain the old names until PR #641 merges. Before that cutover, test
the draft against the staged manifests described below. See the
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

### Testing the draft before the manifest cutover

Cats has migration branches `org-migration/master` and
`org-migration/alt-branch`. Use a temporary bare clone with those commits as its
local active branches. This leaves the published fixtures compatible with the
existing Clowder tests until the migration PR merges.

```sh
cats_fixture_dir=$(mktemp -d)
git clone --bare https://github.com/polka-dot-cat/cats.git "$cats_fixture_dir/cats.git"
git -C "$cats_fixture_dir/cats.git" update-ref refs/heads/master refs/heads/org-migration/master
git -C "$cats_fixture_dir/cats.git" update-ref refs/heads/alt-branch refs/heads/org-migration/alt-branch

env GIT_CONFIG_COUNT=2 \
  GIT_CONFIG_KEY_0="url.file://$cats_fixture_dir/cats.git.insteadOf" \
  GIT_CONFIG_VALUE_0=https://github.com/polka-dot-cat/cats.git \
  GIT_CONFIG_KEY_1=protocol.file.allow GIT_CONFIG_VALUE_1=always \
  pipenv run python -m pytest tests/functional/test_features.py -q \
    -m 'cats and not (ssh or offline or write or lfs or help or init)' \
    -k 'forall or yaml or submodules'
```

The URL override applies only to this command and the root Cats repository.
Child repositories still use GitHub. Do not use this override for tests that
assert the root Cats remote URL: Git reports the rewritten local URL.
After the active manifests are updated, omit the override.

GitHub Actions uses these same staged commits until cutover. It runs the 14
initialization cases against the published URLs, then 667 other non-SSH,
non-offline, non-write, non-LFS cases against the staged fixtures. The three LFS
cases run serially afterward on each disposable runner. Remove the workflow's
temporary fixture pins and overrides once the active manifests are published.
See the [CI preflight record](../docs/clowder-transfer-preflight.md#github-actions).

CircleCI's active `test_write` job uses the same staged Cats commits for its 89
cases. It rewrites only the root Cats SSH/HTTPS URLs; child repositories retain
their GitHub SSH remotes and the tests can create/delete remote `pytest*` branches.
A CircleCI serial group prevents concurrent write-test jobs. Coverage, JUnit,
and Cucumber reports are stored as artifacts without the legacy Code Climate reporter.

### Felidae, submodules, and Beanstalk

The GitHub YAML fixtures use `polka-dot-cat/felidae`. Its active `master` and
`felid` branches, and `mu`'s `submodules` branch, now reference
`polka-dot-cat/ash`; Ash references `polka-dot-cat/duffy`. Tags and fixed commits
retain their original history and can still contain URLs served through GitHub
redirects.

The explicit `source.url` scenarios retain
`git@polka-dot-cat.git.beanstalkapp.com:polka-dot-cat/felidae.git`.
This is a separate hosting service, even though the project name matches GitHub.
The 28 explicit source-URL cases need Beanstalk SSH access and a verified server
host key. Adding an account public key does not establish server trust.

The GitHub-only project YAML cases can run separately:

```sh
pipenv run python -m pytest tests/functional/test_schema_validation.py -q \
  -k 'project and not upstream and not git_lfs and (not source_url or implicit)'
```

These YAML cases use GitHub SSH but do not use the Cats setup that deletes
remote `pytest*` branches. Exclude the `lfs` scenarios on a shared workstation:
some of their steps modify global/system Git LFS settings.

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
