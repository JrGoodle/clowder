@start @cats
Feature: clowder start

    @help @success
    Scenario: clowder start help in empty directory
        Given test directory is empty
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help @success
    Scenario: clowder start help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help @success
    Scenario: clowder start help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @default @success
    Scenario Outline: clowder start local
        Given cats example is initialized and herded
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | new-branch | new-branch  |
        | duke              | purr         | new-branch | new-branch  |
        | black-cats/kishka | master       | new-branch | new-branch  |
        | black-cats/kit    | master       | new-branch | new-branch  |
        | black-cats/sasha  | master       | new-branch | new-branch  |
        | black-cats/june   | master       | new-branch | new-branch  |

    @default @success
    Scenario Outline: clowder start local group excluded
        Given cats example is initialized and herded
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch black-cats'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | knead      | new-branch  |
        | duke              | purr         | purr       | new-branch  |

    @default @success
    Scenario Outline: clowder start local group included
        Given cats example is initialized and herded
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch black-cats'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | black-cats/kishka | master       | new-branch | new-branch  |
        | black-cats/kit    | master       | new-branch | new-branch  |
        | black-cats/sasha  | master       | new-branch | new-branch  |
        | black-cats/june   | master       | new-branch | new-branch  |
