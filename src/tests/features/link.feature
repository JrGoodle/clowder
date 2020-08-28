@cats @link
Feature: clowder link command

    @help @success
    Scenario: clowder link help in empty directory
        Given test directory is empty
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help @success
    Scenario: clowder link help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help @success
    Scenario: clowder link help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @default @success
    Scenario: clowder link default version
        Given cats example is initialized
        And tags clowder version is linked
        When I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked

    @default @success
    Scenario: clowder link version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked

    @default @fail
    Scenario: clowder link no versions
        Given cats example is initialized to no-versions
        And default clowder version is linked
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked

    @default @fail
    Scenario: clowder link missing version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked
