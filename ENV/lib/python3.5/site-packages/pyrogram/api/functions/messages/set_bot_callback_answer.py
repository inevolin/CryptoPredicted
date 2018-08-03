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


class SetBotCallbackAnswer(Object):
    """Attributes:
        ID: ``0xd58f130a``

    Args:
        query_id: ``int`` ``64-bit``
        cache_time: ``int`` ``32-bit``
        alert (optional): ``bool``
        message (optional): ``str``
        url (optional): ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xd58f130a

    def __init__(self, query_id: int, cache_time: int, alert: bool = None, message: str = None, url: str = None):
        self.alert = alert  # flags.1?true
        self.query_id = query_id  # long
        self.message = message  # flags.0?string
        self.url = url  # flags.2?string
        self.cache_time = cache_time  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SetBotCallbackAnswer":
        flags = Int.read(b)
        
        alert = True if flags & (1 << 1) else False
        query_id = Long.read(b)
        
        message = String.read(b) if flags & (1 << 0) else None
        url = String.read(b) if flags & (1 << 2) else None
        cache_time = Int.read(b)
        
        return SetBotCallbackAnswer(query_id, cache_time, alert, message, url)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.alert is not None else 0
        flags |= (1 << 0) if self.message is not None else 0
        flags |= (1 << 2) if self.url is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        if self.message is not None:
            b.write(String(self.message))
        
        if self.url is not None:
            b.write(String(self.url))
        
        b.write(Int(self.cache_time))
        
        return b.getvalue()
