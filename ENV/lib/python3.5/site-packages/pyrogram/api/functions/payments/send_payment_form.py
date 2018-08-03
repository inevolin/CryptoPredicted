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


class SendPaymentForm(Object):
    """Attributes:
        ID: ``0x2b8879b3``

    Args:
        msg_id: ``int`` ``32-bit``
        credentials: Either :obj:`InputPaymentCredentialsSaved <pyrogram.api.types.InputPaymentCredentialsSaved>`, :obj:`InputPaymentCredentials <pyrogram.api.types.InputPaymentCredentials>`, :obj:`InputPaymentCredentialsApplePay <pyrogram.api.types.InputPaymentCredentialsApplePay>` or :obj:`InputPaymentCredentialsAndroidPay <pyrogram.api.types.InputPaymentCredentialsAndroidPay>`
        requested_info_id (optional): ``str``
        shipping_option_id (optional): ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`payments.PaymentResult <pyrogram.api.types.payments.PaymentResult>` or :obj:`payments.PaymentVerficationNeeded <pyrogram.api.types.payments.PaymentVerficationNeeded>`
    """

    ID = 0x2b8879b3

    def __init__(self, msg_id: int, credentials, requested_info_id: str = None, shipping_option_id: str = None):
        self.msg_id = msg_id  # int
        self.requested_info_id = requested_info_id  # flags.0?string
        self.shipping_option_id = shipping_option_id  # flags.1?string
        self.credentials = credentials  # InputPaymentCredentials

    @staticmethod
    def read(b: BytesIO, *args) -> "SendPaymentForm":
        flags = Int.read(b)
        
        msg_id = Int.read(b)
        
        requested_info_id = String.read(b) if flags & (1 << 0) else None
        shipping_option_id = String.read(b) if flags & (1 << 1) else None
        credentials = Object.read(b)
        
        return SendPaymentForm(msg_id, credentials, requested_info_id, shipping_option_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.requested_info_id is not None else 0
        flags |= (1 << 1) if self.shipping_option_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.msg_id))
        
        if self.requested_info_id is not None:
            b.write(String(self.requested_info_id))
        
        if self.shipping_option_id is not None:
            b.write(String(self.shipping_option_id))
        
        b.write(self.credentials.write())
        
        return b.getvalue()
