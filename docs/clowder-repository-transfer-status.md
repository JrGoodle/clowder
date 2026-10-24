# Repository transfer progress

Updated October 23, 2026 (America/Chicago). Follow the
[transfer plan](clowder-repository-transfer-plan.md) for the full sequence.

## Current state

Preparation is complete for the first set of local URL changes. The main
repository remains `JrGoodle/clowder`; its remote, default branch, and public
visibility have not changed. The migration changes are committed locally on
`codex-cleanup`.
Links to `polka-dot-cat/clowder` are prepared for publication after the transfer.

`felidae` has been transferred to
[polka-dot-cat/felidae](https://github.com/polka-dot-cat/felidae). Its repository ID
is still `294826031`. Both branches and both tags match the backup, and the old
repository URL resolves to the new owner. The mirror and its LFS object are saved.

The replacement test repositories are now available under `polka-dot-cat`:
[djinni](https://github.com/polka-dot-cat/djinni),
[gyp](https://github.com/polka-dot-cat/gyp), and
[sox](https://github.com/polka-dot-cat/sox). Their default branch is `master`.
Their published manifests and the matching local Clowder assertions now use the
organization names. All 97 cases affected by the deleted forks and one new
saved-defaults regression pass. The broader Cats/Felidae name migration and main
repository transfer remain separate steps.

## Backups and inventory

The local backup directory, relative to the Clowder checkout, is
`../clowder-transfer-backups/20261024T023608Z/`. The UTC timestamp falls on
October 23 in the workstation's timezone. `../clowder-transfer-backups/latest.txt`
contains its absolute path. Keep these backups outside the repository.

- `clowder.git`: a mirror of the remote Git repository; `git fsck --full` passed.
- Git LFS fetch completed for all 149 Clowder objects.
- GitHub inventory: 13 branches, 40 tags, 40 releases, 55 open issues/PRs combined,
  including four open PRs; collaborators, branch protection, Pages, Actions,
  environments, and integration metadata were recorded.
- All 78 release assets were downloaded; sizes were checked and SHA-256 hashes
  recorded in `release-assets.json`.
- Secret names were inventoried, without secret values. Webhook URLs are recorded
  only as service hosts, without embedded credentials.
- `felidae.git` and `felidae-inventory.json` retain the test repository's
  pre-transfer state.
- Test collection, dependency analysis, and validation logs are saved beside the
  backups. The GitHub inventory is a configuration snapshot, not a complete
  export of issue comments or other GitHub application data.

## Repository mapping

| Existing reference | Confirmed destination or status |
| --- | --- |
| `JrGoodle/clowder` | Planned: `polka-dot-cat/clowder`; ownership change pending |
| `JrGoodle/cats`, `clowder-examples`, `misc-clowder-tests`, `swift-clowder` | Same repository names under `polka-dot-cat`; redirects verified |
| `JrGoodle/mu`, `duke`, `kit`, `kishka`, `sasha`, `june`, `duffy` | Same repository names under `polka-dot-cat`; redirects verified |
| `JrGoodle/felidae` | Transferred to `polka-dot-cat/felidae` in this transition |
| `JrGoodle/djinni`, `gyp`, `sox` | Recreated under `polka-dot-cat`; published manifests and local test assertions now use the organization URLs |
| `JrGoodle/ash` | Still exists under the personal account; referenced by `felidae`'s submodule |
| `JrGoodle/swift` | Existing personal fork; no destination change selected |

The local patch updates project links, build metadata, website and artifact
scripts, test-repository clone URLs, and initialization expectations. Existing
manifest project names remain aligned with the remotely served files. For
example, `polka-dot-cat/cats` still declares projects as `JrGoodle/mu` and similar
names. A broad owner-name substitution would change assertions before their
input manifests change.

The YAML source-URL tests also use a distinct Beanstalk host,
`polka-dot-cat.git.beanstalkapp.com`. Those references are not GitHub organization
URLs and need a separate access check.

## Deleted fork impact

The initial collection found **97 affected test cases out of 1,110**, across 16 scenario
definitions. Counts include expanded outline rows and fixture parameters, not
just files containing a repository name.

| Coverage | Cases | Purpose |
| --- | ---: | --- |
| `config.feature` | 12 | HTTPS/SSH protocol configuration and origin/upstream URLs |
| `herd.feature` | 25 | Default and overridden protocols; remote URLs; branch behind upstream |
| `forall.feature` | 3 | Project/upstream environment variables and script failure handling |
| YAML upstream validation | 57 | Explicit/inherited remote names and source protocols |
| **Total** | **97** | 40 command cases plus 57 YAML-validation cases |

By repository, the overlapping counts are `djinni`: 69, `gyp`: 68, and `sox`: 40.
All 40 miscellaneous command cases initialize or herd the same three-project
manifest, so they depend on all three forks even when a row asserts only one
project. Of the 97 cases, 75 carry the `ssh` marker and 22 do not.

The count came from pytest collection plus each case's selected YAML fixture
and miscellaneous manifest. Before the changes, one HTTPS herd case reproduced
Git's "Repository not found" error while cloning `JrGoodle/djinni`. After the
manifest and assertion updates, all 97 cases were executed and passed. Legacy
shell tests and documentation examples are excluded from this count. Normal
application use does not require these repositories.

### Selected replacement strategy

**Completed: recreated organization-owned copies from the original upstream
histories.** This preserves the existing test goals and limits the amount of
fixture redesign during the ownership move.

| Repository | Source and required state |
| --- | --- |
| `polka-dot-cat/djinni` | Native GitHub fork of [dropbox/djinni](https://github.com/dropbox/djinni). Both source branches match; no tags were advertised. The archived upstream remains separate from the writable fork. |
| `polka-dot-cat/gyp` | Imported all three branches from [Chromium's GYP repository](https://chromium.googlesource.com/external/gyp/); no tags were advertised. Created `fork-branch` at [bd11dd1c51ef17592384df927c47023071639f96](https://github.com/polka-dot-cat/gyp/commit/bd11dd1c51ef17592384df927c47023071639f96). |
| `polka-dot-cat/sox` | Imported both branches and all 31 tags from [the SourceForge SoX Git repository](https://sourceforge.net/p/sox/code/ci/master/tree/). The SourceForge HTTPS upstream remains separate. |

GYP and SoX are Git imports into new GitHub repositories, since their sources are
hosted outside GitHub; they do not have GitHub fork-network relationships. All
imported branch and tag object IDs match their source snapshots. The new GYP
branch is 23 commits behind upstream `master` at verification time.

A fresh clone of GYP's `fork-branch` successfully ran
`git pull --ff-only upstream master`, reached
`1615ec326858f8c2bd8f30b3a86ea71830409ce4`, and remained on `fork-branch` with a clean
working tree. This check changed only the local verification clone. The GitHub
branch still points to `bd11dd1c51ef17592384df927c47023071639f96`.

Source clones, push logs, ref comparisons, and the fast-forward check are saved
under `fixture-restoration-71mfcsze/` in the backup directory above. The new
repository IDs are `1431752815` (Djinni), `1431753424` (GYP), and `1431753437` (SoX).

### Published manifest changes

- [misc-clowder-tests: `58472a5`](https://github.com/polka-dot-cat/misc-clowder-tests/commit/58472a5ae97ef5a4a1a33622132341439c4c028c)
  updates the root `clowder.yaml` and the `defaults` and `https` saved versions.
- [clowder-examples: `0a4714b`](https://github.com/polka-dot-cat/clowder-examples/commit/0a4714bdecbfb1fb9175cf870b490d607b964ddb)
  updates the three restored-fork names in `versions/upstreams-2.clowder.yml`.
- [misc-clowder-tests: `431c87e`](https://github.com/polka-dot-cat/misc-clowder-tests/commit/431c87ebcc8dfcef35007d4cab724ea973377f51)
  explicitly selects Chromium for GYP's upstream in the saved `defaults` version.

These commits were pushed to `master` and verified against GitHub's advertised
refs. The local Clowder changes update 45 YAML fixtures, four feature files, the
upstream environment-variable script, and the upstream example guide. The test
README now records the dependencies, GYP branch requirement, and commands to run
the 98 cases, including the new regression. These Clowder changes are included in
the local migration checkpoint on `codex-cleanup`.

Validation first used the prepared `misc-clowder-tests` commit through a Git URL
override scoped to the test process. Clones of Djinni, GYP, SoX, and their
upstreams used their actual hosting services. Each `misc-clowder-tests` commit
was tested before publication. The pushes preserved history and existing tags.

A fresh-clone check exposed an existing error in the saved `defaults` version:
GYP's upstream fell back to the GitHub source, so it tried to fetch
`https://github.com/external/gyp.git`. The project-level source default does not
set the upstream's source. Commit `431c87e` makes that source explicit. The new
`herd saved defaults with explicit upstream sources` scenario verifies all three
origin/upstream URL pairs and GYP's starting branch and commit.

The working clones, original local files, test logs, and publication records are
saved under `fixture-migration-acvglxfc/` in the backup directory above. The
three restored test repositories still have the same branch and tag IDs as their
post-creation inventory; GYP's remote `fork-branch` remains at the required commit.

**Alternative: small purpose-built Git fixtures.** Use a shared ancestor, an
upstream branch with later commits, and a fork branch behind it. This provides
controlled remote names, protocols, and branch state with less data and fewer
external dependencies. Local bare repositories can cover most behavior; retain
small network integration tests for GitHub SSH/HTTPS and mixed hosting services.
This is the better long-term test design, but requires fixture and assertion
changes beyond restoring the existing examples. Replacing all three with random
public repositories would retain the availability risk and could lose coverage
of mixed hosts or branch history.

## Validation

Python 3.8.16 and Pipenv were unavailable. Validation used the installed Python
3.10.11, within the declared supported range, in an isolated environment outside
the checkout. Dependencies came from `requirements.txt`; the environment also
used `setuptools==67.8.0` and `wheel==0.40.0` for editable installation. Repository
interpreter and dependency pins were unchanged.

- Editable installation and `python -m clowder.app --help`: passed.
- Empty-directory help selection: **18 passed**.
- HTTPS initialization selection, excluding SSH/offline/write/help/subdirectory
  cases: **10 passed**.
- Test collection: **1,110 cases**, without executing fixtures.
- Before restoration: **one expected failure**, at the missing `djinni` clone.
- After manifest migration: **97 passed**, covering all 40 miscellaneous command
  cases and 57 affected upstream YAML cases, including HTTPS and SSH. The initial
  smoke case passed in 8.78 seconds; the other 96 passed in 576.46 seconds.
- Saved-defaults source regression: **one additional case passed** in 9.27 seconds,
  bringing the relevant selection to **98 passing cases**.
- Fresh-clone verification of published commit `431c87e`: the saved `defaults`
  manifest herded all three projects successfully with the expected origin and
  upstream URLs, clean working trees, and the required GYP branch and commit.
- All 49 changed YAML manifests across the three repositories passed JSON Schema
  validation; the changed environment-variable script passed `bash -n`.
- Changed Python files parse, changed shell scripts pass `bash -n`, local
  documentation links resolve, and `git diff --check` passes.
- Sphinx HTML build: the latest incremental build completed with **41 warnings**;
  the earlier full build had 42. These include stale API imports, existing
  configuration problems, and pages outside the toctree (including these two
  transfer documents). Documentation cleanup remains in the existing backlog.

No tests that disable host networking or modify remote branches were run. These
checks do not establish a full CI baseline. GitHub returned no Actions runs or
check runs in the queried baseline; the combined commit status had no component
statuses. Existing required checks must still be reviewed.

## Remaining transfer steps

1. Coordinate the remaining Cats/Felidae project-name changes and submodule URLs.
   Check `ash` and Beanstalk dependencies while inventorying submodules and hosts.
2. Inspect the organization's Actions policy. The current CLI token received
   HTTP 403 when reading it; repository-level Actions settings were readable.
3. Check Pages domain ownership in account/organization settings and coordinate
   any verification change with the transfer. `clowder.cat` currently responds
   over HTTPS; Pages serves `gh-pages` from its root with HTTPS enforced. DNS is
   hosted at Hover. No DNS or domain verification changes have been made.
4. Confirm which integrations to retain and their organization access. Active
   webhook hosts include CircleCI, Read the Docs, Code Climate, Requires.io, and
   Slack; Codecov also appears in project configuration. New badge URLs alone do
   not reconnect those services.
5. Transfer the main repository, update local remotes, publish the prepared patch,
   and complete the [plan's completion checks](clowder-repository-transfer-plan.md#completion-checks).
