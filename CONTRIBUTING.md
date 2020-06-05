# Contributing

## Getting Started

Clone the repository:

```bash
git clone git@github.com:JrGoodle/clowder.git
cd clowder
```

Add the directory you cloned the repo into to `PYTHONPATH` in your shell profile. For example, if cloned into `$HOME/clowder`

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/clowder/src/clowder
```

## Building

Install `clowder` for local development

```bash
script/update
```

Remove `clowder` and clean test directories

```bash
script/clean all
```

## Testing

Install `clowder-test` command runner

```bash
script/test
```

Run test scripts

```bash
clowder-test cats <option>
```

## Pull requests

Any new functionality or bug fixes must have associated tests, in order to prevent future regressions. As of now, the tests are all functional tests located in bash scripts in [test/scripts](test/scripts)
