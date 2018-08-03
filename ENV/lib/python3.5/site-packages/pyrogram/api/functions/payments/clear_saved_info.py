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


class ClearSavedInfo(Object):
    """Attributes:
        ID: ``0xd83d70c1``

    Args:
        credentials (optional): ``bool``
        info (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xd83d70c1

    def __init__(self, credentials: bool = None, info: bool = None):
        self.credentials = credentials  # flags.0?true
        self.info = info  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args) -> "ClearSavedInfo":
        flags = Int.read(b)
        
        credentials = True if flags & (1 << 0) else False
        info = True if flags & (1 << 1) else False
        return ClearSavedInfo(credentials, info)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.credentials is not None else 0
        flags |= (1 << 1) if self.info is not None else 0
        b.write(Int(flags))
        
        return b.getvalue()
