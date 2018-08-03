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


class ValidatedRequestedInfo(Object):
    """Attributes:
        ID: ``0xd1451883``

    Args:
        id (optional): ``str``
        shipping_options (optional): List of :obj:`ShippingOption <pyrogram.api.types.ShippingOption>`

    See Also:
        This object can be returned by :obj:`payments.ValidateRequestedInfo <pyrogram.api.functions.payments.ValidateRequestedInfo>`.
    """

    ID = 0xd1451883

    def __init__(self, id: str = None, shipping_options: list = None):
        self.id = id  # flags.0?string
        self.shipping_options = shipping_options  # flags.1?Vector<ShippingOption>

    @staticmethod
    def read(b: BytesIO, *args) -> "ValidatedRequestedInfo":
        flags = Int.read(b)
        
        id = String.read(b) if flags & (1 << 0) else None
        shipping_options = Object.read(b) if flags & (1 << 1) else []
        
        return ValidatedRequestedInfo(id, shipping_options)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.id is not None else 0
        flags |= (1 << 1) if self.shipping_options is not None else 0
        b.write(Int(flags))
        
        if self.id is not None:
            b.write(String(self.id))
        
        if self.shipping_options is not None:
            b.write(Vector(self.shipping_options))
        
        return b.getvalue()
