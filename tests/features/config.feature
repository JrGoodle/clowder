@config @debug
Feature: clowder config

    @help
    Scenario: config help in empty directory
        Given test directory is empty
        When I run 'clowder config -h' and 'clowder config --help'
        Then the commands succeed

    @help @cats
    Scenario: config help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder config -h' and 'clowder config --help'
        Then the commands succeed

    @help @cats
    Scenario: config help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder config -h' and 'clowder config --help'
        Then the commands succeed

    # TODO: Add tests for groups/projects
    @misc @upstream
    Scenario Outline: config set protocol https
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
    @misc @upstream @ssh
    Scenario Outline: config set protocol ssh
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

    @cats
    Scenario Outline: config set groups config included
        Given cats example is initialized
        And 'clowder config set projects JrGoodle/kishka JrGoodle/kit' was run
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | black-cats/kishka | master |
        | black-cats/kit    | master |

    @cats
    Scenario Outline: config set groups config excluded
        Given cats example is initialized
        And 'clowder config set projects JrGoodle/kishka JrGoodle/kit' was run
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And <directory> doesn't exist

        Examples:
        | directory         |
        | mu                |
        | duke              |
        | black-cats/sasha  |
        | black-cats/june   |

    @cats @internet @write @ssh
    Scenario Outline: config set rebase
        Given cats example is initialized and herded with ssh
        And linked test-branch-ssh clowder version
        And cats example projects have tracking branch <test_branch>
        And project at <directory> checked out <test_branch>
        And project at <directory> is behind upstream <test_branch> by <number_behind> and ahead by <number_ahead> with conflict
        And 'clowder config set rebase' was run
        When I run 'clowder herd'
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
    Scenario: config get
        Given cats example is initialized
        When I run 'clowder config get'
        Then the command succeeds
#        TODO: Add check for output

    @cats
    Scenario: config clear
        Given cats example is initialized
        And test config was copied to clowder repo
        And clowder.config.yml file exists in directory .clowder/config
        When I run 'clowder config clear'
        Then the command succeeds
#        TODO: Remove config file when cleared, also remove project path since it's relative to clowder dir
#        And <filename> doesn't exist in <directory>

    @cats
    Scenario Outline: config set jobs
        Given cats example is initialized
        And <directory> doesn't exist
        And 'clowder config set jobs 4' was run
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean
#        TODO: Add check for whether command ran in parallel

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |
