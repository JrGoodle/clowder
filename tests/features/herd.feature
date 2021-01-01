@herd
Feature: clowder herd

# TODO: Add parallel tests

    @help @cats
    Scenario: herd help in empty directory
        Given test directory is empty
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @help @cats
    Scenario: herd help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @help @cats
    Scenario: herd help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @cats @fail
    Scenario: herd missing clowder.yml
        Given test directory is empty
        When I run 'clowder herd'
        Then the command fails
        And test directory is empty

    @cats
    Scenario Outline: herd default
        Given cats example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> has tracking <branch>
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And project at <directory> has <remote> with <url>

        Examples:
        | directory         | branch | remote | url                                    |
        | mu                | knead  | origin | https://github.com/JrGoodle/mu.git     |
        | duke              | purr   | origin | https://github.com/JrGoodle/duke.git   |
        | black-cats/kishka | master | origin | https://github.com/JrGoodle/kishka.git |
        | black-cats/kit    | master | origin | https://github.com/JrGoodle/kit.git    |
        | black-cats/sasha  | master | origin | https://github.com/JrGoodle/sasha.git  |
        | black-cats/june   | master | origin | https://github.com/JrGoodle/june.git   |

    @cats @subdirectory
    Scenario Outline: herd subdirectory
        Given cats example is initialized and herded
        And project at <directory> created local <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is on <test_branch>
        When I change to directory black-cats
        And I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | test_branch | end_branch |
        | mu                | sub         | knead      |
        | duke              | sub         | purr       |
        | black-cats/kishka | sub         | master     |
        | black-cats/kit    | sub         | master     |
        | black-cats/sasha  | sub         | master     |
        | black-cats/june   | sub         | master     |

    @cats
    Scenario Outline: herd commits
        Given cats example is initialized
        And <directory> doesn't exist
        And linked static-refs clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | commit                                   |
        | mu                | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @cats
    Scenario Outline: herd tags
        Given cats example is initialized
        And <directory> doesn't exist
        And linked tags clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <tag>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | tag                   |
        | mu                | test-clowder-yaml-tag |
        | duke              | purr                  |
        | black-cats/kishka | v0.01                 |
        | black-cats/kit    | v0.01                 |
        | black-cats/sasha  | v0.01                 |
        | black-cats/june   | v0.01                 |

    @fail @cats
    Scenario Outline: clowder herd untracked file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> has untracked file <filename>
        And project at <directory> is on <branch>
        When I run 'clowder herd'
        Then the command fails
        And project at <directory> has untracked file <filename>
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @fail @cats
    Scenario Outline: Test clowder herd staged file
        Given cats example is initialized and herded
        And created <filename> in <directory>
        And project at <directory> staged <filename>
        And project at <directory> is dirty
        And project at <directory> is on <branch>
        When I run 'clowder herd'
        Then the command fails
        And project at <directory> is dirty
        And project at <directory> has staged <filename>
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | filename      |
        | mu                | knead  | something.txt |
        | duke              | purr   | something.txt |
        | black-cats/kishka | master | something.txt |
        | black-cats/kit    | master | something.txt |
        | black-cats/sasha  | master | something.txt |
        | black-cats/june   | master | something.txt |

    @cats
    Scenario Outline: herd from detached HEAD
        Given cats example is initialized and herded
        And project at <directory> checked out detached HEAD behind <branch>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

#    FIXME: Implement this
#    @fail @cats
#    Scenario: Test clowder herd rebase in progress
#        Given cats example is initialized and herded
#        And created file something.txt in directory mu
#        And project at mu staged file something.txt
#        When I run 'clowder herd'
#        Then the command fails
##        And project at mu has staged file something.txt
#        And project at mu is dirty

