@cats @checkout
Feature: clowder checkout command

    @help
    Scenario: checkout help in empty directory
        Given test directory is empty
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help
    Scenario: checkout help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help
    Scenario: checkout help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    Scenario Outline: checkout default existing local branch
        Given cats example is initialized and herded
        And project at <directory> created local <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout pytest-checkout'
        Then the command succeeds
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch     |
        | mu                | knead        | pytest-checkout |
        | duke              | purr         | pytest-checkout |
        | black-cats/kishka | master       | pytest-checkout |
        | black-cats/kit    | master       | pytest-checkout |
        | black-cats/sasha  | master       | pytest-checkout |
        | black-cats/june   | master       | pytest-checkout |

    @subdirectory
    Scenario Outline: checkout default existing local branch from subdirectory
        Given cats example is initialized and herded
        And project at <directory> created local <test_branch>
        And project at <directory> is on <start_branch>
        When I change to directory black-cats
        And I run 'clowder checkout pytest-checkout'
        Then the command succeeds
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch     |
        | mu                | knead        | pytest-checkout |
        | duke              | purr         | pytest-checkout |
        | black-cats/kishka | master       | pytest-checkout |
        | black-cats/kit    | master       | pytest-checkout |
        | black-cats/sasha  | master       | pytest-checkout |
        | black-cats/june   | master       | pytest-checkout |

    Scenario Outline: checkout default existing local branch for project
        Given cats example is initialized and herded
        And project at <directory> created local <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout pytest-checkout mu black-cats/june'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch      | test_branch     |
        | mu                | knead        | pytest-checkout | pytest-checkout |
        | duke              | purr         | purr            | pytest-checkout |
        | black-cats/kishka | master       | master          | pytest-checkout |
        | black-cats/kit    | master       | master          | pytest-checkout |
        | black-cats/sasha  | master       | master          | pytest-checkout |
        | black-cats/june   | master       | pytest-checkout | pytest-checkout |

    Scenario Outline: checkout default no local branch
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> has no local <test_branch>
        When I run 'clowder checkout pytest-checkout'
        Then the command succeeds
        And project at <directory> is on <start_branch>

        Examples:
        | directory         | start_branch | test_branch     |
        | mu                | knead        | pytest-checkout |
        | duke              | purr         | pytest-checkout |
        | black-cats/kishka | master       | pytest-checkout |
        | black-cats/kit    | master       | pytest-checkout |
        | black-cats/sasha  | master       | pytest-checkout |
        | black-cats/june   | master       | pytest-checkout |

    @offline
    Scenario Outline: checkout offline
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> created local <test_branch>
        When the network connection is disabled
        And I run 'clowder checkout pytest-checkout'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch     |
        | mu                | knead        | pytest-checkout |
        | duke              | purr         | pytest-checkout |
        | black-cats/kishka | master       | pytest-checkout |
        | black-cats/kit    | master       | pytest-checkout |
        | black-cats/sasha  | master       | pytest-checkout |
        | black-cats/june   | master       | pytest-checkout |
