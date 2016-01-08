## `clowder` Commands

---

### `clean`

Discards changes in dirty repositories.

```bash
# Discard changes in all projects
$ clowder clean

# Discard changes in projects in clang group
$ clowder clean -g clang

# Discard changes in clang project
$ clowder clean -p llvm-mirror/clang
```

---

### `forall`

Runs command argument in project directories.

```bash
# Run command in all project directories
$ clowder forall "git status"

# Run command for projects in clang group
$ clowder forall "git status" -g clang

# Run command for clang project
$ clowder forall "git status" -p llvm-mirror/clang
```

---

### `herd`

Update default branches with latest changes.

```bash
# Only herd projects in clang and llvm groups
$ clowder herd -g clang llvm

# Only herd clang project
$ clowder herd -p llvm-mirror/clang

# Point clowder.yaml symlink to saved version
$ clowder herd -v 0.1
```

---

### `init`

Clone repo containing `clowder.yaml` file ('clowder repo').

```bash
# Clone clowder repo
$ clowder init https://github.com/jrgoodle/llvm-projects.git

# Clone clowder repo from branch 'tags'
$ clowder init https://github.com/jrgoodle/cats.git -b tags
```

---

### `repo`

Manage clowder repository (`.clowder` directory).

```bash
# Run command in .clowder directory
$ clowder repo 'git status'
```

---

### `save`

Save a `clowder.yaml` version with the information from currently checked out repositories.

```bash
# Save a version of clowder.yaml with current commit sha's
$ clowder save 0.1
```

---

### `start`

Start a new feature branch or check out if it already exists.

```bash
# Create new branch 'my_feature' for all projects
$ clowder start my_feature

# Create new branch 'my_feature' in clang group
$ clowder start my_feature -g clang

# Create new branch 'my_feature' in clang project
$ clowder start my_feature -p llvm-mirror/clang
```

---

### `stash`

Stash changes in dirty repositories.

```bash
# Stash any changes in projects
$ clowder stash

# Stash any changes in projects in clang group
$ clowder stash -g clang

# Stash any changes in clang project
$ clowder stash -p llvm-mirror/clang
```

---

### `status`

Print status of projects.

```bash
# print status of projects
$ clowder status

# print more verbose status of projects
$ clowder status -v

# print status of projects in clang and llvm groups
$ clowder status -g clang llvm

# print verbose status of projects in clang group
$ clowder status -v -g clang
```

---

### `prune`

Prune stale local branches.

```bash
# Prune branch 'stale_branch' for all projects
$ clowder prune stale_branch

# Prune branch 'stale_branch' in clang group
$ clowder prune stale_branch -g clang

# Prune branch 'stale_branch' in clang project
$ clowder prune stale_branch -p llvm-mirror/clang
```
