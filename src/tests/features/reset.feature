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
        And did link test-empty-project clowder version
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @help @success
    Scenario: clowder reset help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder reset -h' and 'clowder reset --help'
        Then the commands succeed

    @success
    Scenario Outline: clowder reset behind
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

    @success
    Scenario Outline: clowder reset ahead
        Given cats example is initialized and herded
        And project at <directory> is ahead of upstream <start_branch> by <number_commits>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is in sync with upstream <start_branch>

        Examples:
        | directory         | start_branch | end_branch | number_commits |
        | mu                | knead        | knead      | 3              |
        | duke              | purr         | purr       | 2              |
        | black-cats/kishka | master       | master     | 3              |
        | black-cats/kit    | master       | master     | 1              |
        | black-cats/sasha  | master       | master     | 2              |
        | black-cats/june   | master       | master     | 5              |

    @success
    Scenario Outline: clowder reset behind ahead
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is in sync with upstream <start_branch>

        Examples:
        | directory         | start_branch | end_branch | number_behind | number_ahead |
        | mu                | knead        | knead      | 3             | 2            |
        | duke              | purr         | purr       | 2             | 1            |
        | black-cats/kishka | master       | master     | 3             | 1            |
        | black-cats/kit    | master       | master     | 1             | 3            |
        | black-cats/sasha  | master       | master     | 2             | 4            |
        | black-cats/june   | master       | master     | 5             | 1            |

    @success @parallel
    Scenario Outline: clowder reset behind parallel
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <start_branch> by <number_commits>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset --jobs 4'
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

    @success @parallel
    Scenario Outline: clowder reset ahead parallel
        Given cats example is initialized and herded
        And project at <directory> is ahead of upstream <start_branch> by <number_commits>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset --jobs 4'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is in sync with upstream <start_branch>

        Examples:
        | directory         | start_branch | end_branch | number_commits |
        | mu                | knead        | knead      | 3              |
        | duke              | purr         | purr       | 2              |
        | black-cats/kishka | master       | master     | 3              |
        | black-cats/kit    | master       | master     | 1              |
        | black-cats/sasha  | master       | master     | 2              |
        | black-cats/june   | master       | master     | 5              |

    @success @parallel
    Scenario Outline: clowder reset behind ahead parallel
        Given cats example is initialized and herded
        And project at <directory> is behind upstream <start_branch> by <number_behind> and ahead by <number_ahead>
        And project at <directory> is on <start_branch>
        When I run 'clowder reset --jobs 4'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is in sync with upstream <start_branch>

        Examples:
        | directory         | start_branch | end_branch | number_behind | number_ahead |
        | mu                | knead        | knead      | 3             | 2            |
        | duke              | purr         | purr       | 2             | 1            |
        | black-cats/kishka | master       | master     | 3             | 1            |
        | black-cats/kit    | master       | master     | 1             | 3            |
        | black-cats/sasha  | master       | master     | 2             | 4            |
        | black-cats/june   | master       | master     | 5             | 1            |
