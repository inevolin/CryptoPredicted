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


class BotInlineResult(Object):
    """Attributes:
        ID: ``0x11965f3a``

    Args:
        id: ``str``
        type: ``str``
        send_message: Either :obj:`BotInlineMessageMediaAuto <pyrogram.api.types.BotInlineMessageMediaAuto>`, :obj:`BotInlineMessageText <pyrogram.api.types.BotInlineMessageText>`, :obj:`BotInlineMessageMediaGeo <pyrogram.api.types.BotInlineMessageMediaGeo>`, :obj:`BotInlineMessageMediaVenue <pyrogram.api.types.BotInlineMessageMediaVenue>` or :obj:`BotInlineMessageMediaContact <pyrogram.api.types.BotInlineMessageMediaContact>`
        title (optional): ``str``
        description (optional): ``str``
        url (optional): ``str``
        thumb (optional): Either :obj:`WebDocument <pyrogram.api.types.WebDocument>` or :obj:`WebDocumentNoProxy <pyrogram.api.types.WebDocumentNoProxy>`
        content (optional): Either :obj:`WebDocument <pyrogram.api.types.WebDocument>` or :obj:`WebDocumentNoProxy <pyrogram.api.types.WebDocumentNoProxy>`
    """

    ID = 0x11965f3a

    def __init__(self, id: str, type: str, send_message, title: str = None, description: str = None, url: str = None, thumb=None, content=None):
        self.id = id  # string
        self.type = type  # string
        self.title = title  # flags.1?string
        self.description = description  # flags.2?string
        self.url = url  # flags.3?string
        self.thumb = thumb  # flags.4?WebDocument
        self.content = content  # flags.5?WebDocument
        self.send_message = send_message  # BotInlineMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "BotInlineResult":
        flags = Int.read(b)
        
        id = String.read(b)
        
        type = String.read(b)
        
        title = String.read(b) if flags & (1 << 1) else None
        description = String.read(b) if flags & (1 << 2) else None
        url = String.read(b) if flags & (1 << 3) else None
        thumb = Object.read(b) if flags & (1 << 4) else None
        
        content = Object.read(b) if flags & (1 << 5) else None
        
        send_message = Object.read(b)
        
        return BotInlineResult(id, type, send_message, title, description, url, thumb, content)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.title is not None else 0
        flags |= (1 << 2) if self.description is not None else 0
        flags |= (1 << 3) if self.url is not None else 0
        flags |= (1 << 4) if self.thumb is not None else 0
        flags |= (1 << 5) if self.content is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.id))
        
        b.write(String(self.type))
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.url is not None:
            b.write(String(self.url))
        
        if self.thumb is not None:
            b.write(self.thumb.write())
        
        if self.content is not None:
            b.write(self.content.write())
        
        b.write(self.send_message.write())
        
        return b.getvalue()
