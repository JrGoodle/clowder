# Contributing

## Getting Started

Clone the repository:

```bash
git clone git@github.com:JrGoodle/clowder.git
cd clowder
```

Add the directory you cloned the repo into to `PYTHONPATH` in your shell profile. For example, if cloned into `$HOME/clowder`

```bash
export PYTHONPATH="$PYTHONPATH:$HOME/clowder/clowder"
```

## Building

Install `clowder` for local development

```bash
script/update
```

Remove `clowder`

```bash
script/clean
```

## Testing

The existing tests are all pytest-bdd functional tests located in [tests/features](tests/features).

## Pull requests

Any new functionality or bug fixes must have associated tests, in order to prevent future regressions.
