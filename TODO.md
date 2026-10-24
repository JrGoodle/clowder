# TODO

Initial backlog from repository review on 2026-10-15, at commit `1438fc8b`.
Priorities below are proposed. Findings come from source and configuration
inspection; application behavior and CI were not tested. The pinned Python
3.8.16 is not installed here, and this checkout has no Pipenv environment.

Check an item off only after its completion criteria are met. Add regression
coverage for behavior fixes. Abstract methods and pytest-bdd scenario bodies that
contain `pass` are not automatically missing implementations.

## Before the backlog: transfer the repository

Follow the [transfer plan](docs/clowder-repository-transfer-plan.md) and
[progress record](docs/clowder-repository-transfer-status.md). The checks below
are separate from the initial review and were updated on 2026-10-23.

- [x] Save the Clowder Git mirror, LFS objects, release assets, and settings inventory.
- [x] Transfer `felidae` to `polka-dot-cat` and verify its ID, branches, tags, and redirect.
- [x] Prepare canonical clone URLs and post-transfer project links locally.
- [x] Validate the preparation with CLI help and 28 focused test cases.
- [x] Count the impact of the deleted forks: 97 collected cases depend on them;
  reproduce a missing-repository failure without remote writes.
- [x] Provision `polka-dot-cat/djinni`, `gyp`, and `sox` from their original
  upstreams; set GYP's `fork-branch` to
  `bd11dd1c51ef17592384df927c47023071639f96` and verify its upstream fast-forward.
- [x] Publish the restored-fork names in `misc-clowder-tests` and
  `clowder-examples`; update local Clowder fixtures and assertions. All 97 affected
  cases plus a new saved-defaults regression pass, including HTTPS and SSH coverage.
- [x] Transfer `ash` and publish canonical submodule URLs in Ash, Mu, and Felidae;
  verify recursive clones and preserve tags and unrelated refs.
- [x] Stage the remaining Cats and clowder-examples manifest names on migration
  branches and prepare their matching Clowder assertions in draft PR #641.
