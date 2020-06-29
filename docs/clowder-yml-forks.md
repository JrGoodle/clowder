# Forks `clowder.yml` example

See also: [clowder.yml syntax reference](clowder-yml-syntax-reference.md)

```yaml
name: forks-clowder

defaults:
  protocol: ssh
  source: github
  git:
    recursive: true

sources:
  - name: github
    url: github.com
  - name: chromium
    url: chromium.googlesource.com
    protocol: https
  - name: sourceforge
    url: git.code.sf.net
    protocol: https

projects:
  - name: dropbox/djinni
    remote: upstream
    fork:
      name: JrGoodle/djinni
  - name: external/gyp
    source: chromium
    remote: upstream
    fork:
      name: JrGoodle/gyp
      branch: fork-branch
  - name: p/sox/code
    path: sox
    remote: upstream
    source: sourceforge
    fork:
      name: JrGoodle/sox
```

---

```yaml
defaults:
  protocol: ssh
  source: github
  git:
    recursive: true
```

Because more than one source is specified, the default `source` to use to clone projects must be given. All projects will recursively init and update submodules by default.

```yaml
sources:
  - name: github
    url: github.com
  - name: chromium
    url: chromium.googlesource.com
    protocol: https
  - name: sourceforge
    url: git.code.sf.net
    protocol: https
```

The `protocol` is set specifically to `https` for repositories where the user may not have the ability to clone via `ssh`.

```yaml
- name: dropbox/djinni
  remote: upstream
  fork:
    name: JrGoodle/djinni
```

The original repository will be cloned with a remote named `upstream`. The `fork` inherits the default remote `origin`.

```yaml
- name: external/gyp
  source: chromium
  remote: upstream
  fork:
    name: JrGoodle/gyp
    branch: fork-branch
```

The user's fork will track `fork-branch`.

```yaml
- name: p/sox/code
  path: sox
  remote: upstream
  source: sourceforge
  fork:
    name: JrGoodle/sox
```

This example will check out the repository to the `sox` directory, rather than `code`.
