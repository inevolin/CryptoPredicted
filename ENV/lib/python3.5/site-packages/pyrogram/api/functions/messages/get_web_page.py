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


class GetWebPage(Object):
    """Attributes:
        ID: ``0x32ca8f91``

    Args:
        url: ``str``
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`WebPageEmpty <pyrogram.api.types.WebPageEmpty>`, :obj:`WebPagePending <pyrogram.api.types.WebPagePending>`, :obj:`WebPage <pyrogram.api.types.WebPage>` or :obj:`WebPageNotModified <pyrogram.api.types.WebPageNotModified>`
    """

    ID = 0x32ca8f91

    def __init__(self, url: str, hash: int):
        self.url = url  # string
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetWebPage":
        # No flags
        
        url = String.read(b)
        
        hash = Int.read(b)
        
        return GetWebPage(url, hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
