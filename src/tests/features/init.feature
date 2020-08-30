@init
Feature: clowder init

    @help @success @cats
    Scenario: clowder init help in empty directory
        Given test directory is empty
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder init help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder init help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @success @cats
    Scenario: clowder init default
        Given .clowder doesn't exist
        And test directory is empty
        When I run 'clowder init'
        Then the command succeeds
        And project at .clowder is a git repository
        And project at .clowder is on branch master
        And project at .clowder is clean
        And default clowder version is linked

    @success @cats
    Scenario: clowder init branch
        Given .clowder doesn't exist
        And test directory is empty
        When I run 'clowder init https://github.com/jrgoodle/cats.git -b no-versions'
        Then the command succeeds
        And project at .clowder is a git repository
        And project at .clowder is on branch no-versions
        And project at .clowder is clean
        And default clowder version is linked

    @success @cats
    Scenario: clowder init existing empty directory
        Given test directory is empty
        And did create directory .clowder
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command succeeds
        And project at .clowder is a git repository
        And project at .clowder is on branch master
        And project at .clowder is clean
        And default clowder version is linked

    @fail @cats
    Scenario: clowder init existing directory with contents
        Given test directory is empty
        And did create directory .clowder
        And did create file .clowder/something
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And project at .clowder is not a git repository
        And file .clowder/something exists

    @fail @cats
    Scenario: clowder init non-symlink yaml file
        Given cats example non-symlink yaml file exists
        And .clowder doesn't exist
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory doesn't exist
