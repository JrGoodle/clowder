# Contributing

## Getting Started

Clone the repository:

```bash
$ git clone git@github.com:JrGoodle/clowder.git
$ cd clowder
```

Add the directory you cloned the repo into to `PYTHONPATH` in your shell profile. For example, if cloned into `$HOME/clowder`

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/clowder/clowder
```

## Building

Install `clowder` for local development

```bash
$ script/update
```

Remove `clowder` and clean test directories

```bash
$ script/clean all
```

## Testing

Install `clowder-test` command runner

```bash
$ script/test
```

Run test scripts

```bash
$ clowder-test swift all
$ clowder-test cats herd
$ clowder-test unittests
```

## Pull requests

Any new functionality or bug fixes must have associated tests, in order to prevent future regressions. There are a few Python unit tests, but the majority of the tests are located in bash scripts in [test/scripts](test/scripts)