#    TODO: Probably should come up with a better test for this (i.e. save a new version and its commit hashes
#    and then herd and check them in the Then section
    @cats
    Scenario Outline: herd previously saved version
        Given cats example is initialized
        And <directory> doesn't exist
        And linked v0.1 clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | commit                                   |
        | mu                | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | f2e20031ddce5cb097105f4d8ccbc77f4ac20709 |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @submodules @cats @debug
    Scenario Outline: herd submodules recursive enabled directories
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists

        Examples:
        | directory         |
        | mu                |
        | mu/ash            |
        | mu/ash/duffy      |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @submodules @cats
    Scenario Outline: herd submodules recursive enabled git projects
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is clean

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @submodules @cats
    Scenario Outline: herd submodules recursive enabled check submodules
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is clean
        And project at <directory> has submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> has been initialized
#       TODO: Check submodule url

        Examples:
        | directory     | submodule_path |
        | mu            | ash            |

    @submodules @cats
    Scenario Outline: herd submodules recursive enabled check recursive submodules
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is clean
#       TODO: Better recursize submodule check
        And project at <directory> has no submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> has been initialized
#       TODO: Check submodule url

        Examples:
        | directory     | submodule_path |
        | mu            | ash/duffy      |

    @submodules @cats
    Scenario Outline: herd submodules disabled check non-submodules exist
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules-no-recurse clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is clean

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @submodules @cats
    Scenario Outline: herd submodules disabled check submodules don't exist
        Given cats example is initialized
        And <directory> doesn't exist
        And linked submodules-no-recurse clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> has submodule at <submodule_path>
