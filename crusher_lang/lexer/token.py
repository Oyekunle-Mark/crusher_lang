from typing import NamedTuple
from typing import Optional
from typing import Union

from .token_type import TokenType


class Token(NamedTuple):
    """The Crusher token"""

    token_type: TokenType
    lexeme: str
    literal: Optional[Union[int, str]]
    line: int
    column: int
