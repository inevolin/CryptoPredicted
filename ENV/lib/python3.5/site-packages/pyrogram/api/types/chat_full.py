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


class ChatFull(Object):
    """Attributes:
        ID: ``0x2e02a614``

    Args:
        id: ``int`` ``32-bit``
        participants: Either :obj:`ChatParticipantsForbidden <pyrogram.api.types.ChatParticipantsForbidden>` or :obj:`ChatParticipants <pyrogram.api.types.ChatParticipants>`
        chat_photo: Either :obj:`PhotoEmpty <pyrogram.api.types.PhotoEmpty>` or :obj:`Photo <pyrogram.api.types.Photo>`
        notify_settings: :obj:`PeerNotifySettings <pyrogram.api.types.PeerNotifySettings>`
        exported_invite: Either :obj:`ChatInviteEmpty <pyrogram.api.types.ChatInviteEmpty>` or :obj:`ChatInviteExported <pyrogram.api.types.ChatInviteExported>`
        bot_info: List of :obj:`BotInfo <pyrogram.api.types.BotInfo>`
    """

    ID = 0x2e02a614

    def __init__(self, id: int, participants, chat_photo, notify_settings, exported_invite, bot_info: list):
        self.id = id  # int
        self.participants = participants  # ChatParticipants
        self.chat_photo = chat_photo  # Photo
        self.notify_settings = notify_settings  # PeerNotifySettings
        self.exported_invite = exported_invite  # ExportedChatInvite
        self.bot_info = bot_info  # Vector<BotInfo>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatFull":
        # No flags
        
        id = Int.read(b)
        
        participants = Object.read(b)
        
        chat_photo = Object.read(b)
        
        notify_settings = Object.read(b)
        
        exported_invite = Object.read(b)
        
        bot_info = Object.read(b)
        
        return ChatFull(id, participants, chat_photo, notify_settings, exported_invite, bot_info)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(self.participants.write())
        
        b.write(self.chat_photo.write())
        
        b.write(self.notify_settings.write())
        
        b.write(self.exported_invite.write())
        
        b.write(Vector(self.bot_info))
        
        return b.getvalue()
