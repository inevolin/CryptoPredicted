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


class UpdateBotWebhookJSON(Object):
    """Attributes:
        ID: ``0x8317c0c3``

    Args:
        data: :obj:`DataJSON <pyrogram.api.types.DataJSON>`
    """

    ID = 0x8317c0c3

    def __init__(self, data):
        self.data = data  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateBotWebhookJSON":
        # No flags
        
        data = Object.read(b)
        
        return UpdateBotWebhookJSON(data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.data.write())
        
        return b.getvalue()
