@branch @cats
Feature: clowder branch

    @help
    Scenario: branch help in empty directory
        Given test directory is empty
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @help
    Scenario: branch help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @help
    Scenario: branch help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder branch -h' and 'clowder branch --help'
        Then the commands succeed

    @offline
    Scenario: branch offline
        Given cats example is initialized and herded
        When the network connection is disabled
        And I run 'clowder branch'
        And I run 'clowder branch -a'
        And I run 'clowder branch -r'
        And the network connection is enabled
        Then the commands succeed

    @subdirectory
    Scenario: branch subdirectory
        Given cats example is initialized and herded
        When I change to directory mu
        And I run 'clowder branch'
        And I run 'clowder branch -a'
        And I run 'clowder branch -r'
        Then the commands succeed
