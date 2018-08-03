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


class KeyboardButtonRow(Object):
    """Attributes:
        ID: ``0x77608b83``

    Args:
        buttons: List of either :obj:`KeyboardButton <pyrogram.api.types.KeyboardButton>`, :obj:`KeyboardButtonUrl <pyrogram.api.types.KeyboardButtonUrl>`, :obj:`KeyboardButtonCallback <pyrogram.api.types.KeyboardButtonCallback>`, :obj:`KeyboardButtonRequestPhone <pyrogram.api.types.KeyboardButtonRequestPhone>`, :obj:`KeyboardButtonRequestGeoLocation <pyrogram.api.types.KeyboardButtonRequestGeoLocation>`, :obj:`KeyboardButtonSwitchInline <pyrogram.api.types.KeyboardButtonSwitchInline>`, :obj:`KeyboardButtonGame <pyrogram.api.types.KeyboardButtonGame>` or :obj:`KeyboardButtonBuy <pyrogram.api.types.KeyboardButtonBuy>`
    """

    ID = 0x77608b83

    def __init__(self, buttons: list):
        self.buttons = buttons  # Vector<KeyboardButton>

    @staticmethod
    def read(b: BytesIO, *args) -> "KeyboardButtonRow":
        # No flags
        
        buttons = Object.read(b)
        
        return KeyboardButtonRow(buttons)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.buttons))
        
        return b.getvalue()