- [ ] At PR #641's merge, fast-forward the active manifest branches to the
  [recorded commits](docs/clowder-repository-transfer-status.md#cats-and-felidae-migration)
  and verify the tests against the published fixtures. Keep the old names until merge.
- [ ] Verify Beanstalk's server host key, then check SSH access and run the 28
  explicit source-URL cases. Retain Beanstalk; the owner confirmed the account
  public key is already registered and chose to leave host verification pending.
- [ ] Finish validating the repaired Actions baseline; see the
  [preflight record](docs/clowder-transfer-preflight.md) for the matrix and run.
  Both Ubuntu jobs now pass all 684 cases, including LFS. The collection fix is
  published and the job limit is raised to 60 minutes after a macOS timeout;
  verify the complete macOS matrix on the updated branch.
- [x] Check Actions repository eligibility and effective permissions on existing
  organization repositories; confirm Pages has no verified domain on either account.
- [x] Inventory service failures and disable the obsolete Requires.io webhook
  with the owner's approval; remove its documentation badge.
- [x] Disable the Read the Docs webhook and remove its build badges at the owner's
  request. Retain the project and build configuration for later reactivation.
- [x] Restore CircleCI's GitHub configuration-fetch authorization. Pipeline `1578`
  loads the configuration and publishes the required status after the owner signed in.
- [x] Restore CircleCI's checkout/deploy key. The owner recreated it; GitHub
  confirms read-only deploy key `167499686`, titled `CircleCI`.
- [ ] Verify the repaired `test_write` job. Job `2968` passed checkout and setup,
  then hit a retired Code Climate reporter download. The active job now runs all
  89 cases directly against the staged Cats manifests and retains coverage artifacts.
- [ ] Confirm retained CircleCI access to `polka-dot-cat` and review Qlty/Codecov
  access or retention. CircleCI's `test_write` check is still required.
- [ ] During transfer, update the `www.clowder.cat` CNAME to
  `polka-dot-cat.github.io`; verify the domain under the organization afterward.
- [ ] Transfer `clowder`, update local remotes, publish the migration changes, and
  complete the transfer plan's verification checklist.

## First: establish a repeatable development baseline

- [ ] **Align Python support and dependency setup.** `.python-version` and Pipenv
  select 3.8.16; `setup.py` lists 3.8–3.11; GitHub Actions selects 3.8/3.11;
  Docker selects 3.8.5; Read the Docs now selects 3.11; AppVeyor selects 3.6–3.8.
  Choose the supported range, add package `python_requires`, and align these
  files. Verify installation, CLI help, and test collection in a fresh environment.
  Preserve the `pytest-bdd==4.0.2` constraint until migration is tested, and check
  uses of `pkg_resources` and `trio.MultiError` when updating dependencies.

- [ ] **Make the test setup independent of personal infrastructure.**
  [Test utilities](tests/functional/util/clowder.py) clone named external repos
  and can delete remote `pytest*` branches during SSH setup.
  [Network steps](tests/functional/when/when.py) disable host networking.
  LFS scenarios can change global/system hooks and filters.
  Add local bare-repository fixtures and simulated connection failures where
  possible; isolate the remaining integration tests. Document a test selection
  that needs neither credentials nor changes to host networking or remote repos.

- [ ] **Establish and record a CI baseline.** In
  [.circleci/config.yml](.circleci/config.yml), only `test_write` is enabled in
  the workflow; offline, parallel, and combined coverage jobs are commented out.
  [GitHub Actions](.github/workflows/ci-pytest.yml) excludes SSH/offline tests and
  uses older action versions. Update and validate the retained jobs, restore or
  explicitly retire disabled coverage, and record results for the chosen platform
  matrix. Fix or retire [AppVeyor](appveyor.yml), which uses an incomplete
  `pip3 install -e` command and an absent `examples/cats` directory.

## Next: fix incomplete or inconsistent behavior

- [ ] **Complete submodule cleanup and update handling.**
  [CleanCommand](clowder/cli/clean.py) accepts `--recursive` but does not pass it
  on. [ProjectRepo.clean](clowder/controller/project_repo.py) changes the parent
  repository before raising `NotImplementedError` for `submodules=True`.
  `ProjectRepo.herd` only calls `submodule_update` when `recursive` is true, while
  [resolved settings](clowder/controller/resolved_git_settings.py) distinguish
  `submodules: true` from `submodules: recursive`. Define and test nonrecursive
  and recursive behavior with nested local submodules, including error paths.

- [ ] **Reconcile existing remotes during herd.** The `configure_remotes`
  decorator in [project_repo.py](clowder/controller/project_repo.py) is a no-op,
  and `Remote._compare_remote_url` in [remote.py](clowder/util/git/model/remote.py)
  is commented out. Herd creates missing remotes but does not resolve the cases
  described by these TODOs. Define behavior for a renamed remote, a matching name
  with a different URL, and project/upstream collisions; add local-repo tests.

- [ ] **Handle manifest symlinks outside the workspace in status output.**
  [ClowderRepo.status](clowder/controller/clowder_repo.py) calls `relative_to`
  on the resolved target without handling an external target, as its FIXME notes.
  Display a valid path or a clear error. Cover internal, external, broken, and
  ambiguous `.yml`/`.yaml` links without an unhandled traceback.

- [ ] **Validate configured projects against actual project/group choices.**
  [Config.__init__](clowder/config.py) passes `self.projects` into
  `_validate_config_projects_defined`, which then checks the same values against
  themselves. Validate against resolved manifest choices and report all unknown
  entries. Cover valid groups, unknown names, and cleared settings in
  [config.feature](tests/features/config.feature).

- [ ] **Remove duplicate exception definitions.**
  [error.py](clowder/util/error.py) defines `ExistingFileError`,
  `ExistingSymlinkError`, `MissingFileError`, and `UnknownArgumentError` twice.
  The later definitions replace the versions derived from `ClowderError`.
  Confirm the intended hierarchy, keep one definition of each, and verify CLI
  error handling and relevant catches.

- [ ] **Define and test saved-version names.**
  [SaveCommand](clowder/cli/save.py) lowercases names and replaces `/` with `-`,
  but still has a validation TODO. Specify allowed names and collision handling,
  then validate before creating files. Preserve or explicitly document the
  slash-to-dash behavior covered by [save.feature](tests/features/save.feature).

## Strengthen regression coverage

- [ ] **Replace placeholder output checks with assertions.**
  `then_command_printed_branch_type` in [output.py](tests/functional/then/output.py)
  contains only `pass`. Status and diff scenarios also contain commented output
  checks. Add active scenarios that assert local/remote branch lists, dirty state,
  and diff output after stripping terminal escapes. Verify the assertions fail
  for incorrect output.

- [ ] **Cover parallel execution and unfinished herd cases.**
  [herd.feature](tests/features/herd.feature),
  [forall.feature](tests/features/forall.feature), and
  [reset.feature](tests/features/reset.feature) request parallel tests.
  Herd also has disabled cases for ref state and tags. Prioritize equivalent
  results for one and multiple jobs, failure propagation, dirty-worktree checks,
  detached HEAD, and annotated/lightweight tags using controlled local fixtures.

## Maintain documentation and release tooling

- [ ] **Repair the documentation build and API pages.**
  [script/docs](script/docs) reads `$1` with `set -u`, so a no-argument call can
  fail after the build. Use an optional argument safely and verify both build and
  preview modes. Regenerate API stubs and remove obsolete references to
  `clowder.data`, `clowder.git_project`, and former top-level controller modules
  in [docs/rst](docs/rst/). Build the docs and resolve stale import/link warnings.

- [ ] **Update contributor and installation guidance.**
  [CONTRIBUTING.md](CONTRIBUTING.md) directs users through `script/update` and
  a package-directory `PYTHONPATH`; [README.md](README.md) uses `sudo pip`.
  After the setup baseline is verified, document an isolated editable install,
  interpreter selection, test markers and side effects, and the current
  INI-style config. Check examples against CLI help and the schema; clarify
  historical docs such as `clowder-yml-syntax-reference-old.md`.

- [ ] **Restore release preconditions and package checks.**
  [script/deploy](script/deploy) has disabled branch/clean-tree assertions and
  a TODO to load release notes. Restore appropriate checks and separate package
  validation from publication. Build a wheel and source archive; verify the CLI
  entry point, bundled schema, and metadata in a fresh install. Use
  [CHANGELOG.md](CHANGELOG.md) for release notes, and test failure paths without
  creating releases or uploading packages.
