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


class UpdateChatUserTyping(Object):
    """Attributes:
        ID: ``0x9a65ea1f``

    Args:
        chat_id: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        action: Either :obj:`SendMessageTypingAction <pyrogram.api.types.SendMessageTypingAction>`, :obj:`SendMessageCancelAction <pyrogram.api.types.SendMessageCancelAction>`, :obj:`SendMessageRecordVideoAction <pyrogram.api.types.SendMessageRecordVideoAction>`, :obj:`SendMessageUploadVideoAction <pyrogram.api.types.SendMessageUploadVideoAction>`, :obj:`SendMessageRecordAudioAction <pyrogram.api.types.SendMessageRecordAudioAction>`, :obj:`SendMessageUploadAudioAction <pyrogram.api.types.SendMessageUploadAudioAction>`, :obj:`SendMessageUploadPhotoAction <pyrogram.api.types.SendMessageUploadPhotoAction>`, :obj:`SendMessageUploadDocumentAction <pyrogram.api.types.SendMessageUploadDocumentAction>`, :obj:`SendMessageGeoLocationAction <pyrogram.api.types.SendMessageGeoLocationAction>`, :obj:`SendMessageChooseContactAction <pyrogram.api.types.SendMessageChooseContactAction>`, :obj:`SendMessageGamePlayAction <pyrogram.api.types.SendMessageGamePlayAction>`, :obj:`SendMessageRecordRoundAction <pyrogram.api.types.SendMessageRecordRoundAction>` or :obj:`SendMessageUploadRoundAction <pyrogram.api.types.SendMessageUploadRoundAction>`
    """

    ID = 0x9a65ea1f

    def __init__(self, chat_id: int, user_id: int, action):
        self.chat_id = chat_id  # int
        self.user_id = user_id  # int
        self.action = action  # SendMessageAction

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateChatUserTyping":
        # No flags
        
        chat_id = Int.read(b)
        
        user_id = Int.read(b)
        
        action = Object.read(b)
        
        return UpdateChatUserTyping(chat_id, user_id, action)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(Int(self.user_id))
        
        b.write(self.action.write())
        
        return b.getvalue()
