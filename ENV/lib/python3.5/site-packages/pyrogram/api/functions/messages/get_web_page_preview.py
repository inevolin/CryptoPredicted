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


class GetWebPagePreview(Object):
    """Attributes:
        ID: ``0x8b68b0cc``

    Args:
        message: ``str``
        entities (optional): List of either :obj:`MessageEntityUnknown <pyrogram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <pyrogram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <pyrogram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <pyrogram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <pyrogram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <pyrogram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <pyrogram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <pyrogram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <pyrogram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <pyrogram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <pyrogram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <pyrogram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <pyrogram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <pyrogram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <pyrogram.api.types.MessageEntityCashtag>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`MessageMediaEmpty <pyrogram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <pyrogram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <pyrogram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <pyrogram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <pyrogram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <pyrogram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <pyrogram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <pyrogram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <pyrogram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <pyrogram.api.types.MessageMediaInvoice>` or :obj:`MessageMediaGeoLive <pyrogram.api.types.MessageMediaGeoLive>`
    """

    ID = 0x8b68b0cc

    def __init__(self, message: str, entities: list = None):
        self.message = message  # string
        self.entities = entities  # flags.3?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetWebPagePreview":
        flags = Int.read(b)
        
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 3) else []
        
        return GetWebPagePreview(message, entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
