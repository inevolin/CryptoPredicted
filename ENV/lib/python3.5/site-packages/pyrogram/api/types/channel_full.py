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


class ChannelFull(Object):
    """Attributes:
        ID: ``0x76af5481``

    Args:
        id: ``int`` ``32-bit``
        about: ``str``
        read_inbox_max_id: ``int`` ``32-bit``
        read_outbox_max_id: ``int`` ``32-bit``
        unread_count: ``int`` ``32-bit``
        chat_photo: Either :obj:`PhotoEmpty <pyrogram.api.types.PhotoEmpty>` or :obj:`Photo <pyrogram.api.types.Photo>`
        notify_settings: :obj:`PeerNotifySettings <pyrogram.api.types.PeerNotifySettings>`
        exported_invite: Either :obj:`ChatInviteEmpty <pyrogram.api.types.ChatInviteEmpty>` or :obj:`ChatInviteExported <pyrogram.api.types.ChatInviteExported>`
        bot_info: List of :obj:`BotInfo <pyrogram.api.types.BotInfo>`
        can_view_participants (optional): ``bool``
        can_set_username (optional): ``bool``
        can_set_stickers (optional): ``bool``
        hidden_prehistory (optional): ``bool``
        participants_count (optional): ``int`` ``32-bit``
        admins_count (optional): ``int`` ``32-bit``
        kicked_count (optional): ``int`` ``32-bit``
        banned_count (optional): ``int`` ``32-bit``
        migrated_from_chat_id (optional): ``int`` ``32-bit``
        migrated_from_max_id (optional): ``int`` ``32-bit``
        pinned_msg_id (optional): ``int`` ``32-bit``
        stickerset (optional): :obj:`StickerSet <pyrogram.api.types.StickerSet>`
        available_min_id (optional): ``int`` ``32-bit``
    """

    ID = 0x76af5481

    def __init__(self, id: int, about: str, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, chat_photo, notify_settings, exported_invite, bot_info: list, can_view_participants: bool = None, can_set_username: bool = None, can_set_stickers: bool = None, hidden_prehistory: bool = None, participants_count: int = None, admins_count: int = None, kicked_count: int = None, banned_count: int = None, migrated_from_chat_id: int = None, migrated_from_max_id: int = None, pinned_msg_id: int = None, stickerset=None, available_min_id: int = None):
        self.can_view_participants = can_view_participants  # flags.3?true
        self.can_set_username = can_set_username  # flags.6?true
        self.can_set_stickers = can_set_stickers  # flags.7?true
        self.hidden_prehistory = hidden_prehistory  # flags.10?true
        self.id = id  # int
        self.about = about  # string
        self.participants_count = participants_count  # flags.0?int
        self.admins_count = admins_count  # flags.1?int
        self.kicked_count = kicked_count  # flags.2?int
        self.banned_count = banned_count  # flags.2?int
        self.read_inbox_max_id = read_inbox_max_id  # int
        self.read_outbox_max_id = read_outbox_max_id  # int
        self.unread_count = unread_count  # int
        self.chat_photo = chat_photo  # Photo
        self.notify_settings = notify_settings  # PeerNotifySettings
        self.exported_invite = exported_invite  # ExportedChatInvite
        self.bot_info = bot_info  # Vector<BotInfo>
        self.migrated_from_chat_id = migrated_from_chat_id  # flags.4?int
        self.migrated_from_max_id = migrated_from_max_id  # flags.4?int
        self.pinned_msg_id = pinned_msg_id  # flags.5?int
        self.stickerset = stickerset  # flags.8?StickerSet
        self.available_min_id = available_min_id  # flags.9?int

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelFull":
        flags = Int.read(b)
        
        can_view_participants = True if flags & (1 << 3) else False
        can_set_username = True if flags & (1 << 6) else False
        can_set_stickers = True if flags & (1 << 7) else False
        hidden_prehistory = True if flags & (1 << 10) else False
        id = Int.read(b)
        
        about = String.read(b)
        
        participants_count = Int.read(b) if flags & (1 << 0) else None
        admins_count = Int.read(b) if flags & (1 << 1) else None
        kicked_count = Int.read(b) if flags & (1 << 2) else None
        banned_count = Int.read(b) if flags & (1 << 2) else None
        read_inbox_max_id = Int.read(b)
        
        read_outbox_max_id = Int.read(b)
        
        unread_count = Int.read(b)
        
        chat_photo = Object.read(b)
        
        notify_settings = Object.read(b)
        
        exported_invite = Object.read(b)
        
        bot_info = Object.read(b)
        
        migrated_from_chat_id = Int.read(b) if flags & (1 << 4) else None
        migrated_from_max_id = Int.read(b) if flags & (1 << 4) else None
        pinned_msg_id = Int.read(b) if flags & (1 << 5) else None
        stickerset = Object.read(b) if flags & (1 << 8) else None
        
        available_min_id = Int.read(b) if flags & (1 << 9) else None
        return ChannelFull(id, about, read_inbox_max_id, read_outbox_max_id, unread_count, chat_photo, notify_settings, exported_invite, bot_info, can_view_participants, can_set_username, can_set_stickers, hidden_prehistory, participants_count, admins_count, kicked_count, banned_count, migrated_from_chat_id, migrated_from_max_id, pinned_msg_id, stickerset, available_min_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.can_view_participants is not None else 0
        flags |= (1 << 6) if self.can_set_username is not None else 0
        flags |= (1 << 7) if self.can_set_stickers is not None else 0
        flags |= (1 << 10) if self.hidden_prehistory is not None else 0
        flags |= (1 << 0) if self.participants_count is not None else 0
        flags |= (1 << 1) if self.admins_count is not None else 0
        flags |= (1 << 2) if self.kicked_count is not None else 0
        flags |= (1 << 2) if self.banned_count is not None else 0
        flags |= (1 << 4) if self.migrated_from_chat_id is not None else 0
        flags |= (1 << 4) if self.migrated_from_max_id is not None else 0
        flags |= (1 << 5) if self.pinned_msg_id is not None else 0
        flags |= (1 << 8) if self.stickerset is not None else 0
        flags |= (1 << 9) if self.available_min_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(String(self.about))
        
        if self.participants_count is not None:
            b.write(Int(self.participants_count))
        
        if self.admins_count is not None:
            b.write(Int(self.admins_count))
        
        if self.kicked_count is not None:
            b.write(Int(self.kicked_count))
        
        if self.banned_count is not None:
            b.write(Int(self.banned_count))
        
        b.write(Int(self.read_inbox_max_id))
        
        b.write(Int(self.read_outbox_max_id))
        
        b.write(Int(self.unread_count))
        
        b.write(self.chat_photo.write())
        
        b.write(self.notify_settings.write())
        
        b.write(self.exported_invite.write())
        
        b.write(Vector(self.bot_info))
        
        if self.migrated_from_chat_id is not None:
            b.write(Int(self.migrated_from_chat_id))
        
        if self.migrated_from_max_id is not None:
            b.write(Int(self.migrated_from_max_id))
        
        if self.pinned_msg_id is not None:
            b.write(Int(self.pinned_msg_id))
        
        if self.stickerset is not None:
            b.write(self.stickerset.write())
        
        if self.available_min_id is not None:
            b.write(Int(self.available_min_id))
        
        return b.getvalue()
