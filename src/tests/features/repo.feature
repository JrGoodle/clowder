@cats @repo
Feature: clowder repo command

    @help @success
    Scenario: clowder repo help in empty directory
        Given test directory is empty
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @help @success
    Scenario: clowder repo help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @help @success
    Scenario: clowder repo help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @fail
    Scenario: clowder repo add non-existing file
        Given cats example is initialized
        And file .clowder/my-file doesn't exist
        And clowder repo is clean
        When I run 'clowder repo add my-file'
        Then the command fails
        And file .clowder/my-file doesn't exist
        And clowder repo is clean

    @success
    Scenario: clowder repo run create file
        Given cats example is initialized
        And file .clowder/my-file doesn't exist
        And clowder repo is clean
        When I run 'clowder repo run "touch my-file"'
        Then the command succeeds
        And file .clowder/my-file exists
        And clowder repo is dirty

    @success
    Scenario: clowder repo run delete file
        Given cats example is initialized
        And .clowder has untracked file my-file
        And file .clowder/my-file exists
        And clowder repo is dirty
        When I run 'clowder repo run "rm my-file"'
        Then the command succeeds
        And file .clowder/my-file doesn't exist
        And clowder repo is clean

    @success
    Scenario: clowder repo checkout
        Given cats example is initialized
        And project at .clowder is on branch master
        And project at .clowder has no local branch repo-test
        And project at .clowder has remote branch repo-test
        When I run 'clowder repo checkout repo-test'
        Then the command succeeds
        And project at .clowder has local branch repo-test
        And project at .clowder is on branch repo-test

    @fail
    Scenario: clowder repo checkout unknown branch
        Given cats example is initialized
        And project at .clowder is on branch master
        And project at .clowder has no local branch i-dont-exist
        And project at .clowder has no remote branch i-dont-exist
        When I run 'clowder repo checkout i-dont-exist'
        Then the command fails
        And project at .clowder has no local branch i-dont-exist
        And project at .clowder has no remote branch i-dont-exist
        And project at .clowder is on branch master

    @success
    Scenario: clowder repo clean
        Given cats example is initialized
        And project at .clowder is on branch master
        And .clowder has new staged file my-staged-file
        And file .clowder/my-staged-file exists
        And project at .clowder is dirty
        When I run 'clowder repo clean'
        Then the command succeeds
        And project at .clowder is clean
        And file .clowder/my-staged-file doesn't exist
        And project at .clowder is on branch master

    @success
    Scenario: clowder repo status
        Given cats example is initialized
        And .clowder has new staged file my-staged-file
        And project at .clowder is dirty
        When I run 'clowder repo status'
        Then the command succeeds
        And project at .clowder is dirty
        And file .clowder/my-staged-file exists
        # TODO: check command output
