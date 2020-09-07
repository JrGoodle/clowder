@clean @cats
Feature: clowder clean

    @help
    Scenario: clean help in empty directory
        Given test directory is empty
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    Scenario Outline: clean
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @offline
    Scenario Outline: clean offline
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When the network connection is disabled
        And I run 'clowder clean'
        And the network connection is enabled
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @subdirectory
    Scenario Outline: clean subdirectory
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I change to directory duke
        And I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

#        TODO: Add test for clean when directories are missing

    Scenario Outline: clean group included
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean black-cats'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean group excluded
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean black-cats'
        Then the command succeeds
        And <filename> exists in <directory>
        And project at <directory> is dirty
        And project at <directory> is on <branch>

        Examples:
        | directory | branch | filename      |
        | mu        | knead  | something.txt |
        | duke      | purr   | something.txt |

    Scenario Outline: clean projects included
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean mu duke'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory | branch | filename      |
        | mu        | knead  | something.txt |
        | duke      | purr   | something.txt |

    Scenario Outline: clean projects excluded
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        When I run 'clowder clean mu duke'
        Then the command succeeds
        And <filename> exists in <directory>
        And project at <directory> is dirty
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean ignores untracked directory
        Given cats example is initialized and herded
        And created <test_directory>
        And created <filename> in <test_directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean'
        Then the command succeeds
        And <filename> exists in <test_directory>
        And project at <directory> is dirty
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      | test_directory              |
        | mu                | knead  | something.txt | mu/something                |
        | duke              | purr   | something.txt | duke/something              |
        | black-cats/kishka | master | something.txt | black-cats/kishka/something |
        | black-cats/kit    | master | something.txt | black-cats/kit/something    |
        | black-cats/sasha  | master | something.txt | black-cats/sasha/something  |
        | black-cats/june   | master | something.txt | black-cats/june/something   |

    Scenario Outline: clean -d untracked directory
        Given cats example is initialized and herded
        And created <test_directory>
        And created <filename> in <test_directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -d'
        Then the command succeeds
        And <test_directory> doesn't exist
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      | test_directory              |
        | mu                | knead  | something.txt | mu/something                |
        | duke              | purr   | something.txt | duke/something              |
        | black-cats/kishka | master | something.txt | black-cats/kishka/something |
        | black-cats/kit    | master | something.txt | black-cats/kit/something    |
        | black-cats/sasha  | master | something.txt | black-cats/sasha/something  |
        | black-cats/june   | master | something.txt | black-cats/june/something   |

    Scenario Outline: clean ignores untracked git directory
        Given cats example is initialized and herded
        And cloned cats repo in <directory>
        And <test_directory> exists
        And <test_directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean'
        Then the command succeeds
        And <test_directory> exists
        And <test_directory> is a git repository
        And project at <directory> is dirty
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | test_directory         |
        | mu                | knead  | mu/cats                |
        | duke              | purr   | duke/cats              |
        | black-cats/kishka | master | black-cats/kishka/cats |
        | black-cats/kit    | master | black-cats/kit/cats    |
        | black-cats/sasha  | master | black-cats/sasha/cats  |
        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean -df untracked git directory
        Given cats example is initialized and herded
        And cloned cats repo in <directory>
        And <test_directory> exists
        And <test_directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -fd'
        Then the command succeeds
        And <test_directory> doesn't exist
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | test_directory         |
        | mu                | knead  | mu/cats                |
        | duke              | purr   | duke/cats              |
        | black-cats/kishka | master | black-cats/kishka/cats |
        | black-cats/kit    | master | black-cats/kit/cats    |
        | black-cats/sasha  | master | black-cats/sasha/cats  |
        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean -X only files ignored by git
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is clean
        When I run 'clowder clean -X'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename     |
        | mu                | knead  | ignored_file |
