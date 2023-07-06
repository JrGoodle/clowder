"""ssh utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

# import base64

import paramiko


class SecureShellCompletedProcess:

    def __init__(self, stdin, stdout, stderr):
        self.stdin = stdin
        self.stdout: str = stdout
        self.stderr: str = stderr


class SecureShell:

    def __init__(self, url: str, user: str, password: str):
        # key = paramiko.RSAKey(data=str(base64.b64decode(b'AAA...')))
        self._client = paramiko.SSHClient()
        # client.get_host_keys().add(ENVIRONMENT.pygoodle_url, 'ssh-rsa', key)
        self._client.connect(url, username=user, password=password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        self._client.close()

    def run_command(self, command: str) -> SecureShellCompletedProcess:
        stdin, stdout, stderr = self._client.exec_command(command)
        return SecureShellCompletedProcess(stdin, stdout, stderr)
