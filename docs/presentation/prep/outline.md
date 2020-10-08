# Clowder

## TODO:

- [ ] Update README so gifs match schema in examples
- [ ] Update clowder.yml files in clowder-examples repo

## History

- origins
  - submodules
    - At my first job, we had multiple repositories we had to manually keep in sync. These included our own frequently changing libs and less frequently changing third party libs.
    - [A programmer had a version control problem and said, "I know, I'll use submodules." Now they have two problems.](https://codingkilledthecat.wordpress.com/2012/04/28/why-your-company-shouldnt-use-git-submodules/)
  - Google repo
    - Used for managing the many repos making up the AOSP. I got a OnePlus One and built Android from source for it, and learned about repo.
    - Tightly coupled with gerritt and Google's Android workflow.
    - Initially I was just planning on writing some scripts to wrap repo, but the behavior didn't match the documentation.
  - subtrees + subrepo + others
  - [llvm-projects](https://github.com/JrGoodle/llvm-projects)
    - Used to be a multi-repository project
    - [Moved to monorepo in mid 2019](https://releases.llvm.org/9.0.0/docs/Proposals/GitHubMove.html)
- [0.4.1](https://github.com/JrGoodle/clowder/releases/tag/0.4.1)
  - Sep 4, 2015
  - initial file format
  - different concept of groups than repo
- [1.0](https://github.com/JrGoodle/clowder/releases/tag/1.0.0)
  - Jan 23, 2016
  - add forks
  - cli changes
- [2.0](https://github.com/JrGoodle/clowder/releases/tag/2.0.0)
  - Sep 1, 2017
  - cli changes
- [3.0](https://github.com/JrGoodle/clowder/releases/tag/3.0.0)
  - Nov 25, 2017
  - cli changes
  - add imports
  - update source url formation to separate protocol and url (allows overriding)
- [4.0](https://github.com/JrGoodle/clowder/releases/tag/4.0b6)
  - cli changes
    - repo syntax without option arguments (i.e. -g for groups)
  - remove imports
  - new syntax
    - upstream instead of fork
      - better aligns with likely use case of primary project being the fork, and the upstream being special
    - branch/tag/commit vs ref with full name
      - validation made easy by json schema
    - use dicts with keys as names instead of lists with element dicts having name property
      - similar to other yaml config files
      - less text
    - combine previous group concept with repo group concept
      - allows for settings at the group level (i.e. path prefix)
    - better model layer allowing for saving only info specified in clowder.yml

## Benefits/Use Cases

- Document active projects
- Easily clone all relevant repos
- Easily set up forks with upstream remote no matter where hosted
  - More likely to keep up to date if you don't have to hunt down the upstream remote url
- Update submodules automatically
  - Reduce submodule commit battles
- Update lfs automatically
  - Makes sure to always update lfs files and install hooks
- Setup shared git config automatically
- Save snapshots for later restoration
- Easily script multiple repos
  - clowder forall
- Not required, can be used individually or by team
  - this isn't something team would need to move to as an organization. the clowder repo and config can be used by individuals without impacting the rest of the organization

## Possible Drawbacks

- Dependency information isn't stored in project repos.
  - If two repos are tightly coupled, results for updates aren't deterministic. This could lead to more complex CI scripting or local failures.
  - monorepo, submodules, or git subtree would probably be a better solution here

## Usage

- clowder init
- clowder herd
- `git herd` alias
- `clowder herd`
- git config
  - could store script in repo and setup hook
- clowder save
- clowder link

## Design decisions

- protocol
  - Where to specify?
  - How to overrride?
- branch/remote vs git settings
  - Root level of project vs subdictionary
  - support for other vcs's
    - svn
    - mercurial
- git submodule
  - naming/schema
- schema
  - ref vs branch/tag/commit
  - full url vs components
- Adding/removing Cement
  - hooks
  - cli limitations
- cute custom subcommand names vs industry standards

## Features

- schemastore
  - VS Code
- autocompletion
- pytest-bdd
  - examples of shell scripts
  - example of bdd test
- circle ci
  - docker for offline tests
  - better way to test writes?

## Future

- Create clowder from GitHub
- plug-ins
- Custom formatting
