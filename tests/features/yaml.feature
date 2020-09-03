@yaml @cats
Feature: clowder yaml

    @help
    Scenario: yaml help in empty directory
        Given test directory is empty
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    @help
    Scenario: yaml help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    @help
    Scenario: yaml help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    Scenario: yaml
        Given cats example is initialized and herded
        And yaml test files were copied to clowder directory
        When I run 'clowder yaml' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml.txt

    Scenario: yaml file
        Given cats example is initialized and herded
        And yaml test files were copied to clowder directory
        When I run 'clowder yaml -f' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml-f.txt

    Scenario: yaml resolved
        Given cats example is initialized and herded
        And yaml test files were copied to clowder directory
        When I run 'clowder yaml -r' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml-r.txt

    @subdirectory
    Scenario: yaml subdirectory
        Given cats example is initialized and herded
        And yaml test files were copied to clowder directory
        When I change to directory black-cats/kishka
        And I run 'clowder yaml' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml.txt

    @fail
    Scenario Outline: yaml resolved with missing repos
        Given cats example is initialized
        And <directory> doesn't exist
        When I run 'clowder yaml -r'
        Then the command fails
        And project at <directory> doesn't exist

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |
