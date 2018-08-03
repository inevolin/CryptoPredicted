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


class InputBotInlineMessageMediaContact(Object):
    """Attributes:
        ID: ``0x2daf01a7``

    Args:
        phone_number: ``str``
        first_name: ``str``
        last_name: ``str``
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <pyrogram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <pyrogram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <pyrogram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <pyrogram.api.types.ReplyInlineMarkup>`
    """

    ID = 0x2daf01a7

    def __init__(self, phone_number: str, first_name: str, last_name: str, reply_markup=None):
        self.phone_number = phone_number  # string
        self.first_name = first_name  # string
        self.last_name = last_name  # string
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineMessageMediaContact":
        flags = Int.read(b)
        
        phone_number = String.read(b)
        
        first_name = String.read(b)
        
        last_name = String.read(b)
        
        reply_markup = Object.read(b) if flags & (1 << 2) else None
        
        return InputBotInlineMessageMediaContact(phone_number, first_name, last_name, reply_markup)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.phone_number))
        
        b.write(String(self.first_name))
        
        b.write(String(self.last_name))
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        return b.getvalue()
