@herd
Feature: Test clowder herd

    @default
    Scenario Outline: Test clowder herd default
        Given cats example is initialized
        And <directory> doesn't exist

        When I run 'clowder herd'

        Then project at <directory> exists
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

    @commits
    Scenario Outline: Test clowder herd commits
        Given cats example is initialized
        And <directory> doesn't exist
        And static-refs yaml version is linked

        When I run 'clowder herd'

        Then project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <commit>
        And project at <directory> is clean

        Examples:
        | directory         | commit                                   |
        | mu                | cddce39214a1ae20266d9ee36966de67438625d1 |
        | duke              | 7083e8840e1bb972b7664cfa20bbd7a25f004018 |
        | black-cats/kit    | da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd |
        | black-cats/kishka | d185e3bff9eaaf6e146d4e09165276cd5c9f31c8 |
        | black-cats/june   | b6e1316cc62cb2ba18fa982fc3d67ef4408c8bfd |
        | black-cats/sasha  | 775979e0b1a7f753131bf16a4794c851c67108d8 |

    @tags
    Scenario Outline: Test clowder herd tags
        Given cats example is initialized
        And <directory> doesn't exist
        And tags yaml version is linked

        When I run 'clowder herd'

        Then project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <tag>
        And project at <directory> is clean

        Examples:
        | directory         | tag                   |
        | mu                | test-clowder-yaml-tag |
        | duke              | purr                  |
        | black-cats/kishka | v0.01                 |
        | black-cats/kit    | v0.01                 |
        | black-cats/sasha  | v0.01                 |
        | black-cats/june   | v0.01                 |

    @default @fail
    Scenario: Test clowder herd dirty fail
        Given cats example is initialized
        And 'clowder herd' has been run
        And mu has untracked file something.txt

        When I run 'clowder herd' with exit code 7

        Then project at mu exists
        And project at mu is a git repository
        And mu has untracked file something.txt
