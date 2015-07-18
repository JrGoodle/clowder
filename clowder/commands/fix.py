import os

import utilities

class Fix(object):

    def __init__(self, clowder, version):
        versionManifest = version + '.xml'

        command = 'repo manifest -o .clowder/clowder/' + versionManifest + ' -r'
        utilities.ex(command)

        os.chdir('.clowder/clowder')

        command = 'git add ' + versionManifest
        utilities.ex(command)

        command = 'git commit -m "Add manifest ' + version + '"'
        utilities.ex(command)

        command = 'git push'
        utilities.ex(command)

        command = 'git tag ' + version
        utilities.ex(command)

        command = 'git push origin ' + version
        utilities.ex(command)
