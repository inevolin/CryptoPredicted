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


class AffectedMessages(Object):
    """Attributes:
        ID: ``0x84d19185``

    Args:
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.ReadHistory <pyrogram.api.functions.messages.ReadHistory>`, :obj:`messages.DeleteMessages <pyrogram.api.functions.messages.DeleteMessages>`, :obj:`messages.ReadMessageContents <pyrogram.api.functions.messages.ReadMessageContents>` and :obj:`channels.DeleteMessages <pyrogram.api.functions.channels.DeleteMessages>`.
    """

    ID = 0x84d19185

    def __init__(self, pts: int, pts_count: int):
        self.pts = pts  # int
        self.pts_count = pts_count  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "AffectedMessages":
        # No flags
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        return AffectedMessages(pts, pts_count)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        return b.getvalue()
