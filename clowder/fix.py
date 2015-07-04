import os
import shutil

from git import Repo

import clowder.log
import clowder.utilities

class Fix(object):

    def __init__(self, version, clowderDirectory):
        command = 'repo manifest -o snapshot.xml -r'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        os.chdir(os.path.join(clowderDirectory, 'clowder'))

        command = 'git checkout snapshots'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        print("Remove previous 'default.xml'")
        os.remove('default.xml')
        print("Move 'snapshot.xml' and rename to 'default.xml'")
        shutil.move('../../snapshot.xml', 'default.xml')

        command = 'git add default.xml'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git commit -m "Update default.xml for version ' + version + '"'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git push'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git tag ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git push origin ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git checkout master'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
