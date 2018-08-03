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


class Message(Object):
    """Attributes:
        ID: ``0x44f9b43d``

    Args:
        id: ``int`` ``32-bit``
        to_id: Either :obj:`PeerUser <pyrogram.api.types.PeerUser>`, :obj:`PeerChat <pyrogram.api.types.PeerChat>` or :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`
        date: ``int`` ``32-bit``
        message: ``str``
        out (optional): ``bool``
        mentioned (optional): ``bool``
        media_unread (optional): ``bool``
        silent (optional): ``bool``
        post (optional): ``bool``
        from_id (optional): ``int`` ``32-bit``
        fwd_from (optional): :obj:`MessageFwdHeader <pyrogram.api.types.MessageFwdHeader>`
        via_bot_id (optional): ``int`` ``32-bit``
        reply_to_msg_id (optional): ``int`` ``32-bit``
        media (optional): Either :obj:`MessageMediaEmpty <pyrogram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <pyrogram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <pyrogram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <pyrogram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <pyrogram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <pyrogram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <pyrogram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <pyrogram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <pyrogram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <pyrogram.api.types.MessageMediaInvoice>` or :obj:`MessageMediaGeoLive <pyrogram.api.types.MessageMediaGeoLive>`
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <pyrogram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <pyrogram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <pyrogram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <pyrogram.api.types.ReplyInlineMarkup>`
        entities (optional): List of either :obj:`MessageEntityUnknown <pyrogram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <pyrogram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <pyrogram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <pyrogram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <pyrogram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <pyrogram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <pyrogram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <pyrogram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <pyrogram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <pyrogram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <pyrogram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <pyrogram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <pyrogram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <pyrogram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <pyrogram.api.types.MessageEntityCashtag>`
        views (optional): ``int`` ``32-bit``
        edit_date (optional): ``int`` ``32-bit``
        post_author (optional): ``str``
        grouped_id (optional): ``int`` ``64-bit``
    """

    ID = 0x44f9b43d

    def __init__(self, id: int, to_id, date: int, message: str, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, post: bool = None, from_id: int = None, fwd_from=None, via_bot_id: int = None, reply_to_msg_id: int = None, media=None, reply_markup=None, entities: list = None, views: int = None, edit_date: int = None, post_author: str = None, grouped_id: int = None):
        self.out = out  # flags.1?true
        self.mentioned = mentioned  # flags.4?true
        self.media_unread = media_unread  # flags.5?true
        self.silent = silent  # flags.13?true
        self.post = post  # flags.14?true
        self.id = id  # int
        self.from_id = from_id  # flags.8?int
        self.to_id = to_id  # Peer
        self.fwd_from = fwd_from  # flags.2?MessageFwdHeader
        self.via_bot_id = via_bot_id  # flags.11?int
        self.reply_to_msg_id = reply_to_msg_id  # flags.3?int
        self.date = date  # int
        self.message = message  # string
        self.media = media  # flags.9?MessageMedia
        self.reply_markup = reply_markup  # flags.6?ReplyMarkup
        self.entities = entities  # flags.7?Vector<MessageEntity>
        self.views = views  # flags.10?int
        self.edit_date = edit_date  # flags.15?int
        self.post_author = post_author  # flags.16?string
        self.grouped_id = grouped_id  # flags.17?long

    @staticmethod
    def read(b: BytesIO, *args) -> "Message":
        flags = Int.read(b)
        
        out = True if flags & (1 << 1) else False
        mentioned = True if flags & (1 << 4) else False
        media_unread = True if flags & (1 << 5) else False
        silent = True if flags & (1 << 13) else False
        post = True if flags & (1 << 14) else False
        id = Int.read(b)
        
        from_id = Int.read(b) if flags & (1 << 8) else None
        to_id = Object.read(b)
        
        fwd_from = Object.read(b) if flags & (1 << 2) else None
        
        via_bot_id = Int.read(b) if flags & (1 << 11) else None
        reply_to_msg_id = Int.read(b) if flags & (1 << 3) else None
        date = Int.read(b)
        
        message = String.read(b)
        
        media = Object.read(b) if flags & (1 << 9) else None
        
        reply_markup = Object.read(b) if flags & (1 << 6) else None
        
        entities = Object.read(b) if flags & (1 << 7) else []
        
        views = Int.read(b) if flags & (1 << 10) else None
        edit_date = Int.read(b) if flags & (1 << 15) else None
        post_author = String.read(b) if flags & (1 << 16) else None
        grouped_id = Long.read(b) if flags & (1 << 17) else None
        return Message(id, to_id, date, message, out, mentioned, media_unread, silent, post, from_id, fwd_from, via_bot_id, reply_to_msg_id, media, reply_markup, entities, views, edit_date, post_author, grouped_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out is not None else 0
        flags |= (1 << 4) if self.mentioned is not None else 0
        flags |= (1 << 5) if self.media_unread is not None else 0
        flags |= (1 << 13) if self.silent is not None else 0
        flags |= (1 << 14) if self.post is not None else 0
        flags |= (1 << 8) if self.from_id is not None else 0
        flags |= (1 << 2) if self.fwd_from is not None else 0
        flags |= (1 << 11) if self.via_bot_id is not None else 0
        flags |= (1 << 3) if self.reply_to_msg_id is not None else 0
        flags |= (1 << 9) if self.media is not None else 0
        flags |= (1 << 6) if self.reply_markup is not None else 0
        flags |= (1 << 7) if self.entities is not None else 0
        flags |= (1 << 10) if self.views is not None else 0
        flags |= (1 << 15) if self.edit_date is not None else 0
        flags |= (1 << 16) if self.post_author is not None else 0
        flags |= (1 << 17) if self.grouped_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        if self.from_id is not None:
            b.write(Int(self.from_id))
        
        b.write(self.to_id.write())
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        if self.via_bot_id is not None:
            b.write(Int(self.via_bot_id))
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(Int(self.date))
        
        b.write(String(self.message))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        if self.views is not None:
            b.write(Int(self.views))
        
        if self.edit_date is not None:
            b.write(Int(self.edit_date))
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.grouped_id is not None:
            b.write(Long(self.grouped_id))
        
        return b.getvalue()
