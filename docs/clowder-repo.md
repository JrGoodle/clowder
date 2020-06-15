# The Clowder Repo

The "clowder repo" is a git repository cloned into the `.clowder` directory when the `clowder init` command is run

## Default `clowder.yml`

 At the root is the primary `clowder.yml` that is symlinked by default during `clowder init`. This file can be symlinked later be running `clowder link`

## Versions

A `versions` directory can contain versioned `<version>.clowder.yml` files. These can be symlinked with the `clowder link <version>` command

For example, `versions/my_version.clowder.yml` would by symlinked by running `clowder link my_version`
