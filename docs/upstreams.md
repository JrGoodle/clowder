# Upstreams

`clowder` simplifies some common fork workflows. Currently, it's only possible to add one fork for a project. Upstreams are handled specially by certain commands.

## `clowder herd`

Update with latest changes

```bash
# Herd a shallow clone to specified depth
$ clowder herd -d 1
```

- If any projects don't have a clean git status then `clowder` exits
- Projects are cloned from the upstream remote if they don't currently exist
- Each project fetches the latest changes from upstream
- If the current git ref checked out doesn't match the `clowder.yml` configuration, the correct ref will be checked out
- The latest changes are pulled from upstream for branches. For commits and tags, the commits are checked out into a detached `HEAD` state

```bash
# Herd using rebase instead of pull
$ clowder herd -r
```

```bash
# Herd a specified branch if it exists, otherwise use default ref
$ clowder herd -b my_branch
```

- If any projects don't have a clean git status then `clowder` exits
- Projects are cloned from the upstream remote if they don't currently exist
- Each project fetches the latest changes from upstream
- If a local branch exists, it's checked out
- If a remote branch `my_branch` exists on the fork remote, the latest changes are pulled. Otherwise, if a remote branch `my_branch` exists upstream, the latest changes are pulled
- If no local or upstream branches exist, the default ref will be checked out like a normal `herd`

```bash
# Herd a specified tag if it exists, otherwise use default ref
$ clowder herd -t my_tag
```

- If any projects don't have a clean git status then `clowder` exits
- Projects are cloned from the upstream remote if they don't currently exist
- Each project fetches the latest changes from upstream
- If a tag exists, it's checked out into a detached `HEAD` state
- If no tag exists, the default ref will be checked out like a normal `herd`

## `clowder prune`

Prune local or remote branches

```bash
# Prune remote branch 'stale_branch' for all projects
$ clowder prune -r stale_branch

# Prune local and remote branch 'stale_branch' for all projects
$ clowder prune -a stale_branch

# Force prune local and remote branch 'stale_branch' for all projects
$ clowder prune -af stale_branch
```

Remote branches are pruned form the fork remote, on the assumption that the user doesn't have write access to the upstream remote

## `clowder reset`

Reset branches to upstream state

```bash
# Reset branches in all projects
$ clowder reset
```

- If any projects don't have a clean git status then `clowder` exits
- Projects are cloned from the upstream remote if they don't currently exist
- Each project fetches the latest changes from upstream
- Branches are reset to the upstream remote branch's latest commit. Otherwise, projects are checked out into a detached `HEAD` state for tags and shas

## `clowder start`

Start a new feature branch or check out if it already exists

```bash
# Create new local and remote tracking branch 'my_feature' for all projects
$ clowder start -t my_feature
```

New tracking branches are created on the fork remote, on the assumption that the user doesn't have write access to the upstream remote
