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


class RpcResult(Object):
    """Attributes:
        ID: ``0xf35c6d01``

    Args:
        req_msg_id: ``int`` ``64-bit``
        result: Any object from :obj:`pyrogram.api.types`
    """

    ID = 0xf35c6d01

    def __init__(self, req_msg_id: int, result):
        self.req_msg_id = req_msg_id  # long
        self.result = result  # Object

    @staticmethod
    def read(b: BytesIO, *args) -> "RpcResult":
        # No flags
        
        req_msg_id = Long.read(b)
        
        result = Object.read(b)
        
        return RpcResult(req_msg_id, result)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(self.result.write())
        
        return b.getvalue()
