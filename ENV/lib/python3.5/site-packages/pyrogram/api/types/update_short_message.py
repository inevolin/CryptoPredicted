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


class UpdateShortMessage(Object):
    """Attributes:
        ID: ``0x914fbf11``

    Args:
        id: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        message: ``str``
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        out (optional): ``bool``
        mentioned (optional): ``bool``
        media_unread (optional): ``bool``
        silent (optional): ``bool``
        fwd_from (optional): :obj:`MessageFwdHeader <pyrogram.api.types.MessageFwdHeader>`
        via_bot_id (optional): ``int`` ``32-bit``
        reply_to_msg_id (optional): ``int`` ``32-bit``
        entities (optional): List of either :obj:`MessageEntityUnknown <pyrogram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <pyrogram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <pyrogram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <pyrogram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <pyrogram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <pyrogram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <pyrogram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <pyrogram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <pyrogram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <pyrogram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <pyrogram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <pyrogram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <pyrogram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <pyrogram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <pyrogram.api.types.MessageEntityCashtag>`

    See Also:
        This object can be returned by :obj:`messages.SendMessage <pyrogram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <pyrogram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <pyrogram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <pyrogram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <pyrogram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <pyrogram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <pyrogram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <pyrogram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <pyrogram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <pyrogram.api.functions.messages.StartBot>`, :obj:`messages.ToggleChatAdmins <pyrogram.api.functions.messages.ToggleChatAdmins>`, :obj:`messages.MigrateChat <pyrogram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <pyrogram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <pyrogram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <pyrogram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <pyrogram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <pyrogram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <pyrogram.api.functions.messages.SendMultiMedia>`, :obj:`help.GetAppChangelog <pyrogram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <pyrogram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <pyrogram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <pyrogram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <pyrogram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <pyrogram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <pyrogram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <pyrogram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <pyrogram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleInvites <pyrogram.api.functions.channels.ToggleInvites>`, :obj:`channels.ToggleSignatures <pyrogram.api.functions.channels.ToggleSignatures>`, :obj:`channels.UpdatePinnedMessage <pyrogram.api.functions.channels.UpdatePinnedMessage>`, :obj:`channels.EditBanned <pyrogram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <pyrogram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <pyrogram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <pyrogram.api.functions.phone.SetCallRating>`.
    """

    ID = 0x914fbf11

    def __init__(self, id: int, user_id: int, message: str, pts: int, pts_count: int, date: int, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, fwd_from=None, via_bot_id: int = None, reply_to_msg_id: int = None, entities: list = None):
        self.out = out  # flags.1?true
        self.mentioned = mentioned  # flags.4?true
        self.media_unread = media_unread  # flags.5?true
        self.silent = silent  # flags.13?true
        self.id = id  # int
        self.user_id = user_id  # int
        self.message = message  # string
        self.pts = pts  # int
        self.pts_count = pts_count  # int
        self.date = date  # int
        self.fwd_from = fwd_from  # flags.2?MessageFwdHeader
        self.via_bot_id = via_bot_id  # flags.11?int
        self.reply_to_msg_id = reply_to_msg_id  # flags.3?int
        self.entities = entities  # flags.7?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateShortMessage":
        flags = Int.read(b)
        
        out = True if flags & (1 << 1) else False
        mentioned = True if flags & (1 << 4) else False
        media_unread = True if flags & (1 << 5) else False
        silent = True if flags & (1 << 13) else False
        id = Int.read(b)
        
        user_id = Int.read(b)
        
        message = String.read(b)
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        date = Int.read(b)
        
        fwd_from = Object.read(b) if flags & (1 << 2) else None
        
        via_bot_id = Int.read(b) if flags & (1 << 11) else None
        reply_to_msg_id = Int.read(b) if flags & (1 << 3) else None
        entities = Object.read(b) if flags & (1 << 7) else []
        
        return UpdateShortMessage(id, user_id, message, pts, pts_count, date, out, mentioned, media_unread, silent, fwd_from, via_bot_id, reply_to_msg_id, entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out is not None else 0
        flags |= (1 << 4) if self.mentioned is not None else 0
        flags |= (1 << 5) if self.media_unread is not None else 0
        flags |= (1 << 13) if self.silent is not None else 0
        flags |= (1 << 2) if self.fwd_from is not None else 0
        flags |= (1 << 11) if self.via_bot_id is not None else 0
        flags |= (1 << 3) if self.reply_to_msg_id is not None else 0
        flags |= (1 << 7) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(Int(self.user_id))
        
        b.write(String(self.message))
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        b.write(Int(self.date))
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        if self.via_bot_id is not None:
            b.write(Int(self.via_bot_id))
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
