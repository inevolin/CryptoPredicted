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


class InputSingleMedia(Object):
    """Attributes:
        ID: ``0x1cc6e91f``

    Args:
        media: Either :obj:`InputMediaEmpty <pyrogram.api.types.InputMediaEmpty>`, :obj:`InputMediaUploadedPhoto <pyrogram.api.types.InputMediaUploadedPhoto>`, :obj:`InputMediaPhoto <pyrogram.api.types.InputMediaPhoto>`, :obj:`InputMediaGeoPoint <pyrogram.api.types.InputMediaGeoPoint>`, :obj:`InputMediaContact <pyrogram.api.types.InputMediaContact>`, :obj:`InputMediaUploadedDocument <pyrogram.api.types.InputMediaUploadedDocument>`, :obj:`InputMediaDocument <pyrogram.api.types.InputMediaDocument>`, :obj:`InputMediaVenue <pyrogram.api.types.InputMediaVenue>`, :obj:`InputMediaGifExternal <pyrogram.api.types.InputMediaGifExternal>`, :obj:`InputMediaPhotoExternal <pyrogram.api.types.InputMediaPhotoExternal>`, :obj:`InputMediaDocumentExternal <pyrogram.api.types.InputMediaDocumentExternal>`, :obj:`InputMediaGame <pyrogram.api.types.InputMediaGame>`, :obj:`InputMediaInvoice <pyrogram.api.types.InputMediaInvoice>` or :obj:`InputMediaGeoLive <pyrogram.api.types.InputMediaGeoLive>`
        random_id: ``int`` ``64-bit``
        message: ``str``
        entities (optional): List of either :obj:`MessageEntityUnknown <pyrogram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <pyrogram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <pyrogram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <pyrogram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <pyrogram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <pyrogram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <pyrogram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <pyrogram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <pyrogram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <pyrogram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <pyrogram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <pyrogram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <pyrogram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <pyrogram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <pyrogram.api.types.MessageEntityCashtag>`
    """

    ID = 0x1cc6e91f

    def __init__(self, media, random_id: int, message: str, entities: list = None):
        self.media = media  # InputMedia
        self.random_id = random_id  # long
        self.message = message  # string
        self.entities = entities  # flags.0?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "InputSingleMedia":
        flags = Int.read(b)
        
        media = Object.read(b)
        
        random_id = Long.read(b)
        
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 0) else []
        
        return InputSingleMedia(media, random_id, message, entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(self.media.write())
        
        b.write(Long(self.random_id))
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
