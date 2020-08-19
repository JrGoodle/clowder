# `clowder.yml` Syntax Reference

- [clowder structure](#clowder-structure)
- [defaults](#defaults)
- [sources](#source)
- [protocol](#protocol)
- [git](#git)
- [group](#group)
- [project](#project)
- [upstream](#upstream)

## clowder structure

```yaml
name: string # REQUIRED

defaults: defaults

sources: { string: source}

clowder: [ project ] | { string: group } # REQUIRED
```

## defaults

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  git: git
  branch: string
  tag: string
  commit: string
```

## source

```yaml
source:
  url: string # REQUIRED
  protocol: enum
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

## group

```yaml
group:
  path: string
  groups: [ string ]
  defaults: defaults
  projects: [ project ] # REQUIRED
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
  branch: string
  tag: string
  commit: string
```

## upstream

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
  branch: string
  tag: string
  commit: string
```
