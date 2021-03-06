# Cats `clowder.yml` example

See also: [clowder.yml syntax reference](clowder-yml-syntax-reference.md)

```yaml
name: cats-clowder

defaults:
  protocol: https
  branch: tracking_branch
  git:
    config:
      alias.cat: '!echo "😸"'

clowder:
  - name: JrGoodle/mu
    branch: groom
    git:
      lfs: true
      recursive: true
  - name: JrGoodle/duke
    tag: v0.01
  - name: JrGoodle/kit
    path: black-cats/kit
    commit: f2e20031ddce5cb097105f4d8ccbc77f4ac20709
  - name: JrGoodle/kishka
    path: black-cats/kishka
    git:
      config:
        alias.cat: '!echo "😸😸😸"'
  - name: JrGoodle/june
    path: black-cats/june
    git:
      config:
        alias.cat: null
  - name: JrGoodle/sasha
    path: black-cats/sasha
    remote: catnip
```

---

```yaml
defaults:
  protocol: https
  branch: tracking_branch
  git:
    config:
      alias.cat: '!echo "😸"'
```

This example specifies a default branch of `tracking_branch` that all projects will inherit. It's also possible to specify a default `tag` or `commit`. The `git`section can contain custom git config entries that will be installed for all projects.

```yaml
- name: JrGoodle/mu
  branch: groom
  git:
    lfs: true
    recursive: true
```

This project will track the `groom` branch. The `git` configuration enables git lfs and submodules. Running `clowder herd` will install git lfs hooks, pull lfs files, and clone submodules recursively.

```yaml
- name: JrGoodle/duke
  tag: v0.01
```

This project will check out the repository to the commit the `v0.01` tag points to.

```yaml
- name: JrGoodle/kit
  path: black-cats/kit
  commit: f2e20031ddce5cb097105f4d8ccbc77f4ac20709
```

This project will check out the repository to the commit specified by the full sha-1. The path the repository will be cloned at is `black-cats/kit`

```yaml
- name: JrGoodle/kishka
  path: black-cats/kishka
  git:
    config:
      alias.cat: '!echo "😸😸😸"'
```

When specified at the project level, the same git config values override any of the same ones in the `defaults`, in this case an alias for a `git cat` command that prints 😸.

```yaml
- name: JrGoodle/june
  path: black-cats/june
  git:
    config:
      alias.cat: null
```

To unset a git config entry in `defaults`, set the value to `null`.

```yaml
- name: JrGoodle/sasha
  path: black-cats/sasha
  remote: catnip
```

Adding a `remote` entry will create a remote named `catnip` instead of `origin`.
