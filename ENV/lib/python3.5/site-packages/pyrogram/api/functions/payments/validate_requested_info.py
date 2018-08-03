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


class ValidateRequestedInfo(Object):
    """Attributes:
        ID: ``0x770a8e74``

    Args:
        msg_id: ``int`` ``32-bit``
        info: :obj:`PaymentRequestedInfo <pyrogram.api.types.PaymentRequestedInfo>`
        save (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`payments.ValidatedRequestedInfo <pyrogram.api.types.payments.ValidatedRequestedInfo>`
    """

    ID = 0x770a8e74

    def __init__(self, msg_id: int, info, save: bool = None):
        self.save = save  # flags.0?true
        self.msg_id = msg_id  # int
        self.info = info  # PaymentRequestedInfo

    @staticmethod
    def read(b: BytesIO, *args) -> "ValidateRequestedInfo":
        flags = Int.read(b)
        
        save = True if flags & (1 << 0) else False
        msg_id = Int.read(b)
        
        info = Object.read(b)
        
        return ValidateRequestedInfo(msg_id, info, save)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.save is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.msg_id))
        
        b.write(self.info.write())
        
        return b.getvalue()
