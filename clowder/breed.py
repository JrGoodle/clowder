import sys
import os
import shutil
import subprocess

from git import Repo

import clowder.log
import clowder.utilities

class Breed(object):

    def __init__(self, url, clowderDirectory):
        command = 'repo init -u ' + url
        clowder.utilities.ex(command)

        command = 'repo sync'
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)

        os.mkdir(clowderDirectory)
        os.chdir(clowderDirectory)

        command = 'git clone ' + url + ' clowder'
        clowder.utilities.ex(command)

        os.chdir(os.path.join(os.getcwd(), 'clowder'))

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

    def configureSnapshotsBranch(self):
        repo = Repo(os.getcwd())

        for branch in repo.references:
            print(branch.name)
            if branch.name == 'snapshots':
                print("Local 'snapshots' branch exists")
                print("Checking out local 'snapshots' branch")
                snapshotsBranch = branch
                repo.head.reference = snapshotsBranch
                break
        else:
            print("Local 'snapshots' branch doesn't exist")
            print("Creating local 'snapshots' branch")
            snapshotsBranch = repo.create_head('snapshots')
            print("Checking out local 'snapshots' branch")
            repo.head.reference = snapshotsBranch

        for branch in repo.references:
            print(branch.name)
            if branch.name == 'origin/snapshots':
                print("Remote 'snapshots' branch exists")
                print("Setting local 'snapshots' to point to existing upstream")
                command = 'git branch --set-upstream snapshots origin/snapshots'
                clowder.utilities.ex(command)
                break
        else:
            print("Remote 'snapshots' branch doesn't exist")
            print("Pushing local 'snapshots' to remote")
            command = 'git push -u origin snapshots'
            clowder.utilities.ex(command)

        command = 'git checkout master'
        clowder.utilities.ex(command)
