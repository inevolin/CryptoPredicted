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


class State(Object):
    """Attributes:
        ID: ``0xa56c2a3e``

    Args:
        pts: ``int`` ``32-bit``
        qts: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        seq: ``int`` ``32-bit``
        unread_count: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`updates.GetState <pyrogram.api.functions.updates.GetState>`.
    """

    ID = 0xa56c2a3e

    def __init__(self, pts: int, qts: int, date: int, seq: int, unread_count: int):
        self.pts = pts  # int
        self.qts = qts  # int
        self.date = date  # int
        self.seq = seq  # int
        self.unread_count = unread_count  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "State":
        # No flags
        
        pts = Int.read(b)
        
        qts = Int.read(b)
        
        date = Int.read(b)
        
        seq = Int.read(b)
        
        unread_count = Int.read(b)
        
        return State(pts, qts, date, seq, unread_count)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pts))
        
        b.write(Int(self.qts))
        
        b.write(Int(self.date))
        
        b.write(Int(self.seq))
        
        b.write(Int(self.unread_count))
        
        return b.getvalue()
