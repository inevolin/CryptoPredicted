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


class UpdateBotShippingQuery(Object):
    """Attributes:
        ID: ``0xe0cdc940``

    Args:
        query_id: ``int`` ``64-bit``
        user_id: ``int`` ``32-bit``
        payload: ``bytes``
        shipping_address: :obj:`PostAddress <pyrogram.api.types.PostAddress>`
    """

    ID = 0xe0cdc940

    def __init__(self, query_id: int, user_id: int, payload: bytes, shipping_address):
        self.query_id = query_id  # long
        self.user_id = user_id  # int
        self.payload = payload  # bytes
        self.shipping_address = shipping_address  # PostAddress

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateBotShippingQuery":
        # No flags
        
        query_id = Long.read(b)
        
        user_id = Int.read(b)
        
        payload = Bytes.read(b)
        
        shipping_address = Object.read(b)
        
        return UpdateBotShippingQuery(query_id, user_id, payload, shipping_address)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.query_id))
        
        b.write(Int(self.user_id))
        
        b.write(Bytes(self.payload))
        
        b.write(self.shipping_address.write())
        
        return b.getvalue()
