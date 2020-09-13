@yaml_validation
Feature: clowder yaml validation

    Scenario: validate project.branch
        Given validating property <project_branch>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has tracking branch felid
        And project at felidae is on branch felid

    Scenario: validate implicit project.branch
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has tracking branch master
        And project at felidae is on branch master

    Scenario: validate project.commit
        Given validating property <project_commit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is on commit e61b2495a3fe903f43a8c2be3d58b6b01bdbf664
        And project at felidae has detached HEAD

    Scenario: validate implicit project.commit
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has tracking branch master
        And project at felidae is on branch master

    Scenario: validate project.git.config
        Given validating property <project_git_config>
        And validation clowder is initialized and herded
        And project at felidae is clean
        And something file doesn't exist in directory felidae
        When I change to directory felidae
        And I run 'git something'
        Then the command succeeds
        And project at felidae is dirty
        And something file exists in directory felidae

    Scenario: validate implicit project.git.config
        Given validating property <project_implicit>
        And validation clowder is initialized and herded
        And project at felidae is clean
        And something file doesn't exist in directory felidae
        When I change to directory felidae
        And I run 'git something'
        Then the command fails
        And project at felidae is clean
        And something file doesn't exist in directory felidae

#    Scenario: validate project.git.depth
#        Given validating property <project_git_depth>
#        And validation clowder is initialized
#        And felidae directory doesn't exist
#        When I run 'clowder herd'
#        Then the command fails
#
#    Scenario: validate implicit project.git.depth
#        Given validating property <project_implicit>
#        And validation clowder is initialized
#        And felidae directory doesn't exist
#        When I run 'clowder herd'
#        Then the command fails

    Scenario: validate project.git.lfs
        Given validating property <project_git_lfs>
        And validation clowder is initialized
        And felidae directory doesn't exist
        And lfs is not installed
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is clean
        And project at felidae has lfs installed
        And jrgoodle.png exists in felidae
        And jrgoodle.png in felidae is not an lfs pointer

    Scenario: validate implicit project.git.lfs
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        And lfs is not installed
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is clean
        And project at felidae doesn't have lfs installed
        And jrgoodle.png exists in felidae
        And jrgoodle.png in felidae is an lfs pointer

    Scenario: validate project.git.submodules
        Given validating property <project_git_submodules>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae exists
        And project at felidae is clean
        And project at felidae has submodule at ash
        And submodule in felidae at ash has been initialized
        And project at felidae has no submodule at ash/duffy
        And submodule in felidae at ash/duffy has been initialized

    Scenario: validate implicit project.git.submodules
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae exists
        And project at felidae is clean
        And project at felidae has submodule at ash
        And submodule in felidae at ash hasn't been initialized

    Scenario: validate project.groups
        Given validating property <project_groups>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd cats'
        And I run 'clowder herd cats-group'
        Then the commands succeed
        And project at felidae is a git repository
        And project at felidae has tracking branch master
        And project at felidae is on branch master

    Scenario: validate implicit project.groups
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd cats'
        And I run 'clowder herd cats-group'
        Then the commands succeed
        And project at felidae is a git repository
        And project at felidae has tracking branch master
        And project at felidae is on branch master

    Scenario: validate project.path
        Given validating property <project_path>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at carnivora/feliforma/felidae is a git repository
        And project at carnivora/feliforma/felidae has tracking branch master
        And project at carnivora/feliforma/felidae is on branch master

    Scenario: validate implicit project.path
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is a git repository
        And project at felidae has tracking branch master
        And project at felidae is on branch master

    Scenario: validate project.remote
        Given validating property <project_remote>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote source with url git@github.com:JrGoodle/felidae.git

    Scenario: validate implicit project.remote
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote oigin with url git@github.com:JrGoodle/felidae.git

    Scenario: validate project.source.protocol
        Given validating property <project_source_protocol>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote origin with url https://polka-dot-cat.git.beanstalkapp.com/felidae.git

    Scenario: validate implicit project.source.protocol
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote origin with url git@github.com:JrGoodle/felidae.git

    Scenario: validate project.source.url
        Given validating property <project_source_url>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote origin with url git@polka-dot-cat.git.beanstalkapp.com:polka-dot-cat/felidae.git
#        And project at felidae has remote origin with url git@polka-dot-cat.git.beanstalkapp.com:/polka-dot-cat/felidae.git

    Scenario: validate implicit project.source.url
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has remote origin with url git@github.com:JrGoodle/felidae.git

    Scenario: validate project.tag
        Given validating property <project_tag>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is on tag cat
        And project at felidae has detached HEAD

    Scenario: validate implicit project.tag
        Given validating property <project_implicit>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae has tracking branch master
        And project at felidae is on branch master
