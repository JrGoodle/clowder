"""command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Any, Dict, List

from .argument import Argument


class MutuallyExclusiveArgumentGroup:

    def __init__(self, args: List[Argument], **kwargs):
        self.args: List[Argument] = args
        self.options: Dict[str, Any] = kwargs
