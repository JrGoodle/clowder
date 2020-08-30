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
        And linked test-empty-project clowder version
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder init help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @success @cats
    Scenario: clowder init default
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command succeeds
        And .clowder directory is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And repo at .clowder has remote origin with url https://github.com/jrgoodle/cats.git
        And default clowder version is linked

    @success @cats @ssh
    Scenario: clowder init default
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init git@github.com:jrgoodle/cats.git'
        Then the command succeeds
        And .clowder directory is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And repo at .clowder has remote origin with url git@github.com:jrgoodle/cats.git
        And default clowder version is linked

    @success @cats
    Scenario: clowder init branch
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init https://github.com/jrgoodle/cats.git -b no-versions'
        Then the command succeeds
        And .clowder directory is a git repository
        And repo at .clowder is on branch no-versions
        And repo at .clowder is clean
        And default clowder version is linked

    @success @cats
    Scenario: clowder init existing empty directory
        Given test directory is empty
        And created directory .clowder
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command succeeds
        And .clowder directory is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And default clowder version is linked

    @fail @cats
    Scenario: clowder init existing directory with contents
        Given test directory is empty
        And created directory .clowder
        And created file something in directory .clowder
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And .clowder directory is not a git repository
        And something file exists in directory .clowder

    @fail @cats
    Scenario: clowder init non-symlink yaml file
        Given cats example non-symlink yaml file exists
        And .clowder directory doesn't exist
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And .clowder directory is a git repository
        And clowder.yaml file exists
        And clowder.yaml is not a symlink

