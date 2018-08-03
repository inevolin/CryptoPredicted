# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class HighScore(Object):
    """Attributes:
        ID: ``0x58fffcd0``

    Args:
        pos: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        score: ``int`` ``32-bit``
    """

    ID = 0x58fffcd0

    def __init__(self, pos: int, user_id: int, score: int):
        self.pos = pos  # int
        self.user_id = user_id  # int
        self.score = score  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "HighScore":
        # No flags
        
        pos = Int.read(b)
        
        user_id = Int.read(b)
        
        score = Int.read(b)
        
        return HighScore(pos, user_id, score)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pos))
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.score))
        
        return b.getvalue()
