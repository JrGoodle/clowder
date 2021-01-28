@start @cats
Feature: clowder start

    @help
    Scenario: start help in empty directory
        Given test directory is empty
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help
    Scenario: start help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help
    Scenario: start help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    Scenario Outline: start local
        Given cats example is initialized and herded
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start i-dont-exist'
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | i-dont-exist |
        | duke              | purr         | i-dont-exist |
        | black-cats/kishka | master       | i-dont-exist |
        | black-cats/kit    | master       | i-dont-exist |
        | black-cats/sasha  | master       | i-dont-exist |
        | black-cats/june   | master       | i-dont-exist |

    @subdirectory
    Scenario Outline: start local subdirectory
        Given cats example is initialized and herded
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>
        And project at <directory> is on <start_branch>
        When I change to directory black-cats/sasha
        And I run 'clowder start i-dont-exist'
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | i-dont-exist |
        | duke              | purr         | i-dont-exist |
        | black-cats/kishka | master       | i-dont-exist |
        | black-cats/kit    | master       | i-dont-exist |
        | black-cats/sasha  | master       | i-dont-exist |
        | black-cats/june   | master       | i-dont-exist |

    @offline
    Scenario Outline: start local offline
        Given cats example is initialized and herded
        And project at <directory> has no remote <test_branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start i-dont-exist'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | i-dont-exist |
        | duke              | purr         | i-dont-exist |
        | black-cats/kishka | master       | i-dont-exist |
        | black-cats/kit    | master       | i-dont-exist |
        | black-cats/sasha  | master       | i-dont-exist |
        | black-cats/june   | master       | i-dont-exist |

    @fail @offline
    Scenario Outline: start tracking offline
        Given cats example is initialized and herded
        And project at <directory> has no remote <test_branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start -t i-dont-exist'
        And the network connection is enabled
        Then the command fails
        And project at <directory> has no local <test_branch>
        And project at <directory> is on <start_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | i-dont-exist |
        | duke              | purr         | i-dont-exist |
        | black-cats/kishka | master       | i-dont-exist |
        | black-cats/kit    | master       | i-dont-exist |
        | black-cats/sasha  | master       | i-dont-exist |
        | black-cats/june   | master       | i-dont-exist |

    Scenario Outline: start local group excluded
        Given cats example is initialized and herded
        And project at <directory> has no remote <test_branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start i-dont-exist black-cats'
        Then the command succeeds
        And project at <directory> is on <start_branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | i-dont-exist |
        | duke              | purr         | i-dont-exist |

    Scenario Outline: start local group included
        Given cats example is initialized and herded
        And project at <directory> has no remote <test_branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start i-dont-exist black-cats'
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | black-cats/kishka | master       | i-dont-exist |
        | black-cats/kit    | master       | i-dont-exist |
        | black-cats/sasha  | master       | i-dont-exist |
        | black-cats/june   | master       | i-dont-exist |

    # TODO: Probably need to create a fixture that sets up remote branches
    @internet @write @ssh @debug
    Scenario Outline: start tracking - no local, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> has local <test_branch>
        And project at <directory> has remote <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch         |
        | mu                | knead        | pytest-start-branch |
        | duke              | purr         | pytest-start-branch |
        | black-cats/kishka | master       | pytest-start-branch |
        | black-cats/kit    | master       | pytest-start-branch |
        | black-cats/sasha  | master       | pytest-start-branch |
        | black-cats/june   | master       | pytest-start-branch |

    @internet @write @fail @ssh
    Scenario Outline: start tracking - local exists not checked out, remote exists, no tracking
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> has no tracking <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch         |
        | mu                | knead        | pytest-start-branch |
#        FIXME: Because duke is first to run, it checks out the local branch then the command fails.
#        Probably should store the starting reference and restore it if the command fails, or
#        check if all projects have the right configuration
#        | duke              | purr         | pytest-start-branch |
        | black-cats/kishka | master       | pytest-start-branch |
        | black-cats/kit    | master       | pytest-start-branch |
        | black-cats/sasha  | master       | pytest-start-branch |
        | black-cats/june   | master       | pytest-start-branch |

    @internet @write @ssh
    Scenario Outline: start tracking - tracking exists, checked out
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | test_branch         |
        | mu                | pytest-start-branch |
        | duke              | pytest-start-branch |
        | black-cats/kishka | pytest-start-branch |
        | black-cats/kit    | pytest-start-branch |
        | black-cats/sasha  | pytest-start-branch |
        | black-cats/june   | pytest-start-branch |

    @internet @write @ssh
    Scenario Outline: start tracking - tracking exists, not checked out
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch         |
        | mu                | knead        | pytest-start-branch |
        | duke              | purr         | pytest-start-branch |
        | black-cats/kishka | master       | pytest-start-branch |
        | black-cats/kit    | master       | pytest-start-branch |
        | black-cats/sasha  | master       | pytest-start-branch |
        | black-cats/june   | master       | pytest-start-branch |

    @internet @write @fail @ssh @debug
    Scenario Outline: start tracking - no local, remote exists
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command fails
        And project at <directory> is on <start_branch>
        And project at <directory> has no tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch         |
        | mu                | knead        | pytest-start-branch |
#        FIXME: Because duke is first to run, it checks out the local branch then the command fails.
#        Probably should store the starting reference and restore it if the command fails, or
#        check if all projects have the right configuration before modifying branches
#        | duke              | purr         | pytest-start-branch |
        | black-cats/kishka | master       | pytest-start-branch |
        | black-cats/kit    | master       | pytest-start-branch |
        | black-cats/sasha  | master       | pytest-start-branch |
        | black-cats/june   | master       | pytest-start-branch |

    @internet @write @fail @ssh
    Scenario Outline: start tracking - local exists checked out, remote exists, no tracking
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> has no tracking <test_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | test_branch         |
        | mu                | pytest-start-branch |
        | duke              | pytest-start-branch |
        | black-cats/kishka | pytest-start-branch |
        | black-cats/kit    | pytest-start-branch |
        | black-cats/sasha  | pytest-start-branch |
        | black-cats/june   | pytest-start-branch |

    @internet @write @ssh
    Scenario Outline: start tracking - local exists checked out, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> has no tracking <test_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | test_branch         |
        | mu                | pytest-start-branch |
        | duke              | pytest-start-branch |
        | black-cats/kishka | pytest-start-branch |
        | black-cats/kit    | pytest-start-branch |
        | black-cats/sasha  | pytest-start-branch |
        | black-cats/june   | pytest-start-branch |

    @internet @write @ssh
    Scenario Outline: start tracking - local exists not checked out, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> is on <start_branch>
        And project at <directory> has no tracking <test_branch>
        When I run 'clowder start -t pytest-start-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch         |
        | mu                | knead        | pytest-start-branch |
        | duke              | purr         | pytest-start-branch |
        | black-cats/kishka | master       | pytest-start-branch |
        | black-cats/kit    | master       | pytest-start-branch |
        | black-cats/sasha  | master       | pytest-start-branch |
        | black-cats/june   | master       | pytest-start-branch |