#       TODO: Check submodule url
        And submodule in <directory> at <submodule_path> hasn't been initialized

        Examples:
        | directory | submodule_path |
        | mu        | ash            |

    # TODO: Add tests for groups/projects
    @misc @upstream @ssh
    Scenario Outline: herd upstream remote urls ssh defaults
        Given misc example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> has <remote> with <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | git@github.com:JrGoodle/djinni.git                 |
        | djinni    | master      | upstream | git@github.com:dropbox/djinni.git                  |
        | gyp       | fork-branch | origin   | git@github.com:JrGoodle/gyp.git                    |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | git@github.com:JrGoodle/sox.git                    |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    # TODO: Add tests for groups/projects
    @misc @upstream
    Scenario Outline: herd upstream remote urls https defaults
        Given misc example is initialized
        And linked https clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> has <remote> with <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | https://github.com/JrGoodle/djinni.git             |
        | djinni    | master      | upstream | https://github.com/dropbox/djinni.git              |
        | gyp       | fork-branch | origin   | https://github.com/JrGoodle/gyp.git                |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | https://github.com/JrGoodle/sox.git                |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    # TODO: Add tests for groups/projects
    @misc @upstream @ssh
    Scenario Outline: herd upstream remote urls override ssh command line
        Given misc example is initialized
        And linked https clowder version
        And <directory> doesn't exist
        When I run 'clowder herd -p ssh'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> has <remote> with <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | git@github.com:JrGoodle/djinni.git                 |
        | djinni    | master      | upstream | git@github.com:dropbox/djinni.git                  |
        | gyp       | fork-branch | origin   | git@github.com:JrGoodle/gyp.git                    |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | git@github.com:JrGoodle/sox.git                    |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    # TODO: Add tests for groups/projects
    @misc @upstream
    Scenario Outline: herd upstream remote urls override https command line
        Given misc example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd -p https'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> has <remote> with <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | https://github.com/JrGoodle/djinni.git             |
        | djinni    | master      | upstream | https://github.com/dropbox/djinni.git              |
        | gyp       | fork-branch | origin   | https://github.com/JrGoodle/gyp.git                |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | https://github.com/JrGoodle/sox.git                |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    # TODO: Add tests for logic renaming remotes

    @misc @upstream
    Scenario: herd project with branch behind upstream
        Given misc example is initialized and herded with https
        And project at gyp is on branch fork-branch
        And project at gyp is on commit bd11dd1c51ef17592384df927c47023071639f96
        When I change to directory gyp
        And I run 'git pull upstream master'
        Then the command succeeds
        And project at gyp is not on commit bd11dd1c51ef17592384df927c47023071639f96
        And project at gyp is on branch fork-branch

    @cats
    Scenario Outline: herd non-symlink yaml file
        Given cats example non-symlink yaml file exists
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd groups default included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu-cat            | knead  |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd groups default excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory |
        | mu        |
        | duke      |

    @cats
    Scenario Outline: herd group black-cats included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd black-cats'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd group black-cats excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd black-cats'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory |
        | mu        |
        | duke      |
        | mu-cat    |

    @cats
    Scenario Outline: herd group cats included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd cats'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory | branch |
        | mu        | knead  |
        | duke      | purr   |
        | mu-cat    | knead  |

    @cats
    Scenario Outline: herd group cats excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd cats'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory         |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @cats
    Scenario Outline: herd groups "cats black-cats"
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd cats black-cats'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | mu-cat            | knead  |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd project name JrGoodle/mu included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd JrGoodle/mu'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory | branch |
        | mu        | knead  |
        | mu-cat    | knead  |

    @cats
    Scenario Outline: herd project name JrGoodle/mu excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd JrGoodle/mu'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory         |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @cats
    Scenario Outline: herd project path mu included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd mu'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory | branch |
        | mu        | knead  |

    @cats
    Scenario Outline: herd project path mu excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd mu'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory         |
        | mu-cat            |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @cats
    Scenario Outline: herd groups "all notdefault"
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd all notdefault'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | mu-cat            | knead  |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd groups "notdefault" included
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd notdefault'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory | branch |
        | mu        | knead  |
        | duke      | purr   |

    @cats
    Scenario Outline: herd groups "notdefault" excluded
        Given cats example is initialized
        And linked groups clowder version
        And <directory> doesn't exist
        When I run 'clowder herd notdefault'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory         |
        | mu-cat            |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @fail @cats @offline
    Scenario Outline: herd default offline
        Given cats example is initialized
        And <directory> doesn't exist
        When the network connection is disabled
        And I run 'clowder herd'
        And the network connection is enabled
        Then the command fails
        And <directory> doesn't exist

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/kishka |
        | black-cats/kit    |
        | black-cats/sasha  |
        | black-cats/june   |

    @cats @internet @write @ssh
    Scenario Outline: herd rebase with conflict
        Given cats example is initialized and herded with ssh
        And linked test-branch-ssh clowder version
        And cats example projects have tracking branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead> with conflict
        When I run 'clowder herd -r'
        Then the command fails
        And project at <directory> has rebase in progress

        Examples:
        | directory         | test_branch | number_behind | number_ahead |
        | mu                | pytest      | 1             | 3            |
        | duke              | pytest      | 2             | 3            |
        | black-cats/kishka | pytest      | 1             | 3            |
        | black-cats/kit    | pytest      | 2             | 3            |
        | black-cats/sasha  | pytest      | 1             | 3            |
        | black-cats/june   | pytest      | 2             | 3            |

    @cats
    Scenario Outline: herd saved version after init
        Given cats example is initialized
        And linked v0.1 clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | commit                                   |
        | mu                | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | f2e20031ddce5cb097105f4d8ccbc77f4ac20709 |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @cats
    Scenario Outline: herd with missing default branch
        Given cats example is initialized and herded
        And project at <directory> checked out detached HEAD behind <branch>
        And project at <directory> deleted local <branch>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kit    | master |
        | black-cats/kishka | master |
        | black-cats/june   | master |
        | black-cats/sasha  | master |

    @cats @fail
    Scenario Outline: herd yaml configured with non-existent remote branch
        Given cats example is initialized
        And linked non-existent-branch clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command fails
        And <directory> doesn't exist

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/kit    |
        | black-cats/kishka |
        | black-cats/june   |
        | black-cats/sasha  |

