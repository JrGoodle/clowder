# `clowder.yml` Syntax Reference

## clowder structure

```yaml
name: string # REQUIRED

defaults: defaults

sources: { string: source}

clowder: [ project ] | { string: group } # REQUIRED
```

## group

```yaml
group:
  path: string
  groups: [ string ]
  defaults: defaults
  projects: [ project ] # REQUIRED
```

## protocol

```yaml
protocol: enum # "ssh" | "https"
```

## source

```yaml
source:
  url: string # REQUIRED
  protocol: enum
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

## git

```yaml
git:
  lfs: bool
  submodules: bool | enum # "update" | "update recursive" | "recursive"
  depth: integer # Must be >= 0, where 0 indicates full clone
  config: { string: string }
```

## defaults

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  branch: string
  git: git
```

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  tag: string
  git: git
```

```yaml
defaults:
  protocol: protocol
  source: string | source
  remote: string
  commit: string
  git: git
```

## project

```yaml
project:
  name: string # REQUIRED
  source: string | source
  branch: string
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
```

```yaml
project:
  name: string # REQUIRED
  source: string | source
  tag: string
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
```

```yaml
project:
  name: string # REQUIRED
  source: string | source
  commit: string
  path: string
  remote: string
  groups: [ string ]
  git: git
  upstream: string | upstream
```
