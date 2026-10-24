# Transfer preflight: Actions, Pages, and integrations

Checked October 23, 2026 (America/Chicago). The main repository is still
`JrGoodle/clowder`, and [PR #641](https://github.com/JrGoodle/clowder/pull/641)
remains a draft. This record supplements the
[transfer plan](clowder-repository-transfer-plan.md) and
[fixture migration status](clowder-repository-transfer-status.md).

The source repository ID is `38194118`, with public visibility and default
branch `master`. Repository admin access and active organization-owner membership
were confirmed. The destination name `polka-dot-cat/clowder` was still unused.
Recheck availability immediately before the transfer.

## GitHub Actions

The owner confirmed that `polka-dot-cat` enables Actions for all repositories.
The repository-level APIs for `polka-dot-cat/ash` and `polka-dot-cat/cats` both
report Actions enabled, all actions allowed, and no required SHA pinning. Ash's
workflow-token default is write access with PR-review approval enabled. The CLI
cannot read the organization-wide policy directly because its token lacks
`admin:org`; these findings distinguish owner confirmation from API evidence.

The Clowder workflow now explicitly requests only `contents: read` and uses
commit-pinned releases of GitHub's checkout, setup-python, and upload-artifact
actions. It retains the four existing required check names:

- `pytest (ubuntu-latest, 3.8)`
- `pytest (ubuntu-latest, 3.11)`
- `pytest (macos-latest, 3.8)`
- `pytest (macos-latest, 3.11)`

Those check labels now select `ubuntu-24.04` and `macos-15-intel`. Python 3.8's
available macOS distribution requires Intel, and the moving Ubuntu label is
transitioning to Ubuntu 26. The declared Python matrix remains 3.8/3.11.
GitHub documents the available [runner images](https://github.com/actions/runner-images)
and [Python distributions](https://github.com/actions/python-versions).

The workflow uses the selected Python directly and installs the pinned project
requirements. Build tools are constrained to the versions used for local
migration validation. It no longer removes a system Python executable or uses
the local bootstrap scripts to change the runner's selected interpreter.

Each matrix job separates the test groups:

| Group | Collected cases | Execution |
| --- | ---: | --- |
| Initialization | 14 | Published GitHub URLs, four workers |
| Functional | 667 | Staged Cats manifests, four workers |
| LFS | 3 | Staged Cats manifests, serial on the disposable runner |

SSH, offline, and remote-write cases remain excluded from Actions. The LFS group
runs after the parallel groups because its steps change global/system LFS
configuration. Cucumber, JUnit, and coverage files are uploaded even when tests
fail. The old annotation actions were removed; reports remain available as
artifacts without granting the test workflow write access to GitHub checks.

The workflow pins the already-published Cats migration commits and uses a
process-scoped local Git URL override for the functional/LFS groups. The
initialization group uses the live URL because it asserts that URL. Remove the
temporary fixture preparation and overrides after the active manifests have
completed their coordinated cutover; until then, ordinary published Cats names
remain compatible with existing Clowder versions.

Validation so far:

- Actionlint and shell checks pass. Collection checks confirm that the three
  groups retain all 684 cases from the previous Actions selection.
- A local smoke run passed 14 initialization cases and eight representative
  functional cases, with coverage, JUnit, and Cucumber reports.
- In [run 40061606195](https://github.com/JrGoodle/clowder/actions/runs/40061606195),
  both Ubuntu/Python 3.8 and Ubuntu/Python 3.11 passed all 14 initialization and
  667 functional cases. The Ubuntu/Python 3.11 Sphinx build also passed.
- Both Ubuntu LFS phases stopped during collection because pytest also searched
  the GYP repositories cloned by the earlier functional group. Follow-up commit
  `b9993e50` explicitly restricts each invocation to `tests/functional`.
- All three LFS cases passed with that fix in a disposable Docker container
  using Python 3.11 and the pinned requirements. No host Git configuration was
  mounted into the container; its system/global LFS changes were isolated.
- In that same run, macOS/Python 3.8 passed all 681 initialization and functional
  cases, then reached the same GYP collection error. The macOS/Python 3.11 job
  exceeded the 30-minute limit during functional tests. The workflow now allows
  60 minutes per job to accommodate the longer macOS runs.
- With the collection fix, both Ubuntu jobs in
  [run 40063001549](https://github.com/JrGoodle/clowder/actions/runs/40063001549)
  succeeded, including their LFS phases. The complete macOS matrix still needs
  confirmation before the Actions baseline can be marked complete.

The first repaired run also exposed a missing parent temporary directory; that
setup error and the collection fix are now published on the draft PR branch.

## Pages and DNS

The owner confirmed that neither the personal account nor `polka-dot-cat` has
any verified Pages domains. There is no existing verification claim to migrate.
The repository's Pages API reports:

- Source: `gh-pages`, directory `/`, legacy branch build.
- Custom domain: `clowder.cat`; public site; HTTPS enforced.
- Certificate: approved for `clowder.cat` and `www.clowder.cat`, expires
  January 21, 2027.
- `https://clowder.cat` returns HTTP 200.

DNS is hosted by Hover (`ns1.hover.com`, `ns2.hover.com`). The apex uses GitHub's
four IPv4 addresses, and no AAAA record was returned. The `www` CNAME still points
to the personal Pages hostname.

| Record | Current value | Action at transfer |
| --- | --- | --- |
| `clowder.cat` A | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` | Retain |
| `www.clowder.cat` CNAME | `jrgoodle.github.io` | Change to `polka-dot-cat.github.io` |

Keep the custom domain and branch source during the repository transfer, then
update the `www` CNAME and verify both hostnames over HTTPS. After the repository
belongs to the organization, add and verify `clowder.cat` in the organization's
Pages settings, using the TXT value GitHub supplies. Do not verify it there
before transfer: verification can release the domain from a site owned by
another account. See [GitHub's domain-verification rules](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

No DNS, Pages source, domain, certificate, or domain-verification setting was
changed during this preflight.

## Integration findings

| Service | Evidence | Remaining action |
| --- | --- | --- |
| Read the Docs | Project `clowder`, ID `154942`, still points to `https://github.com/JrGoodle/clowder.git`. Last recorded build failed July 9, 2023. Its last webhook response was HTTP 400 because no shared secret was configured. | Owner chose to disable it for now. Hook `17286177` is disabled and verified; build badges are removed. The hosted project and build configuration are retained for later reactivation. |
| CircleCI | Project `bb8973a7-cc5b-4870-affe-eb39676286fb` still belongs to `JrGoodle`. After the owner signed in, pipeline `1578` loaded the configuration and started `test_write`. Job `2967` failed checkout with `Permission denied (publickey)`. The owner then recreated its deploy key; GitHub confirms key `167499686`, titled `CircleCI`, with read-only access. | Owner chose to retain it. Verify the job with the restored key and confirm organization access before transfer. `ci/circleci: test_write` remains required by branch protection. |
| Code Climate / Qlty | The old project URL redirects to Qlty's login for the personal-account project. The legacy webhook returns HTTP 200, which does not establish successful analysis. | Review the project and organization access in Qlty; do not treat a badge URL change as a completed migration. |
| Codecov | Public API reports the personal-account project as inactive and not activated; its last update is January 30, 2024. The CircleCI coverage-upload workflow is commented out. | Decide whether to reactivate reporting after transfer; no active upload was established. |
| Slack | Existing webhook is active and its last recorded response is HTTP 200. | Retain its configuration through transfer. No test message was sent. |
| Requires.io | Last delivery was HTTP 405, and the domain now redirects to a sale page. | Owner authorized disabling hook `17286562`. It is disabled, verified, and its obsolete documentation badge is removed in the draft. |

If Read the Docs is reactivated later, update its repository URL and use project
Settings → Integrations → GitHub → **Resync webhook**. Configure the generated
shared secret in the provider webhook as directed, then re-enable delivery and
verify a build. Do not put the secret in this repository or chat.
[Read the Docs webhook update](https://blog.readthedocs.com/security-update-on-incoming-webhooks/)

The draft also repairs `.readthedocs.yml`: it now declares Ubuntu 24.04 and
Python 3.11 under `build`, uses the existing pinned requirements, and pins the
build tools needed by the old package setup. The Actions Ubuntu/Python 3.11 job
builds the same Sphinx documentation. A hosted Read the Docs build is deferred.

CircleCI's configuration-fetch authorization is now restored. A fresh push of
`b4a8015e` created pipeline `1578` without the earlier follower-token error and
published the required GitHub status. [Job 2967](https://circleci.com/gh/JrGoodle/clowder/2967)
failed before tests because its checkout SSH key was rejected; GitHub listed no
deploy keys at that time. The owner recreated the repository checkout/deploy key
through CircleCI. GitHub confirms read-only key `167499686`, created at
`2026-10-24T04:53:21Z`. The separate Additional SSH Keys were left unchanged.
The checkout-key API requires CircleCI authentication and returned HTTP 403 in
this session. Validate the job and confirm `polka-dot-cat` access before transfer.
See [CircleCI's checkout-key API](https://circleci.com/docs/api/v2/#tag/Project/operation/createCheckoutKey).

Branch protection still requires CircleCI's `test_write` status in addition to
the four Actions statuses. Protection and collaborator settings are unchanged.
The owner restored CircleCI authentication and its checkout key; Requires.io and
Read the Docs webhooks were disabled with approval. No browser
connection is available in this session, so account-side service access must be
confirmed separately before treating the transfer preflight as complete.

## Evidence

Redacted inventories, owner confirmations, DNS observations, workflow metadata,
test reports, and service responses are saved outside the repository under
`../clowder-transfer-backups/20261024T023608Z/service-preflight-uds_8n9d/`.
Webhook secrets and full webhook URLs were not copied into this record.
