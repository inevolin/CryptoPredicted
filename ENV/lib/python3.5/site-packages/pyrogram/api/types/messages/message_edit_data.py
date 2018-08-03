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


class MessageEditData(Object):
    """Attributes:
        ID: ``0x26b5dde6``

    Args:
        caption (optional): ``bool``

    See Also:
        This object can be returned by :obj:`messages.GetMessageEditData <pyrogram.api.functions.messages.GetMessageEditData>`.
    """

    ID = 0x26b5dde6

    def __init__(self, caption: bool = None):
        self.caption = caption  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageEditData":
        flags = Int.read(b)
        
        caption = True if flags & (1 << 0) else False
        return MessageEditData(caption)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.caption is not None else 0
        b.write(Int(flags))
        
        return b.getvalue()
