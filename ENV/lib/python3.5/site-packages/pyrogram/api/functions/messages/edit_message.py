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


class EditMessage(Object):
    """Attributes:
        ID: ``0xc000e4c8``

    Args:
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        id: ``int`` ``32-bit``
        no_webpage (optional): ``bool``
        stop_geo_live (optional): ``bool``
        message (optional): ``str``
        media (optional): Either :obj:`InputMediaEmpty <pyrogram.api.types.InputMediaEmpty>`, :obj:`InputMediaUploadedPhoto <pyrogram.api.types.InputMediaUploadedPhoto>`, :obj:`InputMediaPhoto <pyrogram.api.types.InputMediaPhoto>`, :obj:`InputMediaGeoPoint <pyrogram.api.types.InputMediaGeoPoint>`, :obj:`InputMediaContact <pyrogram.api.types.InputMediaContact>`, :obj:`InputMediaUploadedDocument <pyrogram.api.types.InputMediaUploadedDocument>`, :obj:`InputMediaDocument <pyrogram.api.types.InputMediaDocument>`, :obj:`InputMediaVenue <pyrogram.api.types.InputMediaVenue>`, :obj:`InputMediaGifExternal <pyrogram.api.types.InputMediaGifExternal>`, :obj:`InputMediaPhotoExternal <pyrogram.api.types.InputMediaPhotoExternal>`, :obj:`InputMediaDocumentExternal <pyrogram.api.types.InputMediaDocumentExternal>`, :obj:`InputMediaGame <pyrogram.api.types.InputMediaGame>`, :obj:`InputMediaInvoice <pyrogram.api.types.InputMediaInvoice>` or :obj:`InputMediaGeoLive <pyrogram.api.types.InputMediaGeoLive>`
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <pyrogram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <pyrogram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <pyrogram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <pyrogram.api.types.ReplyInlineMarkup>`
        entities (optional): List of either :obj:`MessageEntityUnknown <pyrogram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <pyrogram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <pyrogram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <pyrogram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <pyrogram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <pyrogram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <pyrogram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <pyrogram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <pyrogram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <pyrogram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <pyrogram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <pyrogram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <pyrogram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <pyrogram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <pyrogram.api.types.MessageEntityCashtag>`
        geo_point (optional): Either :obj:`InputGeoPointEmpty <pyrogram.api.types.InputGeoPointEmpty>` or :obj:`InputGeoPoint <pyrogram.api.types.InputGeoPoint>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`UpdatesTooLong <pyrogram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <pyrogram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <pyrogram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <pyrogram.api.types.UpdateShort>`, :obj:`UpdatesCombined <pyrogram.api.types.UpdatesCombined>`, :obj:`Update <pyrogram.api.types.Update>` or :obj:`UpdateShortSentMessage <pyrogram.api.types.UpdateShortSentMessage>`
    """

    ID = 0xc000e4c8

    def __init__(self, peer, id: int, no_webpage: bool = None, stop_geo_live: bool = None, message: str = None, media=None, reply_markup=None, entities: list = None, geo_point=None):
        self.no_webpage = no_webpage  # flags.1?true
        self.stop_geo_live = stop_geo_live  # flags.12?true
        self.peer = peer  # InputPeer
        self.id = id  # int
        self.message = message  # flags.11?string
        self.media = media  # flags.14?InputMedia
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup
        self.entities = entities  # flags.3?Vector<MessageEntity>
        self.geo_point = geo_point  # flags.13?InputGeoPoint

    @staticmethod
    def read(b: BytesIO, *args) -> "EditMessage":
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 1) else False
        stop_geo_live = True if flags & (1 << 12) else False
        peer = Object.read(b)
        
        id = Int.read(b)
        
        message = String.read(b) if flags & (1 << 11) else None
        media = Object.read(b) if flags & (1 << 14) else None
        
        reply_markup = Object.read(b) if flags & (1 << 2) else None
        
        entities = Object.read(b) if flags & (1 << 3) else []
        
        geo_point = Object.read(b) if flags & (1 << 13) else None
        
        return EditMessage(peer, id, no_webpage, stop_geo_live, message, media, reply_markup, entities, geo_point)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage is not None else 0
        flags |= (1 << 12) if self.stop_geo_live is not None else 0
        flags |= (1 << 11) if self.message is not None else 0
        flags |= (1 << 14) if self.media is not None else 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        flags |= (1 << 3) if self.entities is not None else 0
        flags |= (1 << 13) if self.geo_point is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.id))
        
        if self.message is not None:
            b.write(String(self.message))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        if self.geo_point is not None:
            b.write(self.geo_point.write())
        
        return b.getvalue()
