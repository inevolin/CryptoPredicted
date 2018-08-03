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


class FoundGifCached(Object):
    """Attributes:
        ID: ``0x9c750409``

    Args:
        url: ``str``
        photo: Either :obj:`PhotoEmpty <pyrogram.api.types.PhotoEmpty>` or :obj:`Photo <pyrogram.api.types.Photo>`
        document: Either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`
    """

    ID = 0x9c750409

    def __init__(self, url: str, photo, document):
        self.url = url  # string
        self.photo = photo  # Photo
        self.document = document  # Document

    @staticmethod
    def read(b: BytesIO, *args) -> "FoundGifCached":
        # No flags
        
        url = String.read(b)
        
        photo = Object.read(b)
        
        document = Object.read(b)
        
        return FoundGifCached(url, photo, document)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(self.photo.write())
        
        b.write(self.document.write())
        
        return b.getvalue()
