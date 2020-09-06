@prune @cats
Feature: clowder prune

    @help
    Scenario: prune help in empty directory
        Given test directory is empty
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help
    Scenario: prune help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help
    Scenario: prune help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    Scenario Outline: prune default existing local branch checked out
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder prune shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | shrubs      | knead      |
        | duke              | shrubs      | purr       |
        | black-cats/kishka | shrubs      | master     |
        | black-cats/kit    | shrubs      | master     |
        | black-cats/sasha  | shrubs      | master     |
        | black-cats/june   | shrubs      | master     |

    @subdirectory
    Scenario Outline: prune default from subdirectory with existing local branch checked out
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I change to directory mu
        And I run 'clowder prune shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | shrubs      | knead      |
        | duke              | shrubs      | purr       |
        | black-cats/kishka | shrubs      | master     |
        | black-cats/kit    | shrubs      | master     |
        | black-cats/sasha  | shrubs      | master     |
        | black-cats/june   | shrubs      | master     |

    Scenario Outline: prune default existing local branch checked out group selected
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory | test_branch | end_branch |
        | mu        | shrubs      | knead      |
        | duke      | shrubs      | purr       |

    Scenario Outline: prune default existing local branch checked out group not selected
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | test_branch |
        | black-cats/kishka | shrubs      |
        | black-cats/kit    | shrubs      |
        | black-cats/sasha  | shrubs      |
        | black-cats/june   | shrubs      |

    @fail
    Scenario Outline: prune default existing local branch checked out fail not fully merged
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <test_branch>
        When I run 'clowder prune shrubs'
        Then the command fails
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | shrubs      | knead      |
        | duke              | shrubs      | purr       |
        | black-cats/kishka | shrubs      | master     |
        | black-cats/kit    | shrubs      | master     |
        | black-cats/sasha  | shrubs      | master     |
        | black-cats/june   | shrubs      | master     |

    Scenario Outline: prune force default existing local branch checked out not fully merged
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <test_branch>
        When I run 'clowder prune -f shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | shrubs      | knead      |
        | duke              | shrubs      | purr       |
        | black-cats/kishka | shrubs      | master     |
        | black-cats/kit    | shrubs      | master     |
        | black-cats/sasha  | shrubs      | master     |
        | black-cats/june   | shrubs      | master     |

    @offline
    Scenario Outline: prune offline
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When the network connection is disabled
        And I run 'clowder prune shrubs'
        And the network connection is enabled
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | shrubs      | knead      |
        | duke              | shrubs      | purr       |
        | black-cats/kishka | shrubs      | master     |
        | black-cats/kit    | shrubs      | master     |
        | black-cats/sasha  | shrubs      | master     |
        | black-cats/june   | shrubs      | master     |

    @fail @offline
    Scenario Outline: prune remote offline
        Given cats example is initialized and herded
        And project at <directory> created remote branch <test_branch>
        When the network connection is disabled
        And I run 'clowder prune -r  pytest-prune-remote-offline'
        And the network connection is enabled
        Then the command fails
        And project at <directory> has remote branch <test_branch>

        Examples:
        | directory         | test_branch                 |
        | mu                | pytest-prune-remote-offline |
        | duke              | pytest-prune-remote-offline |
        | black-cats/kishka | pytest-prune-remote-offline |
        | black-cats/kit    | pytest-prune-remote-offline |
        | black-cats/sasha  | pytest-prune-remote-offline |
        | black-cats/june   | pytest-prune-remote-offline |

    @fail @offline
    Scenario Outline: prune all offline
        Given cats example is initialized and herded
        And project at <directory> created remote branch <test_branch>
        When the network connection is disabled
        And I run 'clowder prune -a pytest-prune-all-offline'
        And the network connection is enabled
        Then the command fails
        And project at <directory> has no local branch <test_branch>
        And project at <directory> has remote branch <test_branch>

        Examples:
        | directory         | test_branch              |
        | mu                | pytest-prune-all-offline |
        | duke              | pytest-prune-all-offline |
        | black-cats/kishka | pytest-prune-all-offline |
        | black-cats/kit    | pytest-prune-all-offline |
        | black-cats/sasha  | pytest-prune-all-offline |
        | black-cats/june   | pytest-prune-all-offline |

    @internet @write @ssh
    Scenario Outline: prune remote no local branch
        Given cats example is initialized and herded with ssh
        And cats example projects have remote branch <test_branch>
        And cats example projects have no local branch <test_branch>
        When I run 'clowder prune -r  pytest-prune-remote'
        Then the command succeeds
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> has no local branch <test_branch>

        Examples:
        | directory         | test_branch         |
        | mu                | pytest-prune-remote |
        | duke              | pytest-prune-remote |
        | black-cats/kishka | pytest-prune-remote |
        | black-cats/kit    | pytest-prune-remote |
        | black-cats/sasha  | pytest-prune-remote |
        | black-cats/june   | pytest-prune-remote |

    @internet @write @ssh
    Scenario Outline: prune remote tracking branch
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> has local branch <test_branch>
        And project at <directory> has remote branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder prune -r  pytest-prune-remote'
        Then the command succeeds
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | test_branch         |
        | mu                | pytest-prune-remote |
        | duke              | pytest-prune-remote |
        | black-cats/kishka | pytest-prune-remote |
        | black-cats/kit    | pytest-prune-remote |
        | black-cats/sasha  | pytest-prune-remote |
        | black-cats/june   | pytest-prune-remote |

    @internet @write @ssh
    Scenario Outline: prune all
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> has local branch <test_branch>
        And project at <directory> has remote branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I run 'clowder prune -a  pytest-prune-all'
        Then the command succeeds
        And project at <directory> has no remote branch <test_branch>
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch      | end_branch |
        | mu                | pytest-prune-all | knead      |
        | duke              | pytest-prune-all | purr       |
        | black-cats/kishka | pytest-prune-all | master     |
        | black-cats/kit    | pytest-prune-all | master     |
        | black-cats/sasha  | pytest-prune-all | master     |
        | black-cats/june   | pytest-prune-all | master     |
