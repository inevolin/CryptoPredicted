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


class SetTyping(Object):
    """Attributes:
        ID: ``0xa3825e50``

    Args:
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        action: Either :obj:`SendMessageTypingAction <pyrogram.api.types.SendMessageTypingAction>`, :obj:`SendMessageCancelAction <pyrogram.api.types.SendMessageCancelAction>`, :obj:`SendMessageRecordVideoAction <pyrogram.api.types.SendMessageRecordVideoAction>`, :obj:`SendMessageUploadVideoAction <pyrogram.api.types.SendMessageUploadVideoAction>`, :obj:`SendMessageRecordAudioAction <pyrogram.api.types.SendMessageRecordAudioAction>`, :obj:`SendMessageUploadAudioAction <pyrogram.api.types.SendMessageUploadAudioAction>`, :obj:`SendMessageUploadPhotoAction <pyrogram.api.types.SendMessageUploadPhotoAction>`, :obj:`SendMessageUploadDocumentAction <pyrogram.api.types.SendMessageUploadDocumentAction>`, :obj:`SendMessageGeoLocationAction <pyrogram.api.types.SendMessageGeoLocationAction>`, :obj:`SendMessageChooseContactAction <pyrogram.api.types.SendMessageChooseContactAction>`, :obj:`SendMessageGamePlayAction <pyrogram.api.types.SendMessageGamePlayAction>`, :obj:`SendMessageRecordRoundAction <pyrogram.api.types.SendMessageRecordRoundAction>` or :obj:`SendMessageUploadRoundAction <pyrogram.api.types.SendMessageUploadRoundAction>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xa3825e50

    def __init__(self, peer, action):
        self.peer = peer  # InputPeer
        self.action = action  # SendMessageAction

    @staticmethod
    def read(b: BytesIO, *args) -> "SetTyping":
        # No flags
        
        peer = Object.read(b)
        
        action = Object.read(b)
        
        return SetTyping(peer, action)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.action.write())
        
        return b.getvalue()
