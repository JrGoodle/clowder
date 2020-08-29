@cats @base
Feature: clowder base command

    @help @success
    Scenario: clowder help in empty directory
        Given test directory is empty
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help @success
    Scenario: clowder help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help @success
    Scenario: clowder help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @success
    Scenario: clowder with no arguments in empty directory
        Given test directory is empty
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: clowder with no arguments with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: clowder with no arguments with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: clowder version in empty directory
        Given test directory is empty
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @success
    Scenario: clowder version with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @success
    Scenario: clowder version with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @fail
    Scenario: clowder fails with unknown argument
        Given test directory is empty
        When I run 'clowder cats'
        Then the command fails
