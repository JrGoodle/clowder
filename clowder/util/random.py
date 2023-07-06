"""random utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import random
import string


def random_alphanumeric_string(length: int) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    result = ''.join((random.choice(letters_and_digits) for _ in range(length)))
    return result
