import os

import clowder.utilities

class Fix(object):

    def __init__(self, theClowder, version):
        versionManifest = version + '.xml'

        command = 'repo manifest -o .clowder/clowder/' + versionManifest + ' -r'
        clowder.utilities.ex(command)

        os.chdir('.clowder/clowder')

        command = 'git add ' + versionManifest
        clowder.utilities.ex(command)

        command = 'git commit -m "Add manifest ' + version + '"'
        clowder.utilities.ex(command)

        command = 'git push'
        clowder.utilities.ex(command)

        command = 'git tag ' + version
        clowder.utilities.ex(command)

        command = 'git push origin ' + version
        clowder.utilities.ex(command)
