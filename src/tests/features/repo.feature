@cats @repo
Feature: clowder repo command

    @help
    Scenario: repo help in empty directory
        Given test directory is empty
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @help
    Scenario: repo help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @help
    Scenario: repo help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder repo -h' and 'clowder repo --help'
        Then the commands succeed

    @fail
    Scenario: repo add non-existing file
        Given cats example is initialized
        And .clowder/my-file file doesn't exist
        And repo at .clowder is clean
        When I run 'clowder repo add my-file'
        Then the command fails
        And .clowder/my-file file doesn't exist
        And repo at .clowder is clean

    Scenario: repo run create file
        Given cats example is initialized
        And .clowder/my-file file doesn't exist
        And repo at .clowder is clean
        When I run 'clowder repo run "touch my-file"'
        Then the command succeeds
        And .clowder/my-file file exists
        And repo at .clowder is dirty

    Scenario: repo run delete file
        Given cats example is initialized
        And created file my-file in directory .clowder
        And repo at .clowder has untracked file my-file
        And repo at .clowder is dirty
        When I run 'clowder repo run "rm my-file"'
        Then the command succeeds
        And my-file file doesn't exist in directory .clowder
        And repo at .clowder is clean

    Scenario: repo checkout
        Given cats example is initialized
        And repo at .clowder is on branch master
        And repo at .clowder has no local branch repo-test
        And repo at .clowder has remote branch repo-test
        When I run 'clowder repo checkout repo-test'
        Then the command succeeds
        And repo at .clowder has local branch repo-test
        And repo at .clowder is on branch repo-test

    @fail
    Scenario: repo checkout unknown branch
        Given cats example is initialized
        And repo at .clowder is on branch master
        And repo at .clowder has no local branch i-dont-exist
        And repo at .clowder has no remote branch i-dont-exist
        When I run 'clowder repo checkout i-dont-exist'
        Then the command fails
        And repo at .clowder has no local branch i-dont-exist
        And repo at .clowder has no remote branch i-dont-exist
        And repo at .clowder is on branch master

    Scenario: repo clean
        Given cats example is initialized
        And repo at .clowder is on branch master
        And created file my-staged-file in directory .clowder
        And repo at .clowder staged file my-staged-file
        And repo at .clowder is dirty
        When I run 'clowder repo clean'
        Then the command succeeds
        And repo at .clowder is clean
        And my-staged-file file doesn't exist in directory .clowder
        And repo at .clowder is on branch master

    Scenario: repo status
        Given cats example is initialized
        And created file my-staged-file in directory .clowder
        And repo at .clowder staged file my-staged-file
        And repo at .clowder is dirty
        When I run 'clowder repo status'
        Then the command succeeds
        And repo at .clowder is dirty
        And my-staged-file file exists in directory .clowder
        # TODO: check command output
