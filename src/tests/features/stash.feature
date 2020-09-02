@stash @cats
Feature: clowder stash

    @help
    Scenario: stash help in empty directory
        Given test directory is empty
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    @help
    Scenario: stash help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    @help
    Scenario: stash help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder stash -h' and 'clowder stash --help'
        Then the commands succeed

    Scenario Outline: stash
        Given cats example is initialized and herded
        And created <file_name> in <directory>
        And project at <directory> staged <file_name>
        And project at <directory> is dirty
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

    @offline
    Scenario Outline: stash offline
        Given cats example is initialized and herded
        And created <file_name> in <directory>
        And project at <directory> staged <file_name>
        And project at <directory> is dirty
        When the network connection is disabled
        And I run 'clowder stash'
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

    Scenario Outline: stash groups included
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

    Scenario Outline: stash groups excluded
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
