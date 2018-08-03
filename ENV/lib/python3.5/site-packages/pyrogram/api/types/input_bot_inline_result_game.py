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


class InputBotInlineResultGame(Object):
    """Attributes:
        ID: ``0x4fa417f2``

    Args:
        id: ``str``
        short_name: ``str``
        send_message: Either :obj:`InputBotInlineMessageMediaAuto <pyrogram.api.types.InputBotInlineMessageMediaAuto>`, :obj:`InputBotInlineMessageText <pyrogram.api.types.InputBotInlineMessageText>`, :obj:`InputBotInlineMessageMediaGeo <pyrogram.api.types.InputBotInlineMessageMediaGeo>`, :obj:`InputBotInlineMessageMediaVenue <pyrogram.api.types.InputBotInlineMessageMediaVenue>`, :obj:`InputBotInlineMessageMediaContact <pyrogram.api.types.InputBotInlineMessageMediaContact>` or :obj:`InputBotInlineMessageGame <pyrogram.api.types.InputBotInlineMessageGame>`
    """

    ID = 0x4fa417f2

    def __init__(self, id: str, short_name: str, send_message):
        self.id = id  # string
        self.short_name = short_name  # string
        self.send_message = send_message  # InputBotInlineMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineResultGame":
        # No flags
        
        id = String.read(b)
        
        short_name = String.read(b)
        
        send_message = Object.read(b)
        
        return InputBotInlineResultGame(id, short_name, send_message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(String(self.short_name))
        
        b.write(self.send_message.write())
        
        return b.getvalue()
