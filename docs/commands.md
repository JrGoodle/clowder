## `clowder` Commands

---

### `clowder clean`

Discards changes in dirty repositories.

```bash
$ clowder clean # Discard changes in all projects
$ clowder clean -g clang # Discard changes in projects in clang group
$ clowder clean -p llvm-mirror/clang # Discard changes in clang project
```

---

### `clowder forall`

Runs command argument in project directories.

```bash
$ clowder forall "git status" # Run command in all project directories
$ clowder forall "git status" -g clang # Run command for projects in clang group
$ clowder forall "git status" -p llvm-mirror/clang # Run command for clang project
```

---

### `clowder herd`

Update default branches with latest changes.

```bash
$ clowder herd -g clang llvm # Only herd projects in clang and llvm groups
$ clowder herd -p llvm-mirror/clang # Only herd clang project
$ clowder herd -v 0.1 # Point clowder.yaml symlink to saved version
```

---

### `clowder repo`

Manage clowder repository (`.clowder` directory).

```bash
$ clowder repo 'git status' # Run command in .clowder directory
```

---

### `clowder save`

Save a `clowder.yaml` version with the information from currently checked out repositories.

```bash
$ clowder save 0.1 # Save a version of clowder.yaml with current commit sha's
```

---

### `clowder start`

Start a new feature branch or check out if it already exists.

```bash
$ clowder start my_feature # Create new branch 'my_feature' for all projects
$ clowder start my_feature -g clang # Create new branch 'my_feature' in clang group
$ clowder start my_feature -p llvm-mirror/clang  # Create new branch 'my_feature' in clang project
```

---

### `clowder stash`

Stash changes in dirty repositories.

```bash
$ clowder stash # Stash any changes in projects
$ clowder stash -g clang # Stash any changes in projects in clang group
$ clowder stash -p llvm-mirror/clang # Stash any changes in clang project
```

---

### `clowder status`

Print status of projects.

```bash
$ clowder status # print status of projects
$ clowder status -v # print more verbose status of projects
$ clowder status -g clang llvm # print status of projects in clang and llvm groups
$ clowder status -v -g clang # print verbose status of projects in clang group
```
