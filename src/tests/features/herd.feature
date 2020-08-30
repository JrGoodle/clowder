@herd
Feature: clowder herd

    @help @success @cats
    Scenario: clowder herd help in empty directory
        Given test directory is empty
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder herd help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder herd help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder herd -h' and 'clowder herd --help'
        Then the commands succeed

    @success @cats
    Scenario Outline: clowder herd default
        Given cats example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on branch <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |

    @commits @success @cats
    Scenario Outline: clowder herd commits
        Given cats example is initialized
        And <directory> doesn't exist
        And did link static-refs clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on commit <commit>
        And project at <directory> is clean

        Examples:
        | directory         | commit                                   |
        | mu                | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @tags @success @cats
    Scenario Outline: clowder herd tags
        Given cats example is initialized
        And <directory> doesn't exist
        And did link tags clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> is a git repository
        And project at <directory> is on tag <tag>
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
    Scenario: Test clowder herd dirty fail
        Given cats example is initialized and herded
        And mu has untracked file something.txt
        When I run 'clowder herd'
        Then the command fails
        And mu has untracked file something.txt

    @success @submodules @cats
    Scenario Outline: clowder herd submodules recursive enabled check projects
        Given cats example is initialized
        And <directory> doesn't exist
        And did link submodules clowder version
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

    @success @submodules @cats
    Scenario Outline: clowder herd submodules recursive enabled check submodules
        Given cats example is initialized
        And <directory> doesn't exist
        And did link submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is clean
        And project at <directory> has submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> has been initialized

        Examples:
        | directory     | submodule_path |
        | mu            | ash            |

    @success @submodules @cats
    Scenario Outline: clowder herd submodules recursive enabled check recursive submodules
        Given cats example is initialized
        And <directory> doesn't exist
        And did link submodules clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is clean
        And project at <directory> has no submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> has been initialized

        Examples:
        | directory     | submodule_path |
        | mu            | ash/duffy      |

    @success @submodules @cats
    Scenario Outline: clowder herd submodules disabled check non-submodules exist
        Given cats example is initialized
        And <directory> doesn't exist
        And did link submodules-no-recurse clowder version
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

    @success @submodules @cats
    Scenario Outline: clowder herd submodules disabled check submodules don't exist
        Given cats example is initialized
        And <directory> doesn't exist
        And did link submodules-no-recurse clowder version
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> has submodule at <submodule_path>
        And submodule in <directory> at <submodule_path> hasn't been initialized

        Examples:
        | directory | submodule_path |
        | mu        | ash            |

    @success @misc @upstream @ssh
    Scenario Outline: clowder herd upstream remote urls
        Given misc example is initialized
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on branch <branch>
        And project at <directory> has remote <remote> with url <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | git@github.com:JrGoodle/djinni.git                 |
        | djinni    | master      | upstream | git@github.com:dropbox/djinni.git                  |
        | gyp       | fork-branch | origin   | git@github.com:JrGoodle/gyp.git                    |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | git@github.com:JrGoodle/sox.git                    |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    @success @misc @upstream
    Scenario Outline: clowder herd upstream remote urls override https
        Given misc example is initialized
        And did link https clowder version
        And <directory> doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on branch <branch>
        And project at <directory> has remote <remote> with url <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | https://github.com/JrGoodle/djinni.git             |
        | djinni    | master      | upstream | https://github.com/dropbox/djinni.git              |
        | gyp       | fork-branch | origin   | https://github.com/JrGoodle/gyp.git                |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | https://github.com/JrGoodle/sox.git                |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |

    @success @misc @upstream @config
    Scenario Outline: clowder herd upstream remote urls config https
        Given misc example is initialized
        And did link https clowder version
        And <directory> doesn't exist
        And 'clowder config set protocol https' has been run
        When I run 'clowder herd'
        Then the command succeeds
        And project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on branch <branch>
        And project at <directory> has remote <remote> with url <url>

        Examples:
        | directory | branch      | remote   | url                                                |
        | djinni    | master      | origin   | https://github.com/JrGoodle/djinni.git             |
        | djinni    | master      | upstream | https://github.com/dropbox/djinni.git              |
        | gyp       | fork-branch | origin   | https://github.com/JrGoodle/gyp.git                |
        | gyp       | fork-branch | upstream | https://chromium.googlesource.com/external/gyp.git |
        | sox       | master      | origin   | https://github.com/JrGoodle/sox.git                |
        | sox       | master      | upstream | https://git.code.sf.net/p/sox/code.git             |
