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


class InputPaymentCredentialsAndroidPay(Object):
    """Attributes:
        ID: ``0xca05d50e``

    Args:
        payment_token: :obj:`DataJSON <pyrogram.api.types.DataJSON>`
        google_transaction_id: ``str``
    """

    ID = 0xca05d50e

    def __init__(self, payment_token, google_transaction_id: str):
        self.payment_token = payment_token  # DataJSON
        self.google_transaction_id = google_transaction_id  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "InputPaymentCredentialsAndroidPay":
        # No flags
        
        payment_token = Object.read(b)
        
        google_transaction_id = String.read(b)
        
        return InputPaymentCredentialsAndroidPay(payment_token, google_transaction_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.payment_token.write())
        
        b.write(String(self.google_transaction_id))
        
        return b.getvalue()
