@cats @checkout
Feature: clowder checkout command

    @help @success
    Scenario: clowder checkout help in empty directory
        Given test directory is empty
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help @success
    Scenario: clowder checkout help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @help @success
    Scenario: clowder checkout help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder checkout -h' and 'clowder checkout --help'
        Then the commands succeed

    @default @success
    Scenario Outline: clowder checkout default existing local branch
        Given cats example is initialized and herded
        And project at <directory> has local branch <local_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | mu                | knead        | other      | other        |
        | duke              | purr         | other      | other        |

    @default @success
    Scenario Outline: clowder checkout default existing local branch for project
        Given cats example is initialized and herded
        And project at <directory> has local branch <local_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder checkout other mu'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | mu                | knead        | other      | other        |
        | duke              | purr         | purr       | other        |

    @default @success
    Scenario Outline: clowder checkout default no local branch
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        And project at <directory> has no local branch <local_branch>
        When I run 'clowder checkout other'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | black-cats/kishka | master       | master     | other        |
        | black-cats/kit    | master       | master     | other        |
        | black-cats/sasha  | master       | master     | other        |
        | black-cats/june   | master       | master     | other        |
