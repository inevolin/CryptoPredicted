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


class MessageActionPaymentSentMe(Object):
    """Attributes:
        ID: ``0x8f31b327``

    Args:
        currency: ``str``
        total_amount: ``int`` ``64-bit``
        payload: ``bytes``
        charge: :obj:`PaymentCharge <pyrogram.api.types.PaymentCharge>`
        info (optional): :obj:`PaymentRequestedInfo <pyrogram.api.types.PaymentRequestedInfo>`
        shipping_option_id (optional): ``str``
    """

    ID = 0x8f31b327

    def __init__(self, currency: str, total_amount: int, payload: bytes, charge, info=None, shipping_option_id: str = None):
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.payload = payload  # bytes
        self.info = info  # flags.0?PaymentRequestedInfo
        self.shipping_option_id = shipping_option_id  # flags.1?string
        self.charge = charge  # PaymentCharge

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageActionPaymentSentMe":
        flags = Int.read(b)
        
        currency = String.read(b)
        
        total_amount = Long.read(b)
        
        payload = Bytes.read(b)
        
        info = Object.read(b) if flags & (1 << 0) else None
        
        shipping_option_id = String.read(b) if flags & (1 << 1) else None
        charge = Object.read(b)
        
        return MessageActionPaymentSentMe(currency, total_amount, payload, charge, info, shipping_option_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.info is not None else 0
        flags |= (1 << 1) if self.shipping_option_id is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Long(self.total_amount))
        
        b.write(Bytes(self.payload))
        
        if self.info is not None:
            b.write(self.info.write())
        
        if self.shipping_option_id is not None:
            b.write(String(self.shipping_option_id))
        
        b.write(self.charge.write())
        
        return b.getvalue()
