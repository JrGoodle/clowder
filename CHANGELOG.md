# Changelog

## 4.0

- Support `.yml` and `.yaml` extensions (use `.yml` by default)
- Support `clowder.yml` files that aren't symlinks, and without `.clowder` directory
- Infer default `source` when only one is present
- Commands take groups/projects as positional arguments
- Use last path component of `name` if `path` not specified
- Add official support for Python 3.8
- Versions are now stored as named yaml files in the `versions` directory rather than in subdirectories
- Add `clowder config` experimental command
- Add `git herd` alias in projects
- Allow clowder to be called from subdirectories

- Replace Travis CI tests with GitHub Action workflow tests
- Remove imported `clowder.yaml` files
- Remove `sync` command
- Remove `--groups/-g` command option
- Remove `--skip/-s` command option

- Schema changes:
  - `groups` is now an array of strrings in a project, rather than a top level item
  - Add `protocol` option to `source`
  - Add `source` option to `fork`
  - Add `git.config` to `defaults` and `projects`
  - Add `git.rebase` to `defaults` and `projects`
  - Add `git.protocol` to `defaults` and `projects`
  - Add `git.lfs` to `defaults` and `projects`
  - Change `--parallel` to `--jobs` for parallel commands

## [3.2.0](https://github.com/JrGoodle/clowder/releases/tag/3.2.0)

- Fix an issue causing commands to hang on Python 3.8

## [3.1.0](https://github.com/JrGoodle/clowder/releases/tag/3.1.0)

- Drop support for Python 2
- Update for Cement 3
- Prevent `clowder branch` from entering interactive mode
- Remove cocos2d example
- Update Travis CI and Circle CI builds

## [3.0.0](https://github.com/JrGoodle/clowder/releases/tag/3.0.0)

- Migrate to Cement for CLI logic
- Add ability to create plug-ins via Cement
- Add separate `clowder.yaml` parameter for git protocol
- Add test coverage
- Add AppVeyor support for Windows testing
- Add Circle CI support for write tests

## [2.5.0](https://github.com/JrGoodle/clowder/releases/tag/2.5.0)

- Add `clowder checkout` command
- Add Sphinx documentation and update docstrings
- Disallow saving a version named "default"
- Add `--skip/-s` option to various commands
- Add ability to reset projects based on timestamp with `clowder reset --timestamp`
- Add `--parallel` option to `clowder herd`, `clowder sync`, `clowder reset`, and `clowder forall`
- Add more badges and setup code climate
- Various refactoring to reduce number of issues on code climate
- Tweak output formatting for refs

## [2.4.0](https://github.com/JrGoodle/clowder/releases/tag/2.4.0)

- Add `clowder reset` command
- Add `-t`/`--tag` option to `clowder herd`
- Refactor exception handling
- Add support for Python 2
- Add `-r`/`--rebase` option to `clowder herd`
- Add `clowder-test` test script runner for more easily running various tests

## [2.3.0](https://github.com/JrGoodle/clowder/releases/tag/2.3.0)

- Add more options to `clowder clean` (`-f`, `-x`, `-X`, `-d`, `-r`, `-a`)
- More thorough cleaning logic
- Add the ability to override project forks in imported `clowder.yaml` files
- Add `clowder yaml` command to print `clowder.yaml` information
- Add offline support
- Update documentation to use Swift as the example
- Add additonal options to `group`s in `clowder.yaml`
- Add `clowder branch` command
- Add `clowder sync` command
- Better handling of `fork`s
- Fix bug in display of new commits in project status

## [2.2.0](https://github.com/JrGoodle/clowder/releases/tag/2.2.0)

- Add `-b` option to `clowder herd`
- Add environment variables available in `clowder forall` scripts and commands
- Fix handling of edge cases in `clowder herd`
- Fix bugs in `clowder.yaml` import logic
- Show diffs when command fails with dirty repos
- Tweak output formatting
- More complete test coverage
- Update documentation

## [2.1.0](https://github.com/JrGoodle/clowder/releases/tag/2.1.0)

- Add ability to import another `clowder.yaml` file and override values
- Add `clowder diff` command to display git diff status. Replaces previous `clowder status -v` command option
- Add `clowder start -t` option to create remote tracking branches
- Add `clowder prune -r` option to prune remote branches
- Add `clowder prune -a` option to prune local and remote branches
- Less noise in output when pruning branches
- Better validation of `clowder.yaml` files
- Better help messages

## [2.0.0](https://github.com/JrGoodle/clowder/releases/tag/2.0.0)

- Add support for uploading to PyPI as [clowder-repo](https://pypi.python.org/pypi/clowder-repo)
- Add ability to run scripts with `clowder forall`
- Print number of new local and upstream commits in output
- Add `-f` option to `clowder status` to fetch before printing status
- Add `--ignore-errors`/`-i` option to `clowder forall`
- Remove `-f` option from `clowder forall`
- Remove `-b` option from `clowder herd` (may be added back in the future)
- Add `-f` option to `clowder prune` to force delete branches

## [1.1.2](https://github.com/JrGoodle/clowder/releases/tag/1.1.2)

- Remove cat face emoji from command output for better portability.

## [1.1.1](https://github.com/JrGoodle/clowder/releases/tag/1.1.1)

- Fix bug with missing directories when running `clowder forall`.
- Fix bugs in git utilities.

## [1.1.0](https://github.com/JrGoodle/clowder/releases/tag/1.1.0)

- Add `clowder link` command to change `clowder.yaml` symlink location. Remove `--version` option from `clowder herd`.

## [1.0.1](https://github.com/JrGoodle/clowder/releases/tag/1.0.1)

- Change `clowder herd` to accept version and branch parameters.

## [1.0.0](https://github.com/JrGoodle/clowder/releases/tag/1.0.0)

- Add depth (`-d`) option to `clowder herd`.
- Add branch (`-b`) option to `clowder herd`.
- Add projects (`-p`) option to `clowder status`.
- Update command output formatting.

## [0.11.0](https://github.com/JrGoodle/clowder/releases/tag/0.11.0)

- Add various `clowder repo` subcommands:
  - `clowder repo pull`
  - `clowder repo push`
  - `clowder repo add`
  - `clowder repo commit`
  - `clowder repo status`
  - `clowder repo checkout`

## [0.10.0](https://github.com/JrGoodle/clowder/releases/tag/0.10.0)

- Add `depth` support to `clowder.yaml`.
- Better support for forks in `clowder.yaml`.
- Better validation of `clowder.yaml` file.
- Add `clowder prune` command.
- Add `clowder start` command.
- Add branch (`-b`) option to `clowder init`.
- Add `clowder -v` option to print version.
- More detailed git operation output.
- Rename commands:
  - `fix` -> `save`
  - `breed` -> `init`
  - `groom` -> `clean`
  - `meow` -> `status`

## [0.9.0](https://github.com/JrGoodle/clowder/releases/tag/0.9.0)

- Updated command output formatting.
- Remove directories when cloning fails.

## [0.8.3](https://github.com/JrGoodle/clowder/releases/tag/0.8.3)

- Updated `clowder forall` command output.
- Add `clowder repo` command.

## [0.8.2](https://github.com/JrGoodle/clowder/releases/tag/0.8.2)

- Updated command output formatting.

## [0.8.1](https://github.com/JrGoodle/clowder/releases/tag/0.8.1)

- Fix bug in `clowder.yaml` symlink creation.
