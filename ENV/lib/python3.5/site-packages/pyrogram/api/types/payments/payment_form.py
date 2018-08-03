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


class PaymentForm(Object):
    """Attributes:
        ID: ``0x3f56aea3``

    Args:
        bot_id: ``int`` ``32-bit``
        invoice: :obj:`Invoice <pyrogram.api.types.Invoice>`
        provider_id: ``int`` ``32-bit``
        url: ``str``
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        can_save_credentials (optional): ``bool``
        password_missing (optional): ``bool``
        native_provider (optional): ``str``
        native_params (optional): :obj:`DataJSON <pyrogram.api.types.DataJSON>`
        saved_info (optional): :obj:`PaymentRequestedInfo <pyrogram.api.types.PaymentRequestedInfo>`
        saved_credentials (optional): :obj:`PaymentSavedCredentialsCard <pyrogram.api.types.PaymentSavedCredentialsCard>`

    See Also:
        This object can be returned by :obj:`payments.GetPaymentForm <pyrogram.api.functions.payments.GetPaymentForm>`.
    """

    ID = 0x3f56aea3

    def __init__(self, bot_id: int, invoice, provider_id: int, url: str, users: list, can_save_credentials: bool = None, password_missing: bool = None, native_provider: str = None, native_params=None, saved_info=None, saved_credentials=None):
        self.can_save_credentials = can_save_credentials  # flags.2?true
        self.password_missing = password_missing  # flags.3?true
        self.bot_id = bot_id  # int
        self.invoice = invoice  # Invoice
        self.provider_id = provider_id  # int
        self.url = url  # string
        self.native_provider = native_provider  # flags.4?string
        self.native_params = native_params  # flags.4?DataJSON
        self.saved_info = saved_info  # flags.0?PaymentRequestedInfo
        self.saved_credentials = saved_credentials  # flags.1?PaymentSavedCredentials
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "PaymentForm":
        flags = Int.read(b)
        
        can_save_credentials = True if flags & (1 << 2) else False
        password_missing = True if flags & (1 << 3) else False
        bot_id = Int.read(b)
        
        invoice = Object.read(b)
        
        provider_id = Int.read(b)
        
        url = String.read(b)
        
        native_provider = String.read(b) if flags & (1 << 4) else None
        native_params = Object.read(b) if flags & (1 << 4) else None
        
        saved_info = Object.read(b) if flags & (1 << 0) else None
        
        saved_credentials = Object.read(b) if flags & (1 << 1) else None
        
        users = Object.read(b)
        
        return PaymentForm(bot_id, invoice, provider_id, url, users, can_save_credentials, password_missing, native_provider, native_params, saved_info, saved_credentials)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.can_save_credentials is not None else 0
        flags |= (1 << 3) if self.password_missing is not None else 0
        flags |= (1 << 4) if self.native_provider is not None else 0
        flags |= (1 << 4) if self.native_params is not None else 0
        flags |= (1 << 0) if self.saved_info is not None else 0
        flags |= (1 << 1) if self.saved_credentials is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.bot_id))
        
        b.write(self.invoice.write())
        
        b.write(Int(self.provider_id))
        
        b.write(String(self.url))
        
        if self.native_provider is not None:
            b.write(String(self.native_provider))
        
        if self.native_params is not None:
            b.write(self.native_params.write())
        
        if self.saved_info is not None:
            b.write(self.saved_info.write())
        
        if self.saved_credentials is not None:
            b.write(self.saved_credentials.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
