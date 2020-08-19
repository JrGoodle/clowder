# `clowder.yml` Syntax Reference

- [clowder structure](#clowder-structure)
- [defaults](#defaults)
- [sources](#source)
- [protocoll](#protocoll)
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
```

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  git: git
  tag: string
```

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  git: git
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
```

```yaml
project:
  name: string # REQUIRED
  source: string | source
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
  tag: string
```

```yaml
project:
  name: string # REQUIRED
  source: string | source
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
  commit: string
```

## upstream

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
  branch: string
```

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
  tag: string
```

```yaml
upstream:
  name: string # REQUIRED
  source: string | source
  remote: string
  commit: string
```
