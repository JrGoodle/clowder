# `clowder.yml` Syntax Reference

- [name](#name)

- [defaults](#defaults)
  - [protocol](#defaultsprotocol)
  - [source](#defaultssource)
  - [remote](#defaultsremote)
  - [branch](#defaultsbranch)
  - [tag](#defaultstag)
  - [commit](#defaultscommit)
  - [git](#defaultsgit)
    - [lfs](#defaultsgitlfs)
    - [recursive](#defaultsgitrecursive)
    - [depth](#defaultsgitdepth)
    - [config](#defaultsgitconfig)

- [sources](#sources)
  - [<source_name>](#sourcesname)
    - [url](#sourcesurl)
    - [protocol](#sourcesprotocol)

- [projects](#projects)
  - [name](#projectsname)
  - [source](#projectssource)
  - [branch](#projectsbranch)
  - [tag](#projectstag)
  - [commit](#projectscommit)
  - [path](#projectspath)
  - [remote](#projectsremote)
  - [groups](#projectsgroups)
  - [git](#git)

- [git](#git)
  - [lfs](#gitlfs)
  - [recursive](#gitrecursive)
  - [depth](#gitdepth)
  - [config](#gitconfig)
    - [<config_name>](#gitconfig_name)

- [upstream](#projectsupstream)
  - [name](#projectsupstreamname)
  - [source](#projectsupstreamsource)
  - [remote](#projectsupstreamremote)
  - [branch](#projectsupstreambranch)
  - [tag](#projectsupstreamtag)
  - [commit](#projectsupstreamcommit)

- [clowder](#clowder)
  - [<group_name>](#clowdergroup_name)
    - [path](#clowdergrouppath)
    - [groups](#clowdergroupgroups)
    - [defaults](#defaults)
  - [projects](#clowderprojects)

## `name`

Name to be displayed when running commands.

## `defaults`

Default settings that will apply to all projects or sources. If not specified, clowder assumes the following defaults:

- `remote`: `origin`
- `branch`: `master`
- `protocol`: `ssh`
- `source`: `github`

## `defaults.protocol`

The git protocol to use when cloning repositories. Options are `ssh` and `https`. If not specified, defaults to `ssh`.

See also: [sources.protocol](#sourcesprotocol)

## `defaults.source`

The name of the default source to use when cloning project repositories. If not specified, defaults to `github` (see [sources](#sources)).

See also: [projects.source](#projectssource), [projects.fork.source](#projectsforksource)

## `defaults.remote`

The default name of the git remote.

See also: [projects.remote](#projectsremote), [projects.fork.remote](#projectsforkremote)

## `defaults.branch`

The default name of the branch projects should track. Only one of `branch`, `tag`, or `commit` can be present.

See also: [projects.branch](#projectsbranch), [projects.fork.branch](#projectsforkbranch)

## `defaults.tag`

The default name of the tag projects should track. Only one of `branch`, `tag`, or `commit` can be present.

See also: [projects.tag](#projectstag), [projects.fork.tag](#projectsforktag)

## `defaults.commit`

The default commit projects should track. Must be the full 40-character sha-1. Only one of `branch`, `tag`, or `commit` can be present.

See also: [projects.commit](#projectscommit), [projects.fork.commit](#projectsforkcommit)

## `defaults.git`

Default git configuration.

See also: [projects.git](#projectsgit)

## `defaults.git.lfs`

Setting this value to `true` will install git lfs hooks and pull lfs files when `clowder herd` is run.

See also: [projects.git.lfs](#projectsgitlfs)

## `defaults.git.recursive`

Setting this value to `true` will recursively init and update submodules when `clowder herd` is run.

See also: [projects.git.recursive](#projectsgitrecursive)

## `defaults.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned.

See also: [projects.git.depth](#projectsgitdepth)

## `defaults.git.config`

A map of git config values to install in projects. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. Git config values from defaults will be combined with those in [projects.git.confg](#projectsgitconfig). If the same keys are present, the project value will take priority. To prevent a default git config value from being inherited by a project, it must be set to `null` in [projects.git.config](#projectsgitconfig).

See also: [projects.git.config](#projectsgitconfig)

## `sources`

List of git hosting services. The following sources are defined by default:

- `github`: `github.com`
- `gitlab`: `gitlab.com`
- `bitbucket`: `bitbucket.org`

## `sources.name`

The name used to identify the source.

See also: [defaults.source](#defaultssource), [projects.source](#projectssource), [projects.fork.source](#projectsforkremote)

## `sources.url`

The Git URL prefix for all projects that use this source. This is combined with the protocol (see: [defaults.protocol](#defaultsprotocol) [sources.protocol](#sourcesprotocol)) and [projects.name](#projectsname) to form the full url for cloning the repository:

- `git@${sources.url}:${projects.name}.git`
- `https://${sources.url}/${projects.name}.git`

## `sources.protocol`

The Git URL protocol prefix for all projects which use this source. Accepted values are `ssh` and `https`. This is combined with with [sources.url](#sourcesurl) and [projects.name](#projectsname) to form the full url for cloning the repository:

- `git@${sources.url}:${projects.name}.git`
- `https://${sources.url}/${projects.name}.git`

See also: [defaults.protocol](#defaultsprotocol)

## `projects`

List of projects.

## `projects.name`

The project's name is appended onto its source's URL to generate the actual URL to configure the Git remote with. This is combined with the protocol (see: [defaults.protocol](#defaultsprotocol) [sources.protocol](#sourcesprotocol)) and [sources.url](#sourcesurl) to form the full url for cloning the repository:

- `git@${sources.url}:${projects.name}.git`
- `https://${sources.url}/${projects.name}.git`

## `projects.source`

Source to use for forming git clone url.

See also: [defaults.source](#defaultssource), [sources.name](#sourcesname)

## `projects.branch`

Name of the Git branch to track for this project. Only one of `branch`, `tag`, or `commit` can be present.

See also: [defaults.branch](#defaultsbranch)

## `projects.tag`

Name of the Git tag to track for this project. Only one of `tag`, `tag`, or `commit` can be present.

See also: [defaults.tag](#defaultstag)

## `projects.commit`

Commit the project should track. Must be full 40 character SHA-1. Only one of `commit`, `tag`, or `commit` can be present.

See also: [defaults.commit](#defaultscommit)

## `projects.path`

Relative path to clone git repository. If not present, then the last path component of [projects.name](#projectsname) will be used as the git clone path.

## `projects.remote`

The git remote name.

See also: [defaults.remote](#defaultsremote)

## `projects.groups`

Projects can specify custom groups in order to run commands for certain sets of projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present, then the project will not be included in commands unless another group argument is given that it belongs to. The values of `all` and `default` are reserved and not allowed to be specified in this list.

## `projects.git`

Project git configuration.

See also: [defaults.git](#defaultsgit)

## `projects.git.lfs`

Setting this value to `true` will install git lfs hooks and pull lfs files when `clowder herd` is run.

See also: [defaults.git.lfs](#defaultsgitlfs)

## `projects.git.recursive`

Setting this value to `true` will recursively init and update submodules when `clowder herd` is run.

See also: [defaults.git.recursive](#defaultsgitrecursive)

## `projects.git.depth`

The default depth git will clone to. Must be a positive integer. If set to `0` the full repository history will be cloned.

See also: [defaults.git.depth](#defaultsgitdepth)

## `projects.git.config`

A map of git config values to install in the project. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. Git config values from [defaults.git.confg](#defaultsgitconfig) will be combined with those in the project. If the same keys are present, the project value will take priority. To prevent a value from [defaults.git.config](#defaultsgitconfig) from being inherited by the project, it must be set to `null`.

See also: [defaults.git.config](#defaultsgitconfig)

## `projects.fork`

A map of values defining a git fork.

## `projects.fork.name`

This is combined with the protocol (see: [defaults.protocol](#defaultsprotocol) [sources.protocol](#sourcesprotocol)) and [sources.url](#sourcesurl) to form the full url for cloning the repository:

- `git@${sources.url}:${projects.fork.name}.git`
- `https://${sources.url}/${projects.fork.name}.git`

## `projects.fork.source`

Source to use for forming git clone url.

See also: [defaults.source](#defaultssource), [sources.name](#sourcesname)

## `projects.fork.remote`

Git remote name.

See also: [defaults.remote](#defaultsremote)

## `projects.fork.branch`

Name of the branch to track for this project fork. Only one of `branch`, `tag`, or `commit` can be present. If not supplied and `tag` or `commit` are not specified in [projects.fork](#projectsfork) or [defaults](#defaults), the default branch `master` is used.

See also: [defaults.branch](#defaultsbranch)

## `projects.fork.tag`

Name of the Git tag to track for this project fork. Only one of `tag`, `tag`, or `commit` can be present. If not supplied and `branch` or `commit` are not specified in [projects.fork](#projectsfork) or [defaults](#defaults), the default branch `master` is used.

See also: [defaults.tag](#defaultstag)

## `projects.fork.commit`

A git commit SHA-1 to track for this project fork. Must be full 40 character SHA-1. Only one of `commit`, `tag`, or `commit` can be present. If not supplied and `branch` and `tag` are not specified in [projects.fork](#projectsfork) or [defaults](#defaults), the default branch `master` is used.

See also: [defaults.commit](#defaultscommit)
