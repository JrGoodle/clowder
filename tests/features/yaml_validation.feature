@yaml_validation
Feature: clowder yaml validation

#        Examples:
#        | directory | branch | remote | url                                                              |
#        | felidae   | felid  | origin | git@polka-dot-cat.git.beanstalkapp.com:polka-dot-cat/felidae.git |
#        | felidae   | felid  | origin | git@github.com:JrGoodle/felidae.git                              |

    Scenario: validate project.branch
        Given validating property <project_branch>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is a git repository
        And project at felidae has tracking branch felid
        And project at felidae is on branch felid

    Scenario: validate implicit project.branch
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.commit
        Given validating property <project_commit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.commit
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.git.config
        Given validating property <project_git_config>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.git.config
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.git.depth
        Given validating property <project_git_depth>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.git.depth
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.git.lfs
        Given validating property <project_git_lfs>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.git.lfs
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.git.submodules
        Given validating property <project_git_submodules>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.git.submodules
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.groups
        Given validating property <project_groups>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.groups
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.path
        Given validating property <project_path>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.path
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.remote
        Given validating property <project_remote>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.remote
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.source.protocol
        Given validating property <project_source_protocol>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.source.protocol
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.source.url
        Given validating property <project_source_url>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.source.url
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate project.tag
        Given validating property <project_tag>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails

    Scenario: validate implicit project.tag
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command fails
