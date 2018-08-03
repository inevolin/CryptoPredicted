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


class ReorderPinnedDialogs(Object):
    """Attributes:
        ID: ``0x5b51d63f``

    Args:
        order: List of :obj:`InputDialogPeer <pyrogram.api.types.InputDialogPeer>`
        force (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x5b51d63f

    def __init__(self, order: list, force: bool = None):
        self.force = force  # flags.0?true
        self.order = order  # Vector<InputDialogPeer>

    @staticmethod
    def read(b: BytesIO, *args) -> "ReorderPinnedDialogs":
        flags = Int.read(b)
        
        force = True if flags & (1 << 0) else False
        order = Object.read(b)
        
        return ReorderPinnedDialogs(order, force)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.force is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.order))
        
        return b.getvalue()
