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


class Invoice(Object):
    """Attributes:
        ID: ``0xc30aa358``

    Args:
        currency: ``str``
        prices: List of :obj:`LabeledPrice <pyrogram.api.types.LabeledPrice>`
        test (optional): ``bool``
        name_requested (optional): ``bool``
        phone_requested (optional): ``bool``
        email_requested (optional): ``bool``
        shipping_address_requested (optional): ``bool``
        flexible (optional): ``bool``
        phone_to_provider (optional): ``bool``
        email_to_provider (optional): ``bool``
    """

    ID = 0xc30aa358

    def __init__(self, currency: str, prices: list, test: bool = None, name_requested: bool = None, phone_requested: bool = None, email_requested: bool = None, shipping_address_requested: bool = None, flexible: bool = None, phone_to_provider: bool = None, email_to_provider: bool = None):
        self.test = test  # flags.0?true
        self.name_requested = name_requested  # flags.1?true
        self.phone_requested = phone_requested  # flags.2?true
        self.email_requested = email_requested  # flags.3?true
        self.shipping_address_requested = shipping_address_requested  # flags.4?true
        self.flexible = flexible  # flags.5?true
        self.phone_to_provider = phone_to_provider  # flags.6?true
        self.email_to_provider = email_to_provider  # flags.7?true
        self.currency = currency  # string
        self.prices = prices  # Vector<LabeledPrice>

    @staticmethod
    def read(b: BytesIO, *args) -> "Invoice":
        flags = Int.read(b)
        
        test = True if flags & (1 << 0) else False
        name_requested = True if flags & (1 << 1) else False
        phone_requested = True if flags & (1 << 2) else False
        email_requested = True if flags & (1 << 3) else False
        shipping_address_requested = True if flags & (1 << 4) else False
        flexible = True if flags & (1 << 5) else False
        phone_to_provider = True if flags & (1 << 6) else False
        email_to_provider = True if flags & (1 << 7) else False
        currency = String.read(b)
        
        prices = Object.read(b)
        
        return Invoice(currency, prices, test, name_requested, phone_requested, email_requested, shipping_address_requested, flexible, phone_to_provider, email_to_provider)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.test is not None else 0
        flags |= (1 << 1) if self.name_requested is not None else 0
        flags |= (1 << 2) if self.phone_requested is not None else 0
        flags |= (1 << 3) if self.email_requested is not None else 0
        flags |= (1 << 4) if self.shipping_address_requested is not None else 0
        flags |= (1 << 5) if self.flexible is not None else 0
        flags |= (1 << 6) if self.phone_to_provider is not None else 0
        flags |= (1 << 7) if self.email_to_provider is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Vector(self.prices))
        
        return b.getvalue()
