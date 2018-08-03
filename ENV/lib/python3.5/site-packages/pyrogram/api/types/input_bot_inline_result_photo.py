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


class InputBotInlineResultPhoto(Object):
    """Attributes:
        ID: ``0xa8d864a7``

    Args:
        id: ``str``
        type: ``str``
        photo: Either :obj:`InputPhotoEmpty <pyrogram.api.types.InputPhotoEmpty>` or :obj:`InputPhoto <pyrogram.api.types.InputPhoto>`
        send_message: Either :obj:`InputBotInlineMessageMediaAuto <pyrogram.api.types.InputBotInlineMessageMediaAuto>`, :obj:`InputBotInlineMessageText <pyrogram.api.types.InputBotInlineMessageText>`, :obj:`InputBotInlineMessageMediaGeo <pyrogram.api.types.InputBotInlineMessageMediaGeo>`, :obj:`InputBotInlineMessageMediaVenue <pyrogram.api.types.InputBotInlineMessageMediaVenue>`, :obj:`InputBotInlineMessageMediaContact <pyrogram.api.types.InputBotInlineMessageMediaContact>` or :obj:`InputBotInlineMessageGame <pyrogram.api.types.InputBotInlineMessageGame>`
    """

    ID = 0xa8d864a7

    def __init__(self, id: str, type: str, photo, send_message):
        self.id = id  # string
        self.type = type  # string
        self.photo = photo  # InputPhoto
        self.send_message = send_message  # InputBotInlineMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineResultPhoto":
        # No flags
        
        id = String.read(b)
        
        type = String.read(b)
        
        photo = Object.read(b)
        
        send_message = Object.read(b)
        
        return InputBotInlineResultPhoto(id, type, photo, send_message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(String(self.type))
        
        b.write(self.photo.write())
        
        b.write(self.send_message.write())
        
        return b.getvalue()
