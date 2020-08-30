@stash @cats
Feature: clowder stash

    @help @success
    Scenario: clowder stash help in empty directory
        Given test directory is empty
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    @help @success
    Scenario: clowder stash help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    @help @success
    Scenario: clowder stash help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    @success
    Scenario Outline: clowder stash
        Given cats example is initialized and herded
        And created <file_name> in <directory>
        And project at <directory> staged <file_name>
        When I run 'clowder stash'
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | file_name |
        | mu                | secret    |
        | duke              | secret    |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |

    @success
    Scenario Outline: clowder stash groups included
        Given cats example is initialized and herded
        And created <file_name> in <directory>
        And project at <directory> staged <file_name>
        When I run 'clowder stash cats'
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | file_name |
        | mu                | secret    |
        | duke              | secret    |

    @success
    Scenario Outline: clowder stash groups excluded
        Given cats example is initialized and herded
        And created <file_name> in <directory>
        And project at <directory> staged <file_name>
        When I run 'clowder stash cats'
        Then the command succeeds
        And project at <directory> is dirty

        Examples:
        | directory         | file_name |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |
