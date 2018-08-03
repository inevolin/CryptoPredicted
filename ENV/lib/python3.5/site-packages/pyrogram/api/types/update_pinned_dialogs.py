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


class UpdatePinnedDialogs(Object):
    """Attributes:
        ID: ``0xea4cb65b``

    Args:
        order (optional): List of :obj:`DialogPeer <pyrogram.api.types.DialogPeer>`
    """

    ID = 0xea4cb65b

    def __init__(self, order: list = None):
        self.order = order  # flags.0?Vector<DialogPeer>

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatePinnedDialogs":
        flags = Int.read(b)
        
        order = Object.read(b) if flags & (1 << 0) else []
        
        return UpdatePinnedDialogs(order)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.order is not None else 0
        b.write(Int(flags))
        
        if self.order is not None:
            b.write(Vector(self.order))
        
        return b.getvalue()
