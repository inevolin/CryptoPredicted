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


class UpdateWebPage(Object):
    """Attributes:
        ID: ``0x7f891213``

    Args:
        webpage: Either :obj:`WebPageEmpty <pyrogram.api.types.WebPageEmpty>`, :obj:`WebPagePending <pyrogram.api.types.WebPagePending>`, :obj:`WebPage <pyrogram.api.types.WebPage>` or :obj:`WebPageNotModified <pyrogram.api.types.WebPageNotModified>`
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``
    """

    ID = 0x7f891213

    def __init__(self, webpage, pts: int, pts_count: int):
        self.webpage = webpage  # WebPage
        self.pts = pts  # int
        self.pts_count = pts_count  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateWebPage":
        # No flags
        
        webpage = Object.read(b)
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        return UpdateWebPage(webpage, pts, pts_count)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.webpage.write())
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        return b.getvalue()
