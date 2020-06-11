# `clowder.yml` Syntax

- [name](#name) **Required**
- [defaults](#defaults) **Required**
- [defaults.protocol](#defaultsprotocol) **Required**
- [defaults.source](#defaultssource) __Required*__
- [defaults.remote](#defaultsremote)
- [defaults.branch](#defaultsbranch)
- [defaults.tag](#defaultstag)
- [defaults.commit](#defaultscommit)
- [defaults.git.lfs](#defaultsgitlfs)
- [defaults.git.recursive](#defaultsgitrecursive)
- [defaults.git.depth](#defaultsgitdepth)
- [defaults.git.config](#defaultsgitconfig)
- [sources](#sources) **Required**
- [sources.name](#sourcesname) **Required**
- [sources.url](#sourcesurl) **Required**
- [sources.protocol](#sourcesprotocol)
- [projects](#projects) **Required**
- [projects.name](#projectsname) **Required**
- [projects.source](#projectssource)
- [projects.branch](#projectsbranch)
- [projects.tag](#projectstag)
- [projects.commit](#projectscommit)
- [projects.path](#projectspath)
- [projects.remote](#projectsremote)
- [projects.groups](#projectsgroups)
- [projects.fork](#projectsfork)
- [projects.fork.name](#projectsforkname)
- [projects.fork.source](#projectsforksource)
- [projects.fork.remote](#projectsforkremote)
- [projects.git.lfs](#projectsgitlfs)
- [projects.git.recursive](#projectsgitrecursive)
- [projects.git.depth](#projectsgitdepth)
- [projects.git.config](#projectsgitconfig)

## Descriptions

### `name`

Name to be displayed when running commands.

### `defaults`

Default settings that will apply to all projects or sources.

### `defaults.protocol`

**REQUIRED** The git protocol to use when cloning repositories. Options are `ssh` and `https`. This value is inherited by sources, and can be overridden by setting the [sources.protocol](#sourcesprotocol) property.

### `defaults.source`

__REQUIRED*__ The name of the default source to use when cloning project repositories. This can be overridden by setting [projects.source](#projectssource) or [projects.fork.source](#projectsforksource). If only one source is present in `sources` then this value is optional. If more than one is specified, this value is required.

### `defaults.remote`

The default name of the git remote. This can be overridden by setting [projects.remote](#projectsremote) or [projects.fork.remote](#projectsforkremote).

### `defaults.branch`

The default name of the branch projects should track. This can be overridden by setting [projects.branch](#projectsbranch) or [projects.fork.branch](#projectsforkbranch). Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.tag`

The default name of the tag projects should track. This can be overridden by setting [projects.tag](#projectstag) or [projects.fork.tag](#projectsforktag). Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.commit`

The default commit projects should track. This can be overridden by setting [projects.commit](#projectscommit) or [projects.fork.commit](#projectsforkcommit). Only one of `branch`, `tag`, or `commit` can be present. Must be the full 40-character sha-1.

### `defaults.git.lfs`

Setting this value to `true` will cause clowder to install git lfs hooks and pull lfs files when `clowder herd` is run. This can be overridden by setting [projects.git.lfs](#projectsgitlfs).

### `defaults.git.recursive`

Setting this value to `true` will cause clowder to recursively init and update submodules when `clowder herd` is run. This can be overridden by setting [projects.git.recursive](#projectsgitrecursive).

### `defaults.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned. This can be overridden by setting [projects.git.depth](#projectsgitdepth).

### `defaults.git.config`

A map of git config values to install in projects. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. This can be overridden by setting [projects.git.config](#projectsgitconfig). Git config values from defaults will be combined with those in [projects.git.confg](#projects.git.config). If the same keys are present, the project value will take priority. To prevent a default git config value from being inherited by a project, it must be set to `null` in [projects.git.config](#projectsgitconfig).

### `sources`

**REQUIRED** List of git repository sources.

### `sources.name`

**REQUIRED** The name used to identify the repository source for [defaults.remote](#defaultsremote), [projects.remote](#projectsremote), and [projects.fork.remote](#projectsforkremote).

### `sources.url`

**REQUIRED** The Git URL prefix for all projects which use this source. This is combined with [defaults.protocol](#defaultsprotocol) or [sources.protocol](#sourcesprotocol) and [projects.name](#projectsname) to form the full url for cloning the repository, taking the form of `git@${defaults.url/sources.url}:${projects.name}.git` or `https://${defaults.url/sources.url}/${projects.name}.git` depending on the protocol specified.

### `sources.protocol`

The Git URL protocol prefix for all projects which use this source. Accepted values are `ssh` and `https`. This is combined with [sources.url](#sourcesurl) and [projects.name](#projectsname) to form the full url for cloning the repository, taking the form of `git@${defaults.url/sources.url}:${projects.name}.git` or `https://${defaults.url/sources.url}/${projects.name}.git` depending on the protocol specified.

### `projects`

**REQUIRED** List of projects.

### `projects.name`

**REQUIRED** A unique name for this project. The project's name is appended onto its source's URL to generate the actual URL to configure the Git remote with. This is combined with [defaults.protocol](#defaultsprotocol) or [sources.protocol](#sourcesprotocol) and [sources.url](#sourcesurl) to form the full url for cloning the repository, taking the form of `git@${defaults.url/sources.url}:${projects.name}.git` or `https://${defaults.url/sources.url}/${projects.name}.git` depending on the protocol specified.

### `projects.source`

Name from [sources.name](#sourcesname) to use for forming git clone url. See also [defaults.source](#defaultssource).

### `projects.branch`

Name of the Git branch to track for this project. Only one of `branch`, `tag`, or `commit` can be present. If not supplied and `tag` or `commit` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.tag`

Name of the Git tag to track for this project. Only one of `tag`, `tag`, or `commit` can be present. If not supplied and `branch` or `commit` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.commit`

A git commit SHA-1 to track for this project. Must be full 40 character SHA-1. Only one of `commit`, `tag`, or `commit` can be present. If not supplied and `branch` and `tag` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.path`

Relative path to clone git repository. If not present, then the last path component of [projects.name](#projectsname) will be used as the git clone path.

### `projects.remote`

The git remote name. See also [defaults.remote](#defaultsremote).

### `projects.groups`

Projects can specify custom groups to run commands for only certain projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present, then the project will not be included in commands unless another group argument is given that it belongs to. The values of `all` and `default` are reserved and not allowed to be specified in this list.

### `projects.fork`

A map of values defining a git fork.

### `projects.fork.name`

This is combined with [defaults.protocol](#defaultsprotocol) or [sources.protocol](#sourcesprotocol) and [sources.url](#sourcesurl) to form the full url for cloning the repository, taking the form of `git@${defaults.url/sources.url}:${projects.fork.name}.git` or `https://${defaults.url/sources.url}/${projects.fork.name}.git` depending on the protocol specified.

### `projects.fork.source`

Name from [sources.name](#sourcesname) to use for forming git clone url. See also [defaults.source](#defaultssource).

### `projects.fork.remote`

Git remote name. See also [defaults.remote](#defaultsremote).

### `projects.git.lfs`

Setting this value to `true` will cause clowder to install git lfs hooks and pull lfs files when `clowder herd` is run. See also [defaults.git.lfs](#defaultsgitlfs)

### `projects.git.recursive`

Setting this value to `true` will cause clowder to recursively init and update submodules when `clowder herd` is run. See also [defaults.git.recursive](#defaultsgitrecursive)

### `projects.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned. See also [defaults.git.depth](#defaultsgitdepth)

### `projects.git.config`

A map of git config values to install in the project. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. Git config values from [defaults.git.confg](#defaults.git.config) will be combined with those in the project. If the same keys are present, the project value will take priority. To prevent a value from [defaults.git.config](#defaultsgitconfig) from being inherited by the project, it must be set to `null`. See also [defaults.git.config](#defaultsgitconfig)
