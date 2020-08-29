@reset @cats
Feature: clowder reset

    @help @success
    Scenario: clowder reset help in empty directory
        Given test directory is empty
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help @success
    Scenario: clowder reset help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help @success
    Scenario: clowder reset help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @default @success @debug
    Scenario Outline: clowder reset
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <start_branch> by <number_commits>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is in sync with upstream <start_branch>

        Examples:
        | directory         | start_branch | end_branch | number_commits |
        | mu                | knead        | knead      | 3              |
        | duke              | purr         | purr       | 2              |
        | black-cats/kishka | master       | master     | 1              |
        | black-cats/kit    | master       | master     | 1              |
        | black-cats/sasha  | master       | master     | 1              |
        | black-cats/june   | master       | master     | 1              |
