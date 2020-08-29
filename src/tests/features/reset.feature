@reset @cats
Feature: clowder reset

    @help @success
    Scenario: clowder reset help in empty directory
        Given test directory is empty
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help @success
    Scenario: clowder reset help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help @success
    Scenario: clowder reset help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed
