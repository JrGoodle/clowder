# `clowder.yml` Inheritance Reference

- [project](#project)
  - [project.name](#projectname)
  - [project.path](#projectpath)
  - [project.remote](#projectremote)
  - [project.groups](#projectgroups)
  - [project.(ref)](#projectref)
    - [project.branch](#projectbranch)
    - [project.tag](#projecttag)
    - [project.commit](#projectcommit)
  - [project.source](#projectsource)
  - [project.source.url](#projectsourceurl)
  - [project.source.protocol](#projectsourceprotocol)
  - [project.git.lfs](#project.gitlfs)
  - [project.git.submodules](#projectgitsubmodules)
  - [project.git.depth](#project.gitdepth)
  - [project.git.config.setting](#projectgitconfigsetting)
- [upstream](#upstream)
  - [upstream.name](#upstreamname)
  - [upstream.remote](#upstreamremote)
  - [upstream.source.url](#upstreamsourceurl)
  - [upstream.source.protocol](#upstreamsourceprotocol)

## project

Referred to in this document as `..project`

Projects can be located at:

- `clowder.project`
- `clowder.<group_name>.project`
- `clowder.<group_name>.projects.project`

### project.name

- `..project.name`

### project.path

- Default: `..project.name` last path component
- `..project.path`

### project.remote

- Default: `origin`
- `defaults.remote`
- `clowder.<group_name>.defaults.remote`
- `..project.remote`

### project.groups

Values are combined rather than overridden.

- `clowder.<group_name>`
- `clowder.<group_name>.defaults.groups`
- `..project.groups`

### project.(ref)

- Default: `origin` branch
- `defaults.branch`
- `defaults.tag`
- `defaults.commit`
- `clowder.<group_name>.defaults.branch`
- `clowder.<group_name>.defaults.tag`
- `clowder.<group_name>.defaults.commit`
- `..project.branch`
- `..project.tag`
- `..project.commit`
- Command line argument

#### project.branch

- Default: `master`
- `defaults.branch`
- `clowder.<group_name>.defaults.branch`
- `..project.branch`

#### project.tag

- `defaults.tag`
- `clowder.<group_name>.defaults.tag`
- `..project.tag`

#### project.commit

- `defaults.commit`
- `clowder.<group_name>.defaults.commit`
- `..project.commit`

### project.source

- Default: `github`
- `defaults.source`
- `clowder.<group_name>.defaults.source`
- `..project.source`

### project.source.url

- `defaults.source.url`
- `clowder.<group_name>.defaults.source.url`
- `..project.source.url`

### project.source.protocol

- Default: `ssh`
- `defaults.source.protocol`
- `clowder.<group_name>.defaults.source.protocol`
- `..project.source.protocol`
- Config value
- Command line argument

### project.git.lfs

- Default: `false`
- `defaults.git.lfs`
- `clowder.<group_name>.defaults.git.lfs`
- `..project.git.lfs`

### project.git.submodules

- Default: `false`
- `defaults.git.submodules`
- `clowder.<group_name>.defaults.git.submodules`
- `..project.git.submodules`

### project.git.depth

- Default: `0` full clone
- `defaults.git.depth`
- `clowder.<group_name>.defaults.git.depth`
- `..project.git.depth`

### project.git.config.setting

- `defaults.git.config.setting`
- `clowder.<group_name>.defaults.git.config.setting`
- `..project.git.config.setting`

## upstream

Referred to in this document as `..upstream`

Upstreams can be located at:

- `clowder.project.upstream`
- `clowder.<group_name>.project.upstream`
- `clowder.<group_name>.projects.project.upstream`

### upstream.name

- `..upstream.name`

### upstream.remote

- Default: `origin`
- `defaults.remote`
- `clowder.<group_name>.defaults.remote`
- `..upstream.remote`

### upstream.source.url

- `defaults.source.url`
- `clowder.<group_name>.defaults.source.url`
- `..upstream.source.url`

### upstream.source.protocol

- Default: `ssh`
- `defaults.source.protocol`
- `clowder.<group_name>.defaults.source.protocol`
- `..upstream.source.protocol`
- Config value
- Command line argument
