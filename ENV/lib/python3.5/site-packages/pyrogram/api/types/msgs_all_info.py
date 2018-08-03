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


class MsgsAllInfo(Object):
    """Attributes:
        ID: ``0x8cc0d131``

    Args:
        msg_ids: List of ``int`` ``64-bit``
        info: ``str``
    """

    ID = 0x8cc0d131

    def __init__(self, msg_ids: list, info: str):
        self.msg_ids = msg_ids  # Vector<long>
        self.info = info  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "MsgsAllInfo":
        # No flags
        
        msg_ids = Object.read(b, Long)
        
        info = String.read(b)
        
        return MsgsAllInfo(msg_ids, info)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.msg_ids, Long))
        
        b.write(String(self.info))
        
        return b.getvalue()
