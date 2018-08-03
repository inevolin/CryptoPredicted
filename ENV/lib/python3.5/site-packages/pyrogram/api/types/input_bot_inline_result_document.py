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


class InputBotInlineResultDocument(Object):
    """Attributes:
        ID: ``0xfff8fdc4``

    Args:
        id: ``str``
        type: ``str``
        document: Either :obj:`InputDocumentEmpty <pyrogram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <pyrogram.api.types.InputDocument>`
        send_message: Either :obj:`InputBotInlineMessageMediaAuto <pyrogram.api.types.InputBotInlineMessageMediaAuto>`, :obj:`InputBotInlineMessageText <pyrogram.api.types.InputBotInlineMessageText>`, :obj:`InputBotInlineMessageMediaGeo <pyrogram.api.types.InputBotInlineMessageMediaGeo>`, :obj:`InputBotInlineMessageMediaVenue <pyrogram.api.types.InputBotInlineMessageMediaVenue>`, :obj:`InputBotInlineMessageMediaContact <pyrogram.api.types.InputBotInlineMessageMediaContact>` or :obj:`InputBotInlineMessageGame <pyrogram.api.types.InputBotInlineMessageGame>`
        title (optional): ``str``
        description (optional): ``str``
    """

    ID = 0xfff8fdc4

    def __init__(self, id: str, type: str, document, send_message, title: str = None, description: str = None):
        self.id = id  # string
        self.type = type  # string
        self.title = title  # flags.1?string
        self.description = description  # flags.2?string
        self.document = document  # InputDocument
        self.send_message = send_message  # InputBotInlineMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineResultDocument":
        flags = Int.read(b)
        
        id = String.read(b)
        
        type = String.read(b)
        
        title = String.read(b) if flags & (1 << 1) else None
        description = String.read(b) if flags & (1 << 2) else None
        document = Object.read(b)
        
        send_message = Object.read(b)
        
        return InputBotInlineResultDocument(id, type, document, send_message, title, description)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.title is not None else 0
        flags |= (1 << 2) if self.description is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.id))
        
        b.write(String(self.type))
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.description is not None:
            b.write(String(self.description))
        
        b.write(self.document.write())
        
        b.write(self.send_message.write())
        
        return b.getvalue()
