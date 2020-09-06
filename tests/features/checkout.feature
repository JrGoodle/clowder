@cats @checkout
Feature: clowder checkout command

    @help
    Scenario: checkout help in empty directory
        Given test directory is empty
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help
    Scenario: checkout help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help
    Scenario: checkout help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    Scenario Outline: checkout default existing local branch
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | other       |
        | duke              | purr         | other       |
        | black-cats/kishka | master       | other       |
        | black-cats/kit    | master       | other       |
        | black-cats/sasha  | master       | other       |
        | black-cats/june   | master       | other       |

    @subdirectory
    Scenario Outline: checkout default existing local branch from subdirectory
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I change to directory black-cats
        And I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | other       |
        | duke              | purr         | other       |
        | black-cats/kishka | master       | other       |
        | black-cats/kit    | master       | other       |
        | black-cats/sasha  | master       | other       |
        | black-cats/june   | master       | other       |

    Scenario Outline: checkout default existing local branch for project
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other mu black-cats/june'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | other      | other       |
        | duke              | purr         | purr       | other       |
        | black-cats/kishka | master       | master     | other       |
        | black-cats/kit    | master       | master     | other       |
        | black-cats/sasha  | master       | master     | other       |
        | black-cats/june   | master       | other      | other       |

    Scenario Outline: checkout default no local branch
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> has no local branch <test_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <start_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | other       |
        | duke              | purr         | other       |
        | black-cats/kishka | master       | other       |
        | black-cats/kit    | master       | other       |
        | black-cats/sasha  | master       | other       |
        | black-cats/june   | master       | other       |

    @offline
    Scenario Outline: checkout offline
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> created local branch <test_branch>
        When the network connection is disabled
        And I run 'clowder checkout new-branch'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |
