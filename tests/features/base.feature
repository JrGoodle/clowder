@cats @base
Feature: clowder base command

    @help
    Scenario: help in empty directory
        Given test directory is empty
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help
    Scenario: help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    @help
    Scenario: help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder -h' and 'clowder --help'
        Then the commands succeed

    Scenario: with no arguments in empty directory
        Given test directory is empty
        When I run 'clowder'
        Then the command succeeds

    Scenario: with no arguments with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder'
        Then the command succeeds


    Scenario: with no arguments with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder'
        Then the command succeeds


    Scenario: version in empty directory
        Given test directory is empty
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed


    Scenario: version with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed


    Scenario: version with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder -v' and 'clowder --version'
        Then the commands succeed

    @fail
    Scenario: fails with unknown argument
        Given test directory is empty
        When I run 'clowder cats'
        Then the command fails
