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


class BotCallbackAnswer(Object):
    """Attributes:
        ID: ``0x36585ea4``

    Args:
        cache_time: ``int`` ``32-bit``
        alert (optional): ``bool``
        has_url (optional): ``bool``
        native_ui (optional): ``bool``
        message (optional): ``str``
        url (optional): ``str``

    See Also:
        This object can be returned by :obj:`messages.GetBotCallbackAnswer <pyrogram.api.functions.messages.GetBotCallbackAnswer>`.
    """

    ID = 0x36585ea4

    def __init__(self, cache_time: int, alert: bool = None, has_url: bool = None, native_ui: bool = None, message: str = None, url: str = None):
        self.alert = alert  # flags.1?true
        self.has_url = has_url  # flags.3?true
        self.native_ui = native_ui  # flags.4?true
        self.message = message  # flags.0?string
        self.url = url  # flags.2?string
        self.cache_time = cache_time  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "BotCallbackAnswer":
        flags = Int.read(b)
        
        alert = True if flags & (1 << 1) else False
        has_url = True if flags & (1 << 3) else False
        native_ui = True if flags & (1 << 4) else False
        message = String.read(b) if flags & (1 << 0) else None
        url = String.read(b) if flags & (1 << 2) else None
        cache_time = Int.read(b)
        
        return BotCallbackAnswer(cache_time, alert, has_url, native_ui, message, url)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.alert is not None else 0
        flags |= (1 << 3) if self.has_url is not None else 0
        flags |= (1 << 4) if self.native_ui is not None else 0
        flags |= (1 << 0) if self.message is not None else 0
        flags |= (1 << 2) if self.url is not None else 0
        b.write(Int(flags))
        
        if self.message is not None:
            b.write(String(self.message))
        
        if self.url is not None:
            b.write(String(self.url))
        
        b.write(Int(self.cache_time))
        
        return b.getvalue()
