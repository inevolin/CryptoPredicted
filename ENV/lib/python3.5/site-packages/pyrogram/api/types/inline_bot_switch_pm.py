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


class InlineBotSwitchPM(Object):
    """Attributes:
        ID: ``0x3c20629f``

    Args:
        text: ``str``
        start_param: ``str``
    """

    ID = 0x3c20629f

    def __init__(self, text: str, start_param: str):
        self.text = text  # string
        self.start_param = start_param  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "InlineBotSwitchPM":
        # No flags
        
        text = String.read(b)
        
        start_param = String.read(b)
        
        return InlineBotSwitchPM(text, start_param)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        b.write(String(self.start_param))
        
        return b.getvalue()
