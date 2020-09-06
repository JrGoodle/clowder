@start @cats
Feature: clowder start

    @help
    Scenario: start help in empty directory
        Given test directory is empty
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help
    Scenario: start help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @help
    Scenario: start help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder start -h' and 'clowder start --help'
        Then the commands succeed

    @write @ssh
    Scenario Outline: start local
        Given cats example is initialized and herded with ssh
        And cats example projects have no local branch <test_branch>
        And cats example projects have no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @subdirectory @write @ssh
    Scenario Outline: start local subdirectory
        Given cats example is initialized and herded with ssh
        And cats example projects have no local branch <test_branch>
        And cats example projects have no remote branch <test_branch>
        And project at <directory> is on <start_branch>
        When I change to directory black-cats/sasha
        And I run 'clowder start new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @offline
    Scenario Outline: start local offline
        Given cats example is initialized and herded
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start new-branch'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @fail @offline
    Scenario Outline: start tracking offline
        Given cats example is initialized and herded
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder start -t new-branch'
        And the network connection is enabled
        Then the command fails
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <start_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @write @ssh
    Scenario Outline: start local group excluded
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch black-cats'
        Then the command succeeds
        And project at <directory> is on <start_branch>
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |

    @write @ssh
    Scenario Outline: start local group included
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start new-branch black-cats'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    # TODO: Probably need to create a fixture that sets up remote branches
    @internet @write @ssh
    Scenario Outline: start tracking - no local, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> has remote branch <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @internet @write @fail @ssh
    Scenario Outline: start tracking - local exists not checked out, remote exists, no tracking
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> has no tracking branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t new-branch'
        Then the command fails
        And project at <directory> is on <start_branch>
        And project at <directory> has no tracking branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
#        FIXME: Because duke is first to run, it checks out the local branch then the command fails.
#        Probably should store the starting reference and restore it if the command fails, or
#        check if all projects have the right configuration
#        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @internet @write @ssh
    Scenario Outline: start tracking - tracking exists, checked out
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | test_branch |
        | mu                | new-branch  |
        | duke              | new-branch  |
        | black-cats/kishka | new-branch  |
        | black-cats/kit    | new-branch  |
        | black-cats/sasha  | new-branch  |
        | black-cats/june   | new-branch  |

    @internet @write @ssh
    Scenario Outline: start tracking - tracking exists, not checked out
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @internet @write @fail @ssh
    Scenario Outline: start tracking - no local, remote exists
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder start -t new-branch'
        Then the command fails
        And project at <directory> is on <start_branch>
        And project at <directory> has no tracking branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
#        FIXME: Because duke is first to run, it checks out the local branch then the command fails.
#        Probably should store the starting reference and restore it if the command fails, or
#        check if all projects have the right configuration before modifying branches
#        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |

    @internet @write @fail @ssh
    Scenario Outline: start tracking - local exists checked out, remote exists, no tracking
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> has no tracking branch <test_branch>
        When I run 'clowder start -t new-branch'
        Then the command fails
        And project at <directory> is on <test_branch>
        And project at <directory> has no tracking branch <test_branch>

        Examples:
        | directory         | test_branch |
        | mu                | new-branch  |
        | duke              | new-branch  |
        | black-cats/kishka | new-branch  |
        | black-cats/kit    | new-branch  |
        | black-cats/sasha  | new-branch  |
        | black-cats/june   | new-branch  |

    @internet @write @ssh
    Scenario Outline: start tracking - local exists checked out, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> has no tracking branch <test_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | test_branch |
        | mu                | new-branch  |
        | duke              | new-branch  |
        | black-cats/kishka | new-branch  |
        | black-cats/kit    | new-branch  |
        | black-cats/sasha  | new-branch  |
        | black-cats/june   | new-branch  |

    @internet @write @ssh
    Scenario Outline: start tracking - local exists not checked out, no remote
        Given cats example is initialized and herded with ssh
        And cats example projects have no remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> is on <start_branch>
        And project at <directory> has no tracking branch <test_branch>
        When I run 'clowder start -t new-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking branch <test_branch>

        Examples:
        | directory         | start_branch | test_branch |
        | mu                | knead        | new-branch  |
        | duke              | purr         | new-branch  |
        | black-cats/kishka | master       | new-branch  |
        | black-cats/kit    | master       | new-branch  |
        | black-cats/sasha  | master       | new-branch  |
        | black-cats/june   | master       | new-branch  |
