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


class PaymentCharge(Object):
    """Attributes:
        ID: ``0xea02c27e``

    Args:
        id: ``str``
        provider_charge_id: ``str``
    """

    ID = 0xea02c27e

    def __init__(self, id: str, provider_charge_id: str):
        self.id = id  # string
        self.provider_charge_id = provider_charge_id  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "PaymentCharge":
        # No flags
        
        id = String.read(b)
        
        provider_charge_id = String.read(b)
        
        return PaymentCharge(id, provider_charge_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(String(self.provider_charge_id))
        
        return b.getvalue()
