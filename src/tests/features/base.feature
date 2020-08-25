@cats @base
Feature: Test clowder base command

    @help @success
    Scenario: Test clowder help in empty directory
        Given test directory is empty
        When I run commands 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run commands 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder help with valid clowder.yaml
        Given cats example is initialized
        When I run commands 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @success
    Scenario: Test clowder with no arguments in empty directory
        Given test directory is empty
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: Test clowder with no arguments with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: Test clowder with no arguments with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder'
        Then the command succeeds

    @success
    Scenario: Test clowder version in empty directory
        Given test directory is empty
        When I run commands 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @success
    Scenario: Test clowder version with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run commands 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @success
    Scenario: Test clowder version with valid clowder.yaml
        Given cats example is initialized
        When I run commands 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @fail
    Scenario: Test clowder fails with unknown argument
        Given test directory is empty
        When I run 'clowder cats'
        Then the command fails