#    # FIXME: Need to fetch before anything else to update remote branches that don't exist anymore
#    @cats @write @ssh
#    Scenario Outline: herd yaml configured with non-existent remote branch, but local branch exists
#        Given cats example is initialized and herded with ssh
#        And cats example projects have no remote branch <test_branch>
#        And cats example projects have local branch <test_branch>
#        And linked test-branch-ssh clowder version
#        And project at <directory> is on <start_branch>
#        When I run 'clowder herd'
#        Then the command succeeds
#        And project at <directory> is on <test_branch>
#        And project at <directory> has no remote <test_branch>
#
#        Examples:
#        | directory         | start_branch | test_branch  |
#        | mu                | knead        | pytest       |
#        | duke              | purr         | pytest       |
#        | black-cats/kit    | master       | pytest       |
#        | black-cats/kishka | master       | pytest       |
#        | black-cats/june   | master       | pytest       |
#        | black-cats/sasha  | master       | pytest       |

    @cats @write @ssh
    Scenario Outline: herd local exists, remote exists, no tracking, same commit
        Given cats example is initialized and herded with ssh
        And linked test-branch-ssh clowder version
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> has no tracking <test_branch>
        And project at <directory> is on <start_branch>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | start_branch | test_branch  |
        | mu                | knead        | pytest       |
        | duke              | purr         | pytest       |
        | black-cats/kit    | master       | pytest       |
        | black-cats/kishka | master       | pytest       |
        | black-cats/june   | master       | pytest       |
        | black-cats/sasha  | master       | pytest       |

#    FIXME: Needs correct implementation
#    @cats @fail @write @ssh
#    Scenario Outline: herd local exists, remote exists, no tracking, different commits
#        Given cats example is initialized and herded with ssh
#        And linked test-branch-ssh clowder version
#        And cats example projects have remote branch <test_branch>
#        And cats example projects have local branch <test_branch>
#        And project at <directory> has no tracking <test_branch>
#        And project at <directory> is on <start_branch>
#        When I run 'clowder herd'
#        Then the command succeeds
#        And project at <directory> is on <test_branch>
#        And project at <directory> has tracking <test_branch>
#
#        Examples:
#        | directory         | start_branch | test_branch  |
#        | mu                | knead        | pytest       |
#        | duke              | purr         | pytest       |
#        | black-cats/kit    | master       | pytest       |
#        | black-cats/kishka | master       | pytest       |
#        | black-cats/june   | master       | pytest       |
#        | black-cats/sasha  | master       | pytest       |

    @cats @debug
    Scenario Outline: herd after clean herd
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And project at <directory> is clean
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @cats
    Scenario Outline: herd with rebase - check commit messages before and after
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And project at <directory> is behind upstream <branch> by <number_behind> and ahead by <number_ahead>
        When I run 'clowder herd -r'
        Then the command succeeds
        And project at <directory> has rebased commits in <branch> in the correct order
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | number_behind | number_ahead |
        | mu                | knead  | 2             | 1            |
        | duke              | purr   | 1             | 2            |
        | black-cats/kishka | master | 2             | 1            |
        | black-cats/kit    | master | 1             | 2            |
        | black-cats/sasha  | master | 2             | 1            |
        | black-cats/june   | master | 1             | 2            |

    @cats @lfs @debug
    Scenario Outline: herd lfs initial
        Given cats example is initialized
        And linked lfs clowder version
        And lfs is not installed
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And project at <directory> has lfs installed
        And <filename> exists in <directory>
        And <filename> in <directory> is not an lfs pointer

        Examples:
        | directory | branch | filename     |
        | mu        | lfs    | jrgoodle.png |

    @cats @lfs
    Scenario Outline: herd lfs different branch
        Given cats example is initialized and herded
        And linked lfs clowder version
        And project at <directory> doesn't have lfs installed
        And project at <directory> is on <start_branch>
        And <filename> doesn't exist in <directory>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <end_branch>
        And project at <directory> is clean
        And project at <directory> has lfs installed
        And <filename> exists in <directory>
        And <filename> in <directory> is not an lfs pointer

        Examples:
        | directory | start_branch | end_branch | filename     |
        | mu        | knead        | lfs        | jrgoodle.png |

    @cats @lfs
    Scenario Outline: herd lfs same branch
        Given cats example is initialized and herded
        And linked lfs clowder version
        And project at <directory> doesn't have lfs installed
        And project at <directory> checked out <branch>
        And <filename> in <directory> is an lfs pointer
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And project at <directory> has lfs installed
        And <filename> exists in <directory>
        And <filename> in <directory> is not an lfs pointer

        Examples:
        | directory | branch     | filename     |
        | mu        | lfs        | jrgoodle.png |

    @cats @debug
    Scenario Outline: herd install custom git config alias
        Given cats example is initialized and herded
        And linked git-config clowder version
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And <filename> doesn't exist in <directory>
        When I run 'clowder herd'
        And I change to <directory>
        And I run 'git something'
        Then the commands succeed
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And project at <directory> has untracked files
        And <filename> exists in <directory>

        Examples:
        | directory | branch | filename  |
        | mu        | knead  | something |

