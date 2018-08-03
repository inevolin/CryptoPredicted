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


class MessageActionPhoneCall(Object):
    """Attributes:
        ID: ``0x80e11a7f``

    Args:
        call_id: ``int`` ``64-bit``
        reason (optional): Either :obj:`PhoneCallDiscardReasonMissed <pyrogram.api.types.PhoneCallDiscardReasonMissed>`, :obj:`PhoneCallDiscardReasonDisconnect <pyrogram.api.types.PhoneCallDiscardReasonDisconnect>`, :obj:`PhoneCallDiscardReasonHangup <pyrogram.api.types.PhoneCallDiscardReasonHangup>` or :obj:`PhoneCallDiscardReasonBusy <pyrogram.api.types.PhoneCallDiscardReasonBusy>`
        duration (optional): ``int`` ``32-bit``
    """

    ID = 0x80e11a7f

    def __init__(self, call_id: int, reason=None, duration: int = None):
        self.call_id = call_id  # long
        self.reason = reason  # flags.0?PhoneCallDiscardReason
        self.duration = duration  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageActionPhoneCall":
        flags = Int.read(b)
        
        call_id = Long.read(b)
        
        reason = Object.read(b) if flags & (1 << 0) else None
        
        duration = Int.read(b) if flags & (1 << 1) else None
        return MessageActionPhoneCall(call_id, reason, duration)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.reason is not None else 0
        flags |= (1 << 1) if self.duration is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.call_id))
        
        if self.reason is not None:
            b.write(self.reason.write())
        
        if self.duration is not None:
            b.write(Int(self.duration))
        
        return b.getvalue()
