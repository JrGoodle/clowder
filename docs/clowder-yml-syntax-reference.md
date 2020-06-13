# `clowder.yml` Syntax Reference

- [name](#name) **Required**
- [defaults](#defaults) **Required**
- [defaults.protocol](#defaults-protocol) **Required**
- [defaults.source](#defaults-source) __Required*__
- [defaults.remote](#defaults-remote)
- [defaults.branch](#defaults-branch)
- [defaults.tag](#defaults-tag)
- [defaults.commit](#defaults-commit)
- [defaults.git.lfs](#defaults-git-lfs)
- [defaults.git.recursive](#defaults-git-recursive)
- [defaults.git.depth](#defaults-git-depth)
- [defaults.git.config](#defaults-git-config)
- [sources](#sources) **Required**
- [sources.name](#sources-name) **Required**
- [sources.url](#sources-url) **Required**
- [sources.protocol](#sources-protocol)
- [projects](#projects) **Required**
- [projects.name](#projects-name) **Required**
- [projects.source](#projects-source)
- [projects.branch](#projects-branch)
- [projects.tag](#projects-tag)
- [projects.commit](#projects-commit)
- [projects.path](#projects-path)
- [projects.remote](#projects-remote)
- [projects.groups](#projects-groups)
- [projects.fork](#projects-fork)
- [projects.fork.name](#projects-fork-name)
- [projects.fork.source](#projects-fork-source)
- [projects.fork.remote](#projects-fork-remote)
- [projects.fork.branch](#projects-fork-branch)
- [projects.fork.tag](#projects-fork-tag)
- [projects.fork.commit](#projects-fork-commit)
- [projects.git.lfs](#projects-git-lfs)
- [projects.git.recursive](#projects-git-recursive)
- [projects.git.depth](#projects-git-depth)
- [projects.git.config](#projects-git-config)

## Descriptions

### `name`

Name to be displayed when running commands.

### `defaults`

Default settings that will apply to all projects or sources.

### `defaults.protocol`

**REQUIRED** The git protocol to use when cloning repositories. Options are `ssh` and `https`. This value is inherited by sources, and can be overridden by setting the [sources.protocol](#sources-protocol) property.

### `defaults.source`

__REQUIRED*__ The name of the default source to use when cloning project repositories. This can be overridden by setting [projects.source](#projects-source) or [projects.fork.source](#projects-fork-source). If only one source is present in `sources` then this value is optional. If more than one is specified, this value is required.

### `defaults.remote`

The default name of the git remote. This can be overridden by setting [projects.remote](#projects-remote) or [projects.fork.remote](#projects-fork-remote).

### `defaults.branch`

The default name of the branch projects should track. This can be overridden by setting [projects.branch](#projects-branch) or [projects.fork.branch](#projects-fork-branch). Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.tag`

The default name of the tag projects should track. This can be overridden by setting [projects.tag](#projects-tag) or [projects.fork.tag](#projects-fork-tag). Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.commit`

The default commit projects should track. This can be overridden by setting [projects.commit](#projects-commit) or [projects.fork.commit](#projects-fork-commit). Only one of `branch`, `tag`, or `commit` can be present. Must be the full 40-character sha-1.

### `defaults.git.lfs`

Setting this value to `true` will cause clowder to install git lfs hooks and pull lfs files when `clowder herd` is run. This can be overridden by setting [projects.git.lfs](#projects-git-lfs).

### `defaults.git.recursive`

Setting this value to `true` will cause clowder to recursively init and update submodules when `clowder herd` is run. This can be overridden by setting [projects.git.recursive](#projects-git-recursive).

### `defaults.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned. This can be overridden by setting [projects.git.depth](#projects-git-depth).

### `defaults.git.config`

A map of git config values to install in projects. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. This can be overridden by setting [projects.git.config](#projects-git-config). Git config values from defaults will be combined with those in [projects.git.confg](#projects-git-config). If the same keys are present, the project value will take priority. To prevent a default git config value from being inherited by a project, it must be set to `null` in [projects.git.config](#projects-git-config).

### `sources`

**REQUIRED** List of git repository sources.

### `sources.name`

**REQUIRED** The name used to identify the repository source for [defaults.remote](#defaults-remote), [projects.remote](#projects-remote), and [projects.fork.remote](#projects-fork-remote).

### `sources.url`

**REQUIRED** The Git URL prefix for all projects which use this source. This is combined with [defaults.protocol](#defaults-protocol) or [sources.protocol](#sources-protocol) and [projects.name](#projects-name) to form the full url for cloning the repository, taking the form of `git@${sources.url}:${projects.name}.git` or `https://${sources.url}/${projects.name}.git` depending on the protocol specified.

### `sources.protocol`

The Git URL protocol prefix for all projects which use this source. Accepted values are `ssh` and `https`. This is combined with [sources.url](#sources-url) and [projects.name](#projects-name) to form the full url for cloning the repository, taking the form of `git@${sources.url}:${projects.name}.git` or `https://${sources.url}/${projects.name}.git` depending on the protocol specified. See also [defaults.protocol](#defaults-protocol).

### `projects`

**REQUIRED** List of projects.

### `projects.name`

**REQUIRED** A unique name for this project. The project's name is appended onto its source's URL to generate the actual URL to configure the Git remote with. This is combined with [defaults.protocol](#defaults-protocol) or [sources.protocol](#sources-protocol) and [sources.url](#sources-url) to form the full url for cloning the repository, taking the form of `git@${sources.url}:${projects.name}.git` or `https://${sources.url}/${projects.name}.git` depending on the protocol specified.

### `projects.source`

Name from [sources.name](#sources-name) to use for forming git clone url. See also [defaults.source](#defaults-source).

### `projects.branch`

Name of the Git branch to track for this project. Only one of `branch`, `tag`, or `commit` can be present. If not supplied and `tag` or `commit` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.tag`

Name of the Git tag to track for this project. Only one of `tag`, `tag`, or `commit` can be present. If not supplied and `branch` or `commit` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.commit`

A git commit SHA-1 to track for this project. Must be full 40 character SHA-1. Only one of `commit`, `tag`, or `commit` can be present. If not supplied and `branch` and `tag` are not specified in [projects](#projects) or [defaults](#defaults), the default branch `master` is used.

### `projects.path`

Relative path to clone git repository. If not present, then the last path component of [projects.name](#projects-name) will be used as the git clone path.

### `projects.remote`

The git remote name. See also [defaults.remote](#defaults-remote).

### `projects.groups`

Projects can specify custom groups to run commands for only certain projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present, then the project will not be included in commands unless another group argument is given that it belongs to. The values of `all` and `default` are reserved and not allowed to be specified in this list.

### `projects.fork`

A map of values defining a git fork.

### `projects.fork.name`

This is combined with [defaults.protocol](#defaults-protocol) or [sources.protocol](#sources-protocol) and [sources.url](#sources-url) to form the full url for cloning the repository, taking the form of `git@${sources.url}:${projects.fork.name}.git` or `https://${sources.url}/${projects.fork.name}.git` depending on the protocol specified.

### `projects.fork.source`

Name from [sources.name](#sources-name) to use for forming git clone url. See also [defaults.source](#defaults-source).

### `projects.fork.remote`

Git remote name. See also [defaults.remote](#defaults-remote).

### `projects.fork.branch`

Name of the Git branch to track for this project fork. Only one of `branch`, `tag`, or `commit` can be present. If not supplied and `tag` or `commit` are not specified in [projects.fork](#projects-fork) or [defaults](#defaults), the default branch `master` is used.

### `projects.fork.tag`

Name of the Git tag to track for this project fork. Only one of `tag`, `tag`, or `commit` can be present. If not supplied and `branch` or `commit` are not specified in [projects.fork](#projects-fork) or [defaults](#defaults), the default branch `master` is used.

### `projects.fork.commit`

A git commit SHA-1 to track for this project fork. Must be full 40 character SHA-1. Only one of `commit`, `tag`, or `commit` can be present. If not supplied and `branch` and `tag` are not specified in [projects.fork](#projects-fork) or [defaults](#defaults), the default branch `master` is used.

### `projects.git.lfs`

Setting this value to `true` will cause clowder to install git lfs hooks and pull lfs files when `clowder herd` is run. See also [defaults.git.lfs](#defaults-git-lfs)

### `projects.git.recursive`

Setting this value to `true` will cause clowder to recursively init and update submodules when `clowder herd` is run. See also [defaults.git.recursive](#defaults-git-recursive)

### `projects.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned. See also [defaults.git.depth](#defaults-git-depth)

### `projects.git.config`

A map of git config values to install in the project. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. Git config values from [defaults.git.confg](#defaults-git-config) will be combined with those in the project. If the same keys are present, the project value will take priority. To prevent a value from [defaults.git.config](#defaults-git-config) from being inherited by the project, it must be set to `null`. See also [defaults.git.config](#defaults-git-config)
