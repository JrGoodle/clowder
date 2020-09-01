@prune @cats
Feature: clowder prune

    @help @success
    Scenario: prune help in empty directory
        Given test directory is empty
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help @success
    Scenario: prune help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @help @success
    Scenario: prune help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder prune -h' and 'clowder prune --help'
        Then the commands succeed

    @success
    Scenario Outline: prune default existing local branch checked out
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | shrubs       | knead      | shrubs      |
        | duke              | shrubs       | purr       | shrubs      |
        | black-cats/kishka | shrubs       | master     | shrubs      |
        | black-cats/kit    | shrubs       | master     | shrubs      |
        | black-cats/sasha  | shrubs       | master     | shrubs      |
        | black-cats/june   | shrubs       | master     | shrubs      |

    @success
    Scenario Outline: prune default existing local branch checked out group selected
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory | start_branch | end_branch | test_branch |
        | mu        | shrubs       | knead      | shrubs      |
        | duke      | shrubs       | purr       | shrubs      |

    @success
    Scenario Outline: prune default existing local branch checked out group not selected
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs cats'
        Then the command succeeds
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | black-cats/kishka | shrubs       | shrubs     | shrubs      |
        | black-cats/kit    | shrubs       | shrubs     | shrubs      |
        | black-cats/sasha  | shrubs       | shrubs     | shrubs      |
        | black-cats/june   | shrubs       | shrubs     | shrubs      |

    @fail
    Scenario Outline: prune default existing local branch checked out fail not fully merged
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <start_branch>
        When I run 'clowder prune shrubs'
        Then the command fails
        And project at <directory> has local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | shrubs       | knead      | shrubs      |
        | duke              | shrubs       | purr       | shrubs      |
        | black-cats/kishka | shrubs       | master     | shrubs      |
        | black-cats/kit    | shrubs       | master     | shrubs      |
        | black-cats/sasha  | shrubs       | master     | shrubs      |
        | black-cats/june   | shrubs       | master     | shrubs      |

    @success
    Scenario Outline: prune force default existing local branch checked out not fully merged
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> created a new commit
        And project at <directory> is on <start_branch>
        When I run 'clowder prune -f shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | shrubs       | knead      | shrubs      |
        | duke              | shrubs       | purr       | shrubs      |
        | black-cats/kishka | shrubs       | master     | shrubs      |
        | black-cats/kit    | shrubs       | master     | shrubs      |
        | black-cats/sasha  | shrubs       | master     | shrubs      |
        | black-cats/june   | shrubs       | master     | shrubs      |

    @success @offline
    Scenario Outline: prune offline
        Given cats example is initialized and herded
        And project at <directory> created local branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <start_branch>
        When the network connection is disabled
        And I run 'clowder prune shrubs'
        Then the command succeeds
        And project at <directory> has no local branch <test_branch>
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch | test_branch |
        | mu                | shrubs       | knead      | shrubs      |
        | duke              | shrubs       | purr       | shrubs      |
        | black-cats/kishka | shrubs       | master     | shrubs      |
        | black-cats/kit    | shrubs       | master     | shrubs      |
        | black-cats/sasha  | shrubs       | master     | shrubs      |
        | black-cats/june   | shrubs       | master     | shrubs      |

    @fail @offline
    Scenario Outline: prune remote offline
        Given cats example is initialized and herded
#        And project at <directory> created remote branch <test_branch>
        When the network connection is disabled
        And I run 'clowder prune -r  pytest-prune-remote-offline'
        Then the command fails
#        And project at <directory> has remote branch <test_branch>


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
#        And project at <directory> created remote branch <test_branch>
        When the network connection is disabled
        And I run 'clowder prune -a pytest-prune-remote-offline'
        Then the command fails
        And project at <directory> has no local branch <test_branch>
#        And project at <directory> has remote branch <test_branch>

        Examples:
        | directory         | test_branch                 |
        | mu                | pytest-prune-remote-offline |
        | duke              | pytest-prune-remote-offline |
        | black-cats/kishka | pytest-prune-remote-offline |
        | black-cats/kit    | pytest-prune-remote-offline |
        | black-cats/sasha  | pytest-prune-remote-offline |
        | black-cats/june   | pytest-prune-remote-offline |
