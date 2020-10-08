# `clowder.yml` Syntax Reference

- [clowder structure](#clowder-structure)
- [project](#project)
- [group](#group)
- [upstream](#upstream)
- [defaults](#defaults)
- [upstream defaults](#upstream-defaults)
- [source](#source)
- [protocol](#protocol)
- [git](#git)

## clowder structure

```yaml
name: string # REQUIRED
protocol: protocol
defaults: defaults
sources: { source_name: source } # key is a reusable alias
clowder: [ project | string ] | { string: group } # REQUIRED
```

## project

```yaml
project:
  name: string # REQUIRED
  path: string
  groups: [ string ]
  remote: string
  source: string | source
  git: git
  upstream: string | upstream
  branch: string # Only one of 'branch', 'tag', or 'commit' is allowed
  tag: string # Only one of 'branch', 'tag', or 'commit' is allowed
  commit: string # Only one of 'branch', 'tag', or 'commit' is allowed
```

## group

```yaml
group: [ project | string ]
```

```yaml
group:
  path: string
  groups: [ string ]
  defaults: defaults
  projects: [ project | string ] # REQUIRED
```

## upstream

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
```

## defaults

```yaml
defaults:
  source: string
  remote: string
  git: git
  branch: string # Only one of 'branch', 'tag', or 'commit' is allowed
  tag: string # Only one of 'branch', 'tag', or 'commit' is allowed
  commit: string # Only one of 'branch', 'tag', or 'commit' is allowed
  upstream: upstream_defaults
```

## upstream defaults

```yaml
upstream_defaults:
  source: string
  remote: string
```

## source

```yaml
url: string # REQUIRED
protocol: protocol
```

Default sources available:

```yaml
github:
  url: github.com
gitlab:
  url: gitlab.com
bitbucket:
  url: bitbucket.org
```

## protocol

```yaml
protocol: enum # "ssh" | "https"
```

## git

```yaml
git:
  lfs: bool
  submodules: bool | string # "recursive"
  depth: integer # Must be >= 0, where 0 indicates full clone
  config: { string: string | bool | number | null }
```