#   TODO: Check that 'git herd' only herds a single repo
    @cats
    Scenario Outline: herd with git herd alias
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And linked static-refs clowder version
        When I change to <directory>
        And I run 'git herd'
        Then the command succeeds
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | branch | commit                                   |
        | mu                | knead  | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | purr   | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | master | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | master | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | master | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | master | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @cats @debug
    Scenario Outline: herd with git herd alias only applies to one repo - included - mu
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And linked static-refs clowder version
        When I change to directory mu
        And I run 'git herd'
        Then the command succeeds
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory | branch | commit                                   |
        | mu        | knead  | cddce39214a1ae20266d9ee36966de67438625d1 |

    @cats
    Scenario Outline: herd with git herd alias only applies to one repo - excluded - mu
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And linked static-refs clowder version
        When I change to directory mu
        And I run 'git herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | duke              | purr   |
        | black-cats/kit    | master |
        | black-cats/kishka | master |
        | black-cats/june   | master |
        | black-cats/sasha  | master |

    @cats
    Scenario Outline: herd with git herd alias only applies to one repo - included - kishka
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And linked static-refs clowder version
        When I change to directory black-cats/kishka
        And I run 'git herd'
        Then the command succeeds
        And project at <directory> is on <commit>
        And project at <directory> has detached HEAD
        And project at <directory> is clean

        Examples:
        | directory         | branch | commit                                   |
        | black-cats/kishka | master | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |

    @cats
    Scenario Outline: herd with git herd alias only applies to one repo - excluded - kishka
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And linked static-refs clowder version
        When I change to directory black-cats/kishka
        And I run 'git herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kit    | master |
        | black-cats/june   | master |
        | black-cats/sasha  | master |

    @cats
    Scenario Outline: herd branch - no repo, existing remote branch
        Given cats example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd -b herd-branch'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> has tracking <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> is clean
        And project at <directory> has no local <branch>
        And project at <directory> has remote <branch>

        Examples:
        | directory         | branch | test_branch |
        | mu                | knead  | herd-branch |
        | duke              | purr   | herd-branch |
        | black-cats/kit    | master | herd-branch |
        | black-cats/kishka | master | herd-branch |
        | black-cats/june   | master | herd-branch |
        | black-cats/sasha  | master | herd-branch |

    @cats
    Scenario Outline: herd branch - no repo, no existing remote branch
        Given cats example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd -b herd-missing-branch'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> has tracking <branch>
        And project at <directory> is on <branch>
        And project at <directory> is clean
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>

        Examples:
        | directory         | branch | test_branch         |
        | mu                | knead  | herd-missing-branch |
        | duke              | purr   | herd-missing-branch |
        | black-cats/kit    | master | herd-missing-branch |
        | black-cats/kishka | master | herd-missing-branch |
        | black-cats/june   | master | herd-missing-branch |
        | black-cats/sasha  | master | herd-missing-branch |

    @cats
    Scenario Outline: herd branch - no local branch, existing remote branch
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> has remote <test_branch>
        When I run 'clowder herd -b herd-branch'
        Then the command succeeds
        And project at <directory> has tracking <test_branch>
        And project at <directory> is on <test_branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | test_branch |
        | mu                | knead  | herd-branch |
        | duke              | purr   | herd-branch |
        | black-cats/kit    | master | herd-branch |
        | black-cats/kishka | master | herd-branch |
        | black-cats/june   | master | herd-branch |
        | black-cats/sasha  | master | herd-branch |

    @cats
    Scenario Outline: herd branch - no local branch, no remote branch
        Given cats example is initialized and herded
        And project at <directory> is on <branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>
        When I run 'clowder herd -b herd-missing-branch'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> has no local <test_branch>
        And project at <directory> has no remote <test_branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | test_branch         |
        | mu                | knead  | herd-missing-branch |
        | duke              | purr   | herd-missing-branch |
        | black-cats/kit    | master | herd-missing-branch |
        | black-cats/kishka | master | herd-missing-branch |
        | black-cats/june   | master | herd-missing-branch |
        | black-cats/sasha  | master | herd-missing-branch |

    @cats
    Scenario Outline: herd branch - existing local branch, no remote branch
        Given cats example is initialized and herded
        And project at <directory> created local <test_branch>
        And project at <directory> is on <branch>
        And project at <directory> has local <test_branch>
        And project at <directory> has no remote <test_branch>
        When I run 'clowder herd -b herd-missing-branch'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has no remote <test_branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | test_branch         |
        | mu                | knead  | herd-missing-branch |
        | duke              | purr   | herd-missing-branch |
        | black-cats/kit    | master | herd-missing-branch |
        | black-cats/kishka | master | herd-missing-branch |
        | black-cats/june   | master | herd-missing-branch |
        | black-cats/sasha  | master | herd-missing-branch |

