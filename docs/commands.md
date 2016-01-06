## `clowder` Commands

```bash
$ clowder save 0.1 # Save a version of clowder.yaml with current commit sha's
```

```bash
$ clowder forall "git status" # Run command in all project directories
$ clowder forall "git status" -g clang # Run command for projects in clang group
$ clowder forall "git status" -p llvm-mirror/clang # Run command for clang project
```

```bash
$ clowder clean # Discard any changes in projects
$ clowder clean -g clang # Discard any changes in projects in clang group
$ clowder clean -p llvm-mirror/clang # Discard any changes in clang project
```

```bash
$ clowder herd -g clang llvm # Only herd projects in clang and llvm groups
$ clowder herd -p llvm-mirror/clang # Only herd clang project
$ clowder herd -v 0.1 # Point clowder.yaml symlink to saved version
```

```bash
$ clowder status # print status of projects
$ clowder status -v # print more verbose status of projects
$ clowder status -g clang llvm # print status of projects in clang and llvm groups
$ clowder status -v -g clang # print verbose status of projects in clang group
```

```bash
$ clowder repo 'git status' # Run command in .clowder directory
```

```bash
$ clowder stash # Stash any changes in projects
$ clowder stash -g clang # Stash any changes in projects in clang group
$ clowder stash -p llvm-mirror/clang # Stash any changes in clang project
```
