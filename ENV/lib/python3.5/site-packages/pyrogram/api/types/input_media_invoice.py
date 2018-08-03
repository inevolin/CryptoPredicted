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


class InputMediaInvoice(Object):
    """Attributes:
        ID: ``0xf4e096c3``

    Args:
        title: ``str``
        description: ``str``
        invoice: :obj:`Invoice <pyrogram.api.types.Invoice>`
        payload: ``bytes``
        provider: ``str``
        provider_data: :obj:`DataJSON <pyrogram.api.types.DataJSON>`
        start_param: ``str``
        photo (optional): :obj:`InputWebDocument <pyrogram.api.types.InputWebDocument>`
    """

    ID = 0xf4e096c3

    def __init__(self, title: str, description: str, invoice, payload: bytes, provider: str, provider_data, start_param: str, photo=None):
        self.title = title  # string
        self.description = description  # string
        self.photo = photo  # flags.0?InputWebDocument
        self.invoice = invoice  # Invoice
        self.payload = payload  # bytes
        self.provider = provider  # string
        self.provider_data = provider_data  # DataJSON
        self.start_param = start_param  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "InputMediaInvoice":
        flags = Int.read(b)
        
        title = String.read(b)
        
        description = String.read(b)
        
        photo = Object.read(b) if flags & (1 << 0) else None
        
        invoice = Object.read(b)
        
        payload = Bytes.read(b)
        
        provider = String.read(b)
        
        provider_data = Object.read(b)
        
        start_param = String.read(b)
        
        return InputMediaInvoice(title, description, invoice, payload, provider, provider_data, start_param, photo)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.photo is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        b.write(String(self.description))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        b.write(self.invoice.write())
        
        b.write(Bytes(self.payload))
        
        b.write(String(self.provider))
        
        b.write(self.provider_data.write())
        
        b.write(String(self.start_param))
        
        return b.getvalue()
