@clean @cats
Feature: clowder clean

    @help
    Scenario: clean help in empty directory
        Given test directory is empty
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    Scenario Outline: clean
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @offline
    Scenario Outline: clean offline
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When the network connection is disabled
        And I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @subdirectory
    Scenario Outline: clean subdirectory
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I change to directory duke
        And I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

#        TODO: Add test for clean when directories are missing
