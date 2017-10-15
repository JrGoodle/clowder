# Contributing

## Getting Started

Clone the repository:

```bash
$ git clone git@github.com:JrGoodle/clowder.git
$ cd clowder
```

Add the directory you cloned the repo into to `PYTHONPATH` in your shell profile. For example, if cloned into `$HOME/clowder`

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/clowder
```

## Building

Install `clowder` for local development

```bash
$ script/update
```

Remove `clowder` and clean test directories

```bash
$ script/clean
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

## More info

### Commands

See the [clowder commands doc](docs/commands.md)
for documentation of all command options

For example output from individual commands see the [clowder command examples](docs#commands)

### The `clowder.yaml` file

See the [clowder.yaml doc](docs/clowder-yaml.md)
for an explanation of the `clowder.yaml` configuration file

### The clowder repo

See the [clowder repo doc](docs/clowder-repo.md)
for a description of the structure of the clowder repo cloned in the `.clowder` directory


### Using `clowder` with forks

See the [forks doc](docs/forks.md)
for a description of the behavior of `clowder` commands with forks

## Pull requests

Any new functionality or bug fixes must have associated tests, in order to prevent future regressions. There are a few Python unit tests, but the majority of the tests are located in bash scripts in [test/scripts](test/scripts)
