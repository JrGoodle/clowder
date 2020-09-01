@cats @checkout
Feature: clowder checkout command

    @help @success
    Scenario: checkout help in empty directory
        Given test directory is empty
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help @success
    Scenario: checkout help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help @success
    Scenario: checkout help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @success
    Scenario Outline: checkout default existing local branch
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | other      | other       |
        | duke              | purr         | other      | other       |

    @success
    Scenario Outline: checkout default existing local branch for project
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other mu'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | other      | other       |
        | duke              | purr         | purr       | other       |

    @success
    Scenario Outline: checkout default no local branch
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> has no local branch <test_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | black-cats/kishka | master       | master     | other       |
        | black-cats/kit    | master       | master     | other       |
        | black-cats/sasha  | master       | master     | other       |
        | black-cats/june   | master       | master     | other       |

    @success @offline
    Scenario Outline: checkout offline
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> created local branch <test_branch>
        When the network connection is disabled
        And I run 'clowder checkout new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | new-branch | new-branch  |
        | duke              | purr         | new-branch | new-branch  |
