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


class KeyboardButtonSwitchInline(Object):
    """Attributes:
        ID: ``0x0568a748``

    Args:
        text: ``str``
        query: ``str``
        same_peer (optional): ``bool``
    """

    ID = 0x0568a748

    def __init__(self, text: str, query: str, same_peer: bool = None):
        self.same_peer = same_peer  # flags.0?true
        self.text = text  # string
        self.query = query  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "KeyboardButtonSwitchInline":
        flags = Int.read(b)
        
        same_peer = True if flags & (1 << 0) else False
        text = String.read(b)
        
        query = String.read(b)
        
        return KeyboardButtonSwitchInline(text, query, same_peer)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.same_peer is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.text))
        
        b.write(String(self.query))
        
        return b.getvalue()
