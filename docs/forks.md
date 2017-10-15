# Forks

`clowder` simplifies some common fork workflows. Currently, it's only possible to add one fork for a project. Forks are handled specially by certain commands

- [clowder herd](#clowder-herd)
- [clowder prune](#clowder-prune)
- [clowder reset](#clowder-reset)
- [clowder start](#clowder-start)
- [clowder sync](#clowder-sync)

---

## `clowder herd`

Update with latest changes

```bash
# Herd a shallow clone to specified depth
$ clowder herd -d 1
```

```bash
# Herd using rebase instead of pull
$ clowder herd -r
```

```bash
# Herd a specified branch if it exists, otherwise use default ref
$ clowder herd -b my_branch
```

```bash
# Herd a specified tag if it exists, otherwise use default ref
$ clowder herd -t my_tag
```

---

## `clowder prune`

Prune local or remote branches

```bash
# Prune remote branch 'stale_branch' for all projects
$ clowder prune -r stale_branch
```

```bash
# Prune local and remote branch 'stale_branch' for all projects
$ clowder prune -a stale_branch

# Force prune local and remote branch 'stale_branch' for all projects
$ clowder prune -af stale_branch
```

---

## `clowder reset`

Reset branches to upstream state

```bash
# Reset branches in all projects
$ clowder reset
```

---

## `clowder start`

Start a new feature branch or check out if it already exists

```bash
# Create new local and remote tracking branch 'my_feature' for all projects
$ clowder start -t my_feature
```

---

## `clowder sync`

Sync default fork branches with upstream remotes

```bash
# Sync all forks with upstream remotes
$ clowder sync
```

```bash
# Sync using rebase instead of pull
$ clowder sync -r
```

---
