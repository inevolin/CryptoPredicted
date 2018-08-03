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


class RpcError(Object):
    """Attributes:
        ID: ``0x2144ca19``

    Args:
        error_code: ``int`` ``32-bit``
        error_message: ``str``
    """

    ID = 0x2144ca19

    def __init__(self, error_code: int, error_message: str):
        self.error_code = error_code  # int
        self.error_message = error_message  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "RpcError":
        # No flags
        
        error_code = Int.read(b)
        
        error_message = String.read(b)
        
        return RpcError(error_code, error_message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.error_code))
        
        b.write(String(self.error_message))
        
        return b.getvalue()
