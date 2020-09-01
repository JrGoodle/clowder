@branch @cats
Feature: clowder branch

    @help @success
    Scenario: clowder branch help in empty directory
        Given test directory is empty
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @help @success
    Scenario: clowder branch help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @help @success
    Scenario: clowder branch help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @success @offline
    Scenario: clowder branch offline
        Given cats example is initialized and herded
        And the network connection is disabled
        When I run 'clowder branch'
        And I run 'clowder branch -a'
        And I run 'clowder branch -r'
        Then the commands succeed
