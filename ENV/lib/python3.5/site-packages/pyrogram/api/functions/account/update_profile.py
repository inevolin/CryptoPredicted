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


class UpdateProfile(Object):
    """Attributes:
        ID: ``0x78515775``

    Args:
        first_name (optional): ``str``
        last_name (optional): ``str``
        about (optional): ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
    """

    ID = 0x78515775

    def __init__(self, first_name: str = None, last_name: str = None, about: str = None):
        self.first_name = first_name  # flags.0?string
        self.last_name = last_name  # flags.1?string
        self.about = about  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateProfile":
        flags = Int.read(b)
        
        first_name = String.read(b) if flags & (1 << 0) else None
        last_name = String.read(b) if flags & (1 << 1) else None
        about = String.read(b) if flags & (1 << 2) else None
        return UpdateProfile(first_name, last_name, about)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.first_name is not None else 0
        flags |= (1 << 1) if self.last_name is not None else 0
        flags |= (1 << 2) if self.about is not None else 0
        b.write(Int(flags))
        
        if self.first_name is not None:
            b.write(String(self.first_name))
        
        if self.last_name is not None:
            b.write(String(self.last_name))
        
        if self.about is not None:
            b.write(String(self.about))
        
        return b.getvalue()
