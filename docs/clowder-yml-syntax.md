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

The name of your clowder. The name will be displayed when running commands.

### `defaults`

Default settings that will apply to all projects or sources. These values can be overridden at the source, project, or fork levels.

### `defaults.protocol`

**REQUIRED** The git protocol to use when cloning repositories. Options are `ssh` and `https`. This value is inherited by sources, and can be overridden by setting the [sources.protocol](#sourcesprotocol) property.

### `defaults.source`

__REQUIRED*__ The name of the default source to use when cloning project repositories. This can be overridden at the project and fork levels. If only one source is present in `sources` then this value is optional. If more than one is specified, this value is required.

### `defaults.remote`

The default name of the remote created for projects. This can be overridden at the project and fork levels.

### `defaults.branch`

The default name of the branch projects should track. This can be overridden at the project and fork levels. Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.tag`

The default name of the tag projects should track. This can be overridden at the project and fork levels. Only one of `branch`, `tag`, or `commit` can be present.

### `defaults.commit`

The default commit projects should track. This can be overridden at the project and fork levels. Only one of `branch`, `tag`, or `commit` can be present. Must be the full 40-character sha-1.

### `defaults.git.lfs`

Setting this value to true will cause clowder to install git lfs hooks and pull lfs files when `clowde herd` is run.

### `defaults.git.recursive`

Setting this value to true will cause clowder to recursively init and update submodules when `clowde herd` is run.

### `defaults.git.depth`

The default depth git will clone repositories. Must be a positive integer. If set to `0` the full repository history will be cloned.

### `defaults.git.config`

A map of git config values to install in projects. During an initial clone, they will be installed at the end. Later invocations of `clowder herd` will install the config values before running other commands. This can be overridden at the project level. Git config values from defaults will be combined with those in a project. If the same keys are present, the project value will take priority. To prevent a default git config value from being inherited by a project, it must be set to `null` in the `projects.git.config` settings.

### `sources`

**REQUIRED** List of git repository sources.

### `sources.name`

**REQUIRED** The name used to identify the repository source when used in the `remote` entry in defaults, project, or fork.

### `sources.url`

**REQUIRED** This is combined with the `protocol` and `projects.name` to form the full url for cloning the repository, taking the form of  `git@${source.url}:${project.name}.git` or `https://${source.url}/${project.name}.git` depending on the protocol specified.

### `sources.protocol`

The git protocol to use when cloning repositories. Options are `ssh` and `https`. This is combined with the `source.url` and `project.name` to form the full url for cloning the repository, taking the form of  `git@${source.url}:${project.name}.git` or `https://${source.url}/${project.name}.git` depending on the protocol specified.

### `projects`

**REQUIRED** List of projects.

### `projects.name`

**REQUIRED** This is combined with the `protocol` and `sources.url` to form the full url for cloning the repository, taking the form of  `git@${source.url}:${project.name}.git` or `https://${source.url}/${project.name}.git` depending on the protocol specified.

### `projects.source`

Name from `source.name` to use for forming git clone url.

### `projects.branch`

See [defaults.branch](#defaultsbranch)

### `projects.tag`

See [defaults.tag](#defaultstag)

### `projects.commit`

See [defaults.commit](#defaultscommit)

### `projects.path`

Relative path to clone git repository to. If not present, then the last path component of `project.name` will be used as the git clone path.

### `projects.remote`

Git remote name.

### `projects.groups`

Projects can specify custom `groups` to run commands for only certain projects. By default, all projects are added to the `all` group, and a group of their `name` and `path`. If `notdefault` is present then the project will not be included in commands unless another group argument is given that it belongs to.

### `projects.fork`

A map of values defining a git fork.

### `projects.fork.name`

This is combined with the `protocol` and `sources.url` to form the full url for cloning the repository, taking the form of  `git@${source.url}:${fork.name}.git` or `https://${source.url}/${fork.name}.git` depending on the protocol specified.

### `projects.fork.source`

See [projects.source](#projectssource)

### `projects.fork.remote`

Git remote name.

### `projects.git.lfs`

See [defaults.git.lfs](#defaultsgitlfs)

### `projects.git.recursive`

See [defaults.git.recursive](#defaultsgitrecursive)

### `projects.git.depth`

See [defaults.git.depth](#defaultsgitdepth)

### `projects.git.config`

See [defaults.git.config](#defaultsgitconfig)
