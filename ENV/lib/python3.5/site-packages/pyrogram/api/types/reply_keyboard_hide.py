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


class ReplyKeyboardHide(Object):
    """Attributes:
        ID: ``0xa03e5b85``

    Args:
        selective (optional): ``bool``
    """

    ID = 0xa03e5b85

    def __init__(self, selective: bool = None):
        self.selective = selective  # flags.2?true

    @staticmethod
    def read(b: BytesIO, *args) -> "ReplyKeyboardHide":
        flags = Int.read(b)
        
        selective = True if flags & (1 << 2) else False
        return ReplyKeyboardHide(selective)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.selective is not None else 0
        b.write(Int(flags))
        
        return b.getvalue()
