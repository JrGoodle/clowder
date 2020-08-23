Feature: New Syntax
    Run 'clowder init', 'clowder herd', and 'clowder status'

    Scenario Outline: Default init
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

