@init @debug
Feature: clowder init

    @help @cats
    Scenario: init help in empty directory
        Given test directory is empty
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @help @cats
    Scenario: init help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @help @cats
    Scenario: init help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder init -h' and 'clowder init --help'
        Then the commands succeed

    @cats
    Scenario: init default
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command succeeds
        And directory at .clowder is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And repo at .clowder has remote origin with url https://github.com/JrGoodle/cats.git
        And default clowder version is linked

    @cats @ssh
    Scenario: init default
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init git@github.com:JrGoodle/cats.git'
        Then the command succeeds
        And directory at .clowder is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And repo at .clowder has remote origin with url git@github.com:JrGoodle/cats.git
        And default clowder version is linked

    @cats
    Scenario: init branch
        Given .clowder directory doesn't exist
        And test directory is empty
        When I run 'clowder init https://github.com/JrGoodle/cats.git -b alt-branch'
        Then the command succeeds
        And directory at .clowder is a git repository
        And repo at .clowder is on branch alt-branch
        And repo at .clowder is clean
        And default clowder version is linked

    @cats
    Scenario: init existing empty directory
        Given test directory is empty
        And created directory .clowder
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command succeeds
        And directory at .clowder is a git repository
        And repo at .clowder is on branch master
        And repo at .clowder is clean
        And default clowder version is linked

    @fail @cats
    Scenario: init existing directory with contents
        Given test directory is empty
        And created directory .clowder
        And created file something in directory .clowder
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is not a git repository
        And something file exists in directory .clowder

    @fail @cats
    Scenario: init existing non-symlink yml file
        Given cats example non-symlink yml file exists
        And .clowder directory doesn't exist
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yml file exists
        And clowder.yml is not a symlink

    @cats
    Scenario: init existing symlink yaml file no .clowder directory
        Given .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yml symlink pointing to something-to-link-to
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command succeeds
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yml file exists
        And clowder.yml is a symlink pointing to .clowder/clowder.yml

    @fail @cats
    Scenario: init existing ambiguous non-symlink yaml file, non-symlink yml file, no .clowder directory
        Given cats example ambiguous non-symlink yaml and yml files exist
        And .clowder directory doesn't exist
        And clowder.yaml and clowder.yml files exist
        And clowder.yaml and clowder.yml are not symlinks
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml and clowder.yml files exist
        And clowder.yaml and clowder.yml are not symlinks

    @fail @cats
    Scenario: init existing ambiguous yaml symlink, non-symlink yml file, no .clowder directory
        Given cats example non-symlink yaml file exists
        And .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yml symlink pointing to something-to-link-to
        And clowder.yaml file exists
        And clowder.yaml is not a symlink
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml file exists
        And clowder.yaml is not a symlink
        And clowder.yml is a symlink pointing to .clowder/clowder.yml

    @cats
    Scenario: init existing ambiguous yaml symlink, yml symlink, no .clowder directory
        Given .clowder directory doesn't exist
        And created file something-to-link-to in directory .
        And created clowder.yml and clowder.yaml symlinks pointing to something-to-link-to
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        # TODO: Should this actually be a failure???
        Then the command succeeds
        And .clowder directory exists
        And directory at .clowder is a git repository
        And clowder.yaml symlink doesn't exist
        And clowder.yml is a symlink pointing to .clowder/clowder.yml

    @fail @cats
    Scenario: init existing .clowder file
        Given test directory is empty
        And created file .clowder in directory .
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder file exists
        And .clowder is not a directory
        And clowder.yaml and clowder.yml symlinks don't exist

    @fail @cats
    Scenario: init existing .clowder symlink
        Given cats example clowder repo symlink exists
        And .clowder is a symlink
        And clowder.yaml and clowder.yml symlinks don't exist
        When I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command fails
        And .clowder symlink exists
        And clowder.yaml and clowder.yml symlinks don't exist

    @fail @cats @offline
    Scenario: init offline
        Given .clowder directory doesn't exist
        And test directory is empty
        When the network connection is disabled
        And I run 'clowder init https://github.com/JrGoodle/cats.git'
        And the network connection is enabled
        Then the command fails
        And .clowder directory doesn't exist
        And clowder.yaml and clowder.yml symlinks don't exist
        And test directory is empty

    @cats @subdirectory
    Scenario: init subdirectory
        Given cats example is initialized and herded
        And mu/.clowder directory doesn't exist
        When I change to directory mu
        And I run 'clowder init https://github.com/JrGoodle/cats.git'
        Then the command succeeds
        And directory at mu/.clowder is a git repository
        And repo at mu/.clowder is on branch master
        And repo at mu/.clowder is clean
        And repo at mu/.clowder has remote origin with url https://github.com/JrGoodle/cats.git
#        FIXME: Allow checking this in other directories
#        And default clowder version is linked
