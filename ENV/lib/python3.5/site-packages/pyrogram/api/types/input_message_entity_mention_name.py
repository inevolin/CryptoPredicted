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


class InputMessageEntityMentionName(Object):
    """Attributes:
        ID: ``0x208e68c9``

    Args:
        offset: ``int`` ``32-bit``
        length: ``int`` ``32-bit``
        user_id: Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`
    """

    ID = 0x208e68c9

    def __init__(self, offset: int, length: int, user_id):
        self.offset = offset  # int
        self.length = length  # int
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args) -> "InputMessageEntityMentionName":
        # No flags
        
        offset = Int.read(b)
        
        length = Int.read(b)
        
        user_id = Object.read(b)
        
        return InputMessageEntityMentionName(offset, length, user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.offset))
        
        b.write(Int(self.length))
        
        b.write(self.user_id.write())
        
        return b.getvalue()
