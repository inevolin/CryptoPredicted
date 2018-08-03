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


class SavedGifs(Object):
    """Attributes:
        ID: ``0x2e0709a5``

    Args:
        hash: ``int`` ``32-bit``
        gifs: List of either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetSavedGifs <pyrogram.api.functions.messages.GetSavedGifs>`.
    """

    ID = 0x2e0709a5

    def __init__(self, hash: int, gifs: list):
        self.hash = hash  # int
        self.gifs = gifs  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "SavedGifs":
        # No flags
        
        hash = Int.read(b)
        
        gifs = Object.read(b)
        
        return SavedGifs(hash, gifs)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.gifs))
        
        return b.getvalue()
