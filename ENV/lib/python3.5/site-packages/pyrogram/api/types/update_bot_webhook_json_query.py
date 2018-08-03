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


class UpdateBotWebhookJSONQuery(Object):
    """Attributes:
        ID: ``0x9b9240a6``

    Args:
        query_id: ``int`` ``64-bit``
        data: :obj:`DataJSON <pyrogram.api.types.DataJSON>`
        timeout: ``int`` ``32-bit``
    """

    ID = 0x9b9240a6

    def __init__(self, query_id: int, data, timeout: int):
        self.query_id = query_id  # long
        self.data = data  # DataJSON
        self.timeout = timeout  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateBotWebhookJSONQuery":
        # No flags
        
        query_id = Long.read(b)
        
        data = Object.read(b)
        
        timeout = Int.read(b)
        
        return UpdateBotWebhookJSONQuery(query_id, data, timeout)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.query_id))
        
        b.write(self.data.write())
        
        b.write(Int(self.timeout))
        
        return b.getvalue()
