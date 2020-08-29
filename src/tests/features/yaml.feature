@yaml @cats
Feature: clowder yaml

    @help @success
    Scenario: clowder yaml help in empty directory
        Given test directory is empty
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    @help @success
    Scenario: clowder yaml help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    @help @success
    Scenario: clowder yaml help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder yaml -h' and 'clowder yaml --help'
        Then the commands succeed

    @success
    Scenario: clowder yaml
        Given cats example is initialized and herded
        And yaml test files are in clowder directory
        When I run 'clowder yaml' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml.txt

    @success
    Scenario: clowder yaml file
        Given cats example is initialized and herded
        And yaml test files are in clowder directory
        When I run 'clowder yaml -f' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml-f.txt

    @success
    Scenario: clowder yaml resolved
        Given cats example is initialized and herded
        And yaml test files are in clowder directory
        When I run 'clowder yaml -r' without debug output
        Then the command succeeds
        And output matches contents of clowder-yaml-r.txt

    @fail
    Scenario Outline: clowder yaml resolved with missing repos
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
