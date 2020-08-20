# `clowder.yml` Syntax Reference

- [clowder structure](#clowder-structure)
- [project](#project)
- [upstream](#upstream)
- [group](#group)
- [defaults](#defaults)
- [source](#source)
- [protocol](#protocol)
- [git](#git)

## clowder structure

```yaml
name: string # REQUIRED

defaults: defaults

sources: { string: source}

clowder: [ project ] | { string: group } # REQUIRED
```

## project

```yaml
project:
  name: string # REQUIRED
  source: string | source
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
  branch: string # Only one of 'branch', 'tag', or 'commit' is allowed
  tag: string # Only one of 'branch', 'tag', or 'commit' is allowed
  commit: string # Only one of 'branch', 'tag', or 'commit' is allowed
```

## upstream

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
  branch: string # Only one of 'branch', 'tag', or 'commit' is allowed
  tag: string # Only one of 'branch', 'tag', or 'commit' is allowed
  commit: string # Only one of 'branch', 'tag', or 'commit' is allowed
```

## group

```yaml
group:
  path: string
  groups: [ string ]
  defaults: defaults
  projects: [ project ] # REQUIRED
```

## defaults

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  git: git
  branch: string # Only one of 'branch', 'tag', or 'commit' is allowed
  tag: string # Only one of 'branch', 'tag', or 'commit' is allowed
  commit: string # Only one of 'branch', 'tag', or 'commit' is allowed
```

## source

```yaml
source:
  url: string # REQUIRED
  protocol: enum
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
  submodules: bool | enum # "update" | "update recursive" | "recursive"
  depth: integer # Must be >= 0, where 0 indicates full clone
  config: { string: string | null }
```
