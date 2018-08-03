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


class MsgNewDetailedInfo(Object):
    """Attributes:
        ID: ``0x809db6df``

    Args:
        answer_msg_id: ``int`` ``64-bit``
        bytes: ``int`` ``32-bit``
        status: ``int`` ``32-bit``
    """

    ID = 0x809db6df

    def __init__(self, answer_msg_id: int, bytes: int, status: int):
        self.answer_msg_id = answer_msg_id  # long
        self.bytes = bytes  # int
        self.status = status  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "MsgNewDetailedInfo":
        # No flags
        
        answer_msg_id = Long.read(b)
        
        bytes = Int.read(b)
        
        status = Int.read(b)
        
        return MsgNewDetailedInfo(answer_msg_id, bytes, status)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.answer_msg_id))
        
        b.write(Int(self.bytes))
        
        b.write(Int(self.status))
        
        return b.getvalue()
