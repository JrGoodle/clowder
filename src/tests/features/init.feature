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
        And directory at .clowder is a git repository
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
        And directory at .clowder is a git repository
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
        And directory at .clowder is a git repository
        And repo at .clowder is on branch no-versions
        And repo at .clowder is clean
        And default clowder version is linked

    @success @cats
    Scenario: clowder init existing empty directory
        Given test directory is empty
        And created directory .clowder
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command succeeds
        And directory at .clowder is a git repository
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
        And directory at .clowder is not a git repository
        And something file exists in directory .clowder

    @fail @cats
    Scenario: clowder init existing non-symlink yaml file
        Given cats example non-symlink yaml file exists
        And .clowder directory doesn't exist
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml file exists
        And clowder.yaml is not a symlink

    @success @cats
    Scenario: clowder init existing symlink yaml file no .clowder directory
        Given .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yaml symlink pointing to something-to-link-to
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command succeeds
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml file exists
        And clowder.yaml is a symlink pointing to .clowder/clowder.yaml

    @fail @cats
    Scenario: clowder init existing ambiguous non-symlink yaml file, non-symlink yml file, no .clowder directory
        Given cats example ambiguous non-symlink yaml and yml files exist
        And .clowder directory doesn't exist
        And clowder.yaml and clowder.yml files exist
        And clowder.yaml and clowder.yml are not symlinks
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml and clowder.yml files exist
        And clowder.yaml and clowder.yml are not symlinks

    @fail @cats
    Scenario: clowder init existing ambiguous yaml symlink, non-symlink yml file, no .clowder directory
        Given cats example non-symlink yml file exists
        And .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yaml symlink pointing to something-to-link-to
        And clowder.yml file exists
        And clowder.yml is not a symlink
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yml file exists
        And clowder.yml is not a symlink
        And clowder.yaml is a symlink pointing to .clowder/clowder.yaml

    @success @cats
    Scenario: clowder init existing ambiguous yaml symlink, yml symlink, no .clowder directory
        Given .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yml and clowder.yaml symlinks pointing to something-to-link-to
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        # TODO: Should this actually be a failure???
        Then the command succeeds
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yml symlink doesn't exist
        And clowder.yaml is a symlink pointing to .clowder/clowder.yaml

    @fail @cats
    Scenario: clowder init existing .clowder file
        Given test directory is empty
        And created file .clowder in directory .
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder file exists
        And .clowder is not a directory
        And clowder.yaml and clowder.yml symlinks don't exist

    @fail @cats
    Scenario: clowder init existing .clowder symlink
        Given cats example clowder repo symlink exists
        And .clowder is a symlink
        And clowder.yaml and clowder.yml symlinks don't exist
        When I run 'clowder init https://github.com/jrgoodle/cats.git'
        Then the command fails
        And .clowder symlink exists
        And clowder.yaml and clowder.yml symlinks don't exist
