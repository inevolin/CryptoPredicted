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


class BotCommand(Object):
    """Attributes:
        ID: ``0xc27ac8c7``

    Args:
        command: ``str``
        description: ``str``
    """

    ID = 0xc27ac8c7

    def __init__(self, command: str, description: str):
        self.command = command  # string
        self.description = description  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "BotCommand":
        # No flags
        
        command = String.read(b)
        
        description = String.read(b)
        
        return BotCommand(command, description)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.command))
        
        b.write(String(self.description))
        
        return b.getvalue()
