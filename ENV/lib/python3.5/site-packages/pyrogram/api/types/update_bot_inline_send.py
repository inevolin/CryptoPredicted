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


class UpdateBotInlineSend(Object):
    """Attributes:
        ID: ``0x0e48f964``

    Args:
        user_id: ``int`` ``32-bit``
        query: ``str``
        id: ``str``
        geo (optional): Either :obj:`GeoPointEmpty <pyrogram.api.types.GeoPointEmpty>` or :obj:`GeoPoint <pyrogram.api.types.GeoPoint>`
        msg_id (optional): :obj:`InputBotInlineMessageID <pyrogram.api.types.InputBotInlineMessageID>`
    """

    ID = 0x0e48f964

    def __init__(self, user_id: int, query: str, id: str, geo=None, msg_id=None):
        self.user_id = user_id  # int
        self.query = query  # string
        self.geo = geo  # flags.0?GeoPoint
        self.id = id  # string
        self.msg_id = msg_id  # flags.1?InputBotInlineMessageID

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateBotInlineSend":
        flags = Int.read(b)
        
        user_id = Int.read(b)
        
        query = String.read(b)
        
        geo = Object.read(b) if flags & (1 << 0) else None
        
        id = String.read(b)
        
        msg_id = Object.read(b) if flags & (1 << 1) else None
        
        return UpdateBotInlineSend(user_id, query, id, geo, msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.geo is not None else 0
        flags |= (1 << 1) if self.msg_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.user_id))
        
        b.write(String(self.query))
        
        if self.geo is not None:
            b.write(self.geo.write())
        
        b.write(String(self.id))
        
        if self.msg_id is not None:
            b.write(self.msg_id.write())
        
        return b.getvalue()
