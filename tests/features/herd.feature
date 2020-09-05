@herd
Feature: clowder herd

    @help @cats
    Scenario: herd help in empty directory
        Given test directory is empty
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @help @cats
    Scenario: herd help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
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
        And project at <directory> created local branch <test_branch>
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
    Scenario Outline: Test clowder herd untracked file
        Given cats example is initialized and herded
        And created file <filename> in directory <directory>
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
        And created file <filename> in directory <directory>
        And project at <directory> staged file <filename>
        And project at <directory> is on <branch>
        When I run 'clowder herd'
        Then the command fails
#        And project at mu has staged file something.txt
        And project at <directory> is dirty
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
        | black-cats/kit    | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @submodules @cats
    Scenario Outline: herd submodules recursive enabled check projects
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
        And project at <directory> has no submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> has been initialized

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

    # TODO: Add tests for groups/projects
    @misc @upstream @config
    Scenario Outline: herd upstream remote urls override https config
        Given misc example is initialized
        And <directory> doesn't exist
        And 'clowder config set protocol https' was run
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
    @misc @upstream @config @ssh
    Scenario Outline: herd upstream remote urls override ssh config
        Given misc example is initialized
        And linked https clowder version
        And <directory> doesn't exist
        And 'clowder config set protocol ssh' was run
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

    @cats @internet @write
    Scenario Outline: herd rebase with conflict
        Given cats example is initialized and herded
        And project at <directory> has local commits and is behind remote branch <test_branch>
        When I run 'clowder herd -r'
        Then the command fails
        And project at <directory> has rebase in progress

        Examples:
        | directory         | test_branch |
        | mu                | knead       |
        | duke              | purr        |
        | black-cats/kishka | master      |
        | black-cats/kit    | master      |
        | black-cats/sasha  | master      |
        | black-cats/june   | master      |

    @cats
    Scenario Outline: herd saved version after init
        Given cats example is initialized
        And linked v0.1 clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on commit <commit>
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

    Scenario Outline: herd with missing default branch
        Given cats example is initialized and herded
        And project at <directory> deleted local branch <branch>
        And project at <directory> checked out detached HEAD behind <branch>
        And project at <directory> is on <commit>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | commit                                   |
        | mu                | knead  | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | purr   | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | master | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | master | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | master | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | master | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @fail
    Scenario Outline: herd yaml configured with non-existent remote branch
        Given cats example is initialized
        And project at <directory> deleted local branch <branch>
        And project at <directory> checked out detached HEAD behind <branch>
        And project at <directory> is on <commit>
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch | commit                                   |
        | mu                | knead  | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | purr   | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | master | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | master | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | master | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | master | 775979e0b1a7f753131bf16a4794c851c67108d8 |
