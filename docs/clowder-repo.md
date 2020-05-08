# The Clowder Repo

The "clowder repo" is a git repository cloned into the `.clowder` directory when the `clowder init` command is run

## Primary/Default `clowder.yaml`

 At the root is the primary `clowder.yaml` that is symlinked by default during `clowder init`. This file can be symlinked later be running `clowder link`

## Versions

A `versions` directory can contain versioned `clowder.yaml` files. These can be symlinked with the `clowder link -v` command

For example, `versions/my_version.yaml` would by symlinked by running `clowder link -v my_version`
