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


class ReplyKeyboardMarkup(Object):
    """Attributes:
        ID: ``0x3502758c``

    Args:
        rows: List of :obj:`KeyboardButtonRow <pyrogram.api.types.KeyboardButtonRow>`
        resize (optional): ``bool``
        single_use (optional): ``bool``
        selective (optional): ``bool``
    """

    ID = 0x3502758c

    def __init__(self, rows: list, resize: bool = None, single_use: bool = None, selective: bool = None):
        self.resize = resize  # flags.0?true
        self.single_use = single_use  # flags.1?true
        self.selective = selective  # flags.2?true
        self.rows = rows  # Vector<KeyboardButtonRow>

    @staticmethod
    def read(b: BytesIO, *args) -> "ReplyKeyboardMarkup":
        flags = Int.read(b)
        
        resize = True if flags & (1 << 0) else False
        single_use = True if flags & (1 << 1) else False
        selective = True if flags & (1 << 2) else False
        rows = Object.read(b)
        
        return ReplyKeyboardMarkup(rows, resize, single_use, selective)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.resize is not None else 0
        flags |= (1 << 1) if self.single_use is not None else 0
        flags |= (1 << 2) if self.selective is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.rows))
        
        return b.getvalue()
