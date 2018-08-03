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


class BotInlineMediaResult(Object):
    """Attributes:
        ID: ``0x17db940b``

    Args:
        id: ``str``
        type: ``str``
        send_message: Either :obj:`BotInlineMessageMediaAuto <pyrogram.api.types.BotInlineMessageMediaAuto>`, :obj:`BotInlineMessageText <pyrogram.api.types.BotInlineMessageText>`, :obj:`BotInlineMessageMediaGeo <pyrogram.api.types.BotInlineMessageMediaGeo>`, :obj:`BotInlineMessageMediaVenue <pyrogram.api.types.BotInlineMessageMediaVenue>` or :obj:`BotInlineMessageMediaContact <pyrogram.api.types.BotInlineMessageMediaContact>`
        photo (optional): Either :obj:`PhotoEmpty <pyrogram.api.types.PhotoEmpty>` or :obj:`Photo <pyrogram.api.types.Photo>`
        document (optional): Either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`
        title (optional): ``str``
        description (optional): ``str``
    """

    ID = 0x17db940b

    def __init__(self, id: str, type: str, send_message, photo=None, document=None, title: str = None, description: str = None):
        self.id = id  # string
        self.type = type  # string
        self.photo = photo  # flags.0?Photo
        self.document = document  # flags.1?Document
        self.title = title  # flags.2?string
        self.description = description  # flags.3?string
        self.send_message = send_message  # BotInlineMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "BotInlineMediaResult":
        flags = Int.read(b)
        
        id = String.read(b)
        
        type = String.read(b)
        
        photo = Object.read(b) if flags & (1 << 0) else None
        
        document = Object.read(b) if flags & (1 << 1) else None
        
        title = String.read(b) if flags & (1 << 2) else None
        description = String.read(b) if flags & (1 << 3) else None
        send_message = Object.read(b)
        
        return BotInlineMediaResult(id, type, send_message, photo, document, title, description)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.photo is not None else 0
        flags |= (1 << 1) if self.document is not None else 0
        flags |= (1 << 2) if self.title is not None else 0
        flags |= (1 << 3) if self.description is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.id))
        
        b.write(String(self.type))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.description is not None:
            b.write(String(self.description))
        
        b.write(self.send_message.write())
        
        return b.getvalue()
