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


class MsgsStateInfo(Object):
    """Attributes:
        ID: ``0x04deb57d``

    Args:
        req_msg_id: ``int`` ``64-bit``
        info: ``str``
    """

    ID = 0x04deb57d

    def __init__(self, req_msg_id: int, info: str):
        self.req_msg_id = req_msg_id  # long
        self.info = info  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "MsgsStateInfo":
        # No flags
        
        req_msg_id = Long.read(b)
        
        info = String.read(b)
        
        return MsgsStateInfo(req_msg_id, info)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(String(self.info))
        
        return b.getvalue()
