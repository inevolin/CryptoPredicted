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


class DestroySession(Object):
    """Attributes:
        ID: ``0xe7512126``

    Args:
        session_id: ``int`` ``64-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`DestroySessionOk <pyrogram.api.types.DestroySessionOk>` or :obj:`DestroySessionNone <pyrogram.api.types.DestroySessionNone>`
    """

    ID = 0xe7512126

    def __init__(self, session_id: int):
        self.session_id = session_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "DestroySession":
        # No flags
        
        session_id = Long.read(b)
        
        return DestroySession(session_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.session_id))
        
        return b.getvalue()
