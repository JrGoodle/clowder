@reset @cats
Feature: clowder reset

    @help
    Scenario: reset help in empty directory
        Given test directory is empty
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help
    Scenario: reset help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help
    Scenario: reset help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    Scenario Outline: reset behind
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <test_branch> by <number_commits>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_commits |
        | mu                | knead       | 3              |
        | duke              | purr        | 2              |
        | black-cats/kishka | master      | 1              |
        | black-cats/kit    | master      | 1              |
        | black-cats/sasha  | master      | 1              |
        | black-cats/june   | master      | 1              |

    Scenario Outline: reset ahead
        Given cats example is initialized and herded
        And project at <directory> is ahead of upstream <test_branch> by <number_commits>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_commits |
        | mu                | knead       | 3              |
        | duke              | purr        | 2              |
        | black-cats/kishka | master      | 3              |
        | black-cats/kit    | master      | 1              |
        | black-cats/sasha  | master      | 2              |
        | black-cats/june   | master      | 5              |

    Scenario Outline: reset behind ahead
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_behind | number_ahead |
        | mu                | knead       | 3             | 2            |
        | duke              | purr        | 2             | 1            |
        | black-cats/kishka | master      | 3             | 1            |
        | black-cats/kit    | master      | 1             | 3            |
        | black-cats/sasha  | master      | 2             | 4            |
        | black-cats/june   | master      | 5             | 1            |

    @parallel
    Scenario Outline: reset behind parallel
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <test_branch> by <number_commits>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset --jobs 4'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_commits |
        | mu                | knead       | 3              |
        | duke              | purr        | 2              |
        | black-cats/kishka | master      | 1              |
        | black-cats/kit    | master      | 1              |
        | black-cats/sasha  | master      | 1              |
        | black-cats/june   | master      | 1              |

    @parallel
    Scenario Outline: reset ahead parallel
        Given cats example is initialized and herded
        And project at <directory> is ahead of upstream <test_branch> by <number_commits>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset --jobs 4'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_commits |
        | mu                | knead       | 3              |
        | duke              | purr        | 2              |
        | black-cats/kishka | master      | 3              |
        | black-cats/kit    | master      | 1              |
        | black-cats/sasha  | master      | 2              |
        | black-cats/june   | master      | 5              |

    @parallel
    Scenario Outline: reset behind ahead parallel
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead>
        And project at <directory> is on <test_branch>
        When I run 'clowder reset --jobs 4'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> is in sync with upstream <test_branch>

        Examples:
        | directory         | test_branch | number_behind | number_ahead |
        | mu                | knead       | 3             | 2            |
        | duke              | purr        | 2             | 1            |
        | black-cats/kishka | master      | 3             | 1            |
        | black-cats/kit    | master      | 1             | 3            |
        | black-cats/sasha  | master      | 2             | 4            |
        | black-cats/june   | master      | 5             | 1            |
