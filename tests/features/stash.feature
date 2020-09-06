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
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is dirty
        When I run 'clowder stash'
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | filename |
        | mu                | secret    |
        | duke              | secret    |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |

    @subdirectory
    Scenario Outline: stash subdirectory
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is dirty
        When I change to directory mu
        And I run 'clowder stash'
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | filename |
        | mu                | secret    |
        | duke              | secret    |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |

    @offline
    Scenario Outline: stash offline
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is dirty
        When the network connection is disabled
        And I run 'clowder stash'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | filename |
        | mu                | secret    |
        | duke              | secret    |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |

    Scenario Outline: stash groups included
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        When I run 'clowder stash cats'
        Then the command succeeds
        And project at <directory> is clean

        Examples:
        | directory         | filename |
        | mu                | secret    |
        | duke              | secret    |

    Scenario Outline: stash groups excluded
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        When I run 'clowder stash cats'
        Then the command succeeds
        And project at <directory> is dirty

        Examples:
        | directory         | filename |
        | black-cats/kishka | secret    |
        | black-cats/kit    | secret    |
        | black-cats/sasha  | secret    |
        | black-cats/june   | secret    |