#        TODO: Set up other projects for this test
#        | duke              | purr   | duke/cats              |
#        | black-cats/kishka | master | black-cats/kishka/cats |
#        | black-cats/kit    | master | black-cats/kit/cats    |
#        | black-cats/sasha  | master | black-cats/sasha/cats  |
#        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean -X ignores files not ignored by git
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -X'
        Then the command succeeds
        And <filename> exists in <directory>
        And project at <directory> is dirty
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename    |
        | mu                | knead  | not_ignored |
        | duke              | purr   | not_ignored |
        | black-cats/kishka | master | not_ignored |
        | black-cats/kit    | master | not_ignored |
        | black-cats/sasha  | master | not_ignored |
        | black-cats/june   | master | not_ignored |

    Scenario Outline: clean ignores files ignored by git
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is clean
        When I run 'clowder clean'
        Then the command succeeds
        And <filename> exists in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename     |
        | mu                | knead  | ignored_file |
#        TODO: Set up other projects for this test
#        | duke              | purr   | duke/cats              |
#        | black-cats/kishka | master | black-cats/kishka/cats |
#        | black-cats/kit    | master | black-cats/kit/cats    |
#        | black-cats/sasha  | master | black-cats/sasha/cats  |
#        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean untracked file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean -x staged file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -x'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean -x untracked file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -x'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean -a untracked git directory
        Given cats example is initialized and herded
        And cloned cats repo in <directory>
        And <test_directory> exists
        And <test_directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -a'
        Then the command succeeds
        And <test_directory> doesn't exist
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | test_directory         |
        | mu                | knead  | mu/cats                |
        | duke              | purr   | duke/cats              |
        | black-cats/kishka | master | black-cats/kishka/cats |
        | black-cats/kit    | master | black-cats/kit/cats    |
        | black-cats/sasha  | master | black-cats/sasha/cats  |
        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean -a untracked file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -a'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean -a staged file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -a'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    Scenario Outline: clean -a files ignored by git
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> is on <branch>
        And project at <directory> is clean
        When I run 'clowder clean -a'
        Then the command succeeds
        And <filename> doesn't exist in <directory>
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename     |
        | mu                | knead  | ignored_file |
#        TODO: Set up other projects for this test
#        | duke              | purr   | duke/cats              |
#        | black-cats/kishka | master | black-cats/kishka/cats |
#        | black-cats/kit    | master | black-cats/kit/cats    |
#        | black-cats/sasha  | master | black-cats/sasha/cats  |
#        | black-cats/june   | master | black-cats/june/cats   |

    Scenario Outline: clean -a untracked directory
        Given cats example is initialized and herded
        And created <test_directory>
        And created <filename> in <test_directory>
        And project at <directory> is on <branch>
        And project at <directory> is dirty
        When I run 'clowder clean -a'
        Then the command succeeds
        And <test_directory> doesn't exist
        And project at <directory> is clean
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      | test_directory              |
        | mu                | knead  | something.txt | mu/something                |
        | duke              | purr   | something.txt | duke/something              |
        | black-cats/kishka | master | something.txt | black-cats/kishka/something |
        | black-cats/kit    | master | something.txt | black-cats/kit/something    |
        | black-cats/sasha  | master | something.txt | black-cats/sasha/something  |
        | black-cats/june   | master | something.txt | black-cats/june/something   |

    @write @ssh
    Scenario Outline: clean abort rebase in progress
        Given cats example is initialized and herded with ssh
        And cats example projects have tracking branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> on <test_branch> has rebase in progress
        And project at <directory> is dirty
        When I run 'clowder clean'
        Then the command succeeds
        And project at <directory> has no rebase in progress
        And project at <directory> is clean
        And project at <directory> is on <test_branch>

        Examples:
        | directory         | test_branch |
        | mu                | pytest      |
        | duke              | pytest      |
        | black-cats/kishka | pytest      |
        | black-cats/kit    | pytest      |
        | black-cats/sasha  | pytest      |
        | black-cats/june   | pytest      |
