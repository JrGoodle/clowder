@prune @cats
Feature: clowder prune

    @help @success
    Scenario: clowder prune help in empty directory
        Given test directory is empty
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help @success
    Scenario: clowder prune help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help @success
    Scenario: clowder prune help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @default @success
    Scenario Outline: clowder prune default existing local branch checked out
        Given cats example is initialized and herded
        And project at <directory> created <local_branch>
        And project at <directory> checked out <local_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <local_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | mu                | shrubs       | knead      | shrubs       |
        | duke              | shrubs       | purr       | shrubs       |
        | black-cats/kishka | shrubs       | master     | shrubs       |
        | black-cats/kit    | shrubs       | master     | shrubs       |
        | black-cats/sasha  | shrubs       | master     | shrubs       |
        | black-cats/june   | shrubs       | master     | shrubs       |

    @default @success
    Scenario Outline: clowder prune default existing local branch checked out group selected
        Given cats example is initialized and herded
        And project at <directory> created <local_branch>
        And project at <directory> checked out <local_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has no local branch <local_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory | start_branch | end_branch | local_branch |
        | mu        | shrubs       | knead      | shrubs       |
        | duke      | shrubs       | purr       | shrubs       |

    @default @success
    Scenario Outline: clowder prune default existing local branch checked out group not selected
        Given cats example is initialized and herded
        And project at <directory> created <local_branch>
        And project at <directory> checked out <local_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has local branch <local_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | black-cats/kishka | shrubs       | shrubs     | shrubs       |
        | black-cats/kit    | shrubs       | shrubs     | shrubs       |
        | black-cats/sasha  | shrubs       | shrubs     | shrubs       |
        | black-cats/june   | shrubs       | shrubs     | shrubs       |

    @default @fail
    Scenario Outline: clowder prune default existing local branch checked out fail not fully merged
        Given cats example is initialized and herded
        And project at <directory> created <local_branch>
        And project at <directory> checked out <local_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs'
        Then the command fails
        And project at <directory> has local branch <local_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | mu                | shrubs       | knead      | shrubs       |
        | duke              | shrubs       | purr       | shrubs       |
        | black-cats/kishka | shrubs       | master     | shrubs       |
        | black-cats/kit    | shrubs       | master     | shrubs       |
        | black-cats/sasha  | shrubs       | master     | shrubs       |
        | black-cats/june   | shrubs       | master     | shrubs       |

    @default @success
    Scenario Outline: clowder prune force default existing local branch checked out not fully merged
        Given cats example is initialized and herded
        And project at <directory> created <local_branch>
        And project at <directory> checked out <local_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <start_branch>
        When I run 'clowder prune -f shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <local_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | local_branch |
        | mu                | shrubs       | knead      | shrubs       |
        | duke              | shrubs       | purr       | shrubs       |
        | black-cats/kishka | shrubs       | master     | shrubs       |
        | black-cats/kit    | shrubs       | master     | shrubs       |
        | black-cats/sasha  | shrubs       | master     | shrubs       |
        | black-cats/june   | shrubs       | master     | shrubs       |
