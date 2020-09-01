@start @cats
Feature: clowder start

    @help @success
    Scenario: start help in empty directory
        Given test directory is empty
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help @success
    Scenario: start help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help @success
    Scenario: start help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @success
    Scenario Outline: start local
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

    # FIXME: Probably need to create a fixture that sets up remote branches
    @success @internet @write
    Scenario Outline: start tracking
        Given cats example is initialized and herded
        And project at <directory> deleted remote branch <test_branch>
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> has remote branch <test_branch>
        And project at <directory> is on <end_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | knead      | new-branch  |
        | duke              | purr         | purr       | new-branch  |
        | black-cats/kishka | master       | master     | new-branch  |
        | black-cats/kit    | master       | master     | new-branch  |
        | black-cats/sasha  | master       | master     | new-branch  |
        | black-cats/june   | master       | master     | new-branch  |

    @success @offline
    Scenario Outline: start local offline
        Given cats example is initialized and herded
#        And project at <directory> deleted remote branch <test_branch>
        And project at <directory> has no local branch <test_branch>
#        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>
#        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | new-branch | new-branch  |
        | duke              | purr         | new-branch | new-branch  |
        | black-cats/kishka | master       | new-branch | new-branch  |
        | black-cats/kit    | master       | new-branch | new-branch  |
        | black-cats/sasha  | master       | new-branch | new-branch  |
        | black-cats/june   | master       | new-branch | new-branch  |

    @fail @offline
    Scenario Outline: start tracking offline
        Given cats example is initialized and herded
#        And project at <directory> deleted remote branch <test_branch>
        And project at <directory> has no local branch <test_branch>
#        And project at <directory> has no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start -t new-branch'
        Then the command fails
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>
#        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | knead        | knead      | new-branch  |
        | duke              | purr         | purr       | new-branch  |
        | black-cats/kishka | master       | master     | new-branch  |
        | black-cats/kit    | master       | master     | new-branch  |
        | black-cats/sasha  | master       | master     | new-branch  |
        | black-cats/june   | master       | master     | new-branch  |

    @success
    Scenario Outline: start local group excluded
        Given cats example is initialized and herded
        And project at <directory> deleted remote branch <test_branch>
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

    @success
    Scenario Outline: start local group included
        Given cats example is initialized and herded
        And project at <directory> deleted remote branch <test_branch>
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