#   TODO: Add actual check for same commit
    @cats @write @ssh
    Scenario Outline: herd branch - local exists, remote exists, no tracking, same commit
        Given cats example is initialized and herded with ssh
        And linked test-branch-ssh clowder version
        And cats example projects have remote branch <test_branch>
        And cats example projects have local branch <test_branch>
        And project at <directory> has no tracking <test_branch>
        And project at <directory> is on <branch>
        When I run 'clowder herd -b pytest'
        Then the command succeeds
        And project at <directory> is on <test_branch>
        And project at <directory> has tracking <test_branch>

        Examples:
        | directory         | branch | test_branch         |
        | mu                | knead  | pytest              |
        | duke              | purr   | pytest              |
        | black-cats/kit    | master | pytest              |
        | black-cats/kishka | master | pytest              |
        | black-cats/june   | master | pytest              |
        | black-cats/sasha  | master | pytest              |

#    TODO: Implement this and add tests for behind, ahead, behind/ahead
#    @cats @write @ssh
#    Scenario Outline: herd branch - local exists, remote exists, no tracking, different commits
#        Given cats example is initialized and herded with ssh
#        And linked test-branch-ssh clowder version
#        And cats example projects have remote branch <test_branch>
#        And cats example projects have local branch <test_branch>
#        And project at <directory> has no tracking <test_branch>
#        And project at <directory> is on <branch>
#        When I run 'clowder herd -b pytest'
#        Then the command succeeds
#        And project at <directory> is on <test_branch>
#        And project at <directory> has tracking <test_branch>
#
#        Examples:
#        | directory         | branch | test_branch         |
#        | mu                | knead  | pytest              |
#        | duke              | purr   | pytest              |
#        | black-cats/kit    | master | pytest              |
#        | black-cats/kishka | master | pytest              |
#        | black-cats/june   | master | pytest              |
#        | black-cats/sasha  | master | pytest              |

    @cats @internet
    Scenario Outline: herd tag - no repo, existing tag
        Given cats example is initialized
        And GitHub <repo> has remote <tag>
        And <directory> doesn't exist
        When I run 'clowder herd -t pytest-tag'
        Then the command succeeds
        And <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <tag>
        And project at <directory> has detached HEAD
        And project at <directory> has local <branch>

        Examples:
        | directory         | branch | tag        | repo            |
        | mu                | knead  | pytest-tag | JrGoodle/mu     |
        | duke              | purr   | pytest-tag | JrGoodle/duke   |
        | black-cats/kit    | master | pytest-tag | JrGoodle/kit    |
        | black-cats/kishka | master | pytest-tag | JrGoodle/kishka |
        | black-cats/june   | master | pytest-tag | JrGoodle/june   |
        | black-cats/sasha  | master | pytest-tag | JrGoodle/sasha  |

    @cats @internet
    Scenario Outline: herd tag - no repo, no tag
        Given cats example is initialized
        And GitHub <repo> has no remote <tag>
        And <directory> doesn't exist
        When I run 'clowder herd -t pytest-tag-missing'
        Then the command succeeds
        And <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | tag                | repo            |
        | mu                | knead  | pytest-tag-missing | JrGoodle/mu     |
        | duke              | purr   | pytest-tag-missing | JrGoodle/duke   |
        | black-cats/kit    | master | pytest-tag-missing | JrGoodle/kit    |
        | black-cats/kishka | master | pytest-tag-missing | JrGoodle/kishka |
        | black-cats/june   | master | pytest-tag-missing | JrGoodle/june   |
        | black-cats/sasha  | master | pytest-tag-missing | JrGoodle/sasha  |

    @cats @internet
    Scenario Outline: herd tag - existing repo, existing tag
        Given cats example is initialized and herded
        And GitHub <repo> has remote <tag>
        And project at <directory> is on <branch>
        When I run 'clowder herd -t pytest-tag'
        Then the command succeeds
        And project at <directory> is on <tag>
        And project at <directory> has detached HEAD

        Examples:
        | directory         | branch | tag        | repo            |
        | mu                | knead  | pytest-tag | JrGoodle/mu     |
        | duke              | purr   | pytest-tag | JrGoodle/duke   |
        | black-cats/kit    | master | pytest-tag | JrGoodle/kit    |
        | black-cats/kishka | master | pytest-tag | JrGoodle/kishka |
        | black-cats/june   | master | pytest-tag | JrGoodle/june   |
        | black-cats/sasha  | master | pytest-tag | JrGoodle/sasha  |

    @cats @internet
    Scenario Outline: herd tag - existing repo, no existing tag
        Given cats example is initialized and herded
        And GitHub <repo> has no remote <tag>
        And project at <directory> is on <branch>
        When I run 'clowder herd -t pytest-tag-missing'
        Then the command succeeds
        And project at <directory> is on <branch>

        Examples:
        | directory         | branch | tag                | repo            |
        | mu                | knead  | pytest-tag-missing | JrGoodle/mu     |
        | duke              | purr   | pytest-tag-missing | JrGoodle/duke   |
        | black-cats/kit    | master | pytest-tag-missing | JrGoodle/kit    |
        | black-cats/kishka | master | pytest-tag-missing | JrGoodle/kishka |
        | black-cats/june   | master | pytest-tag-missing | JrGoodle/june   |
        | black-cats/sasha  | master | pytest-tag-missing | JrGoodle/sasha  |

# TODO: Add more tests for local vs remote tags and annotated vs lightweight

    @cats @internet
    Scenario Outline: herd non-standard default branch implicitly
        Given cats example is initialized
        And linked default-branch clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory | branch          |
        | duffy     | default-branch  |

# TODO: Add tests for creating .git/refs/remotes/remote/HEAD file
