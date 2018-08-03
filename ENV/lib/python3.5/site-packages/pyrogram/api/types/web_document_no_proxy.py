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


class WebDocumentNoProxy(Object):
    """Attributes:
        ID: ``0xf9c8bcc6``

    Args:
        url: ``str``
        size: ``int`` ``32-bit``
        mime_type: ``str``
        attributes: List of either :obj:`DocumentAttributeImageSize <pyrogram.api.types.DocumentAttributeImageSize>`, :obj:`DocumentAttributeAnimated <pyrogram.api.types.DocumentAttributeAnimated>`, :obj:`DocumentAttributeSticker <pyrogram.api.types.DocumentAttributeSticker>`, :obj:`DocumentAttributeVideo <pyrogram.api.types.DocumentAttributeVideo>`, :obj:`DocumentAttributeAudio <pyrogram.api.types.DocumentAttributeAudio>`, :obj:`DocumentAttributeFilename <pyrogram.api.types.DocumentAttributeFilename>` or :obj:`DocumentAttributeHasStickers <pyrogram.api.types.DocumentAttributeHasStickers>`
    """

    ID = 0xf9c8bcc6

    def __init__(self, url: str, size: int, mime_type: str, attributes: list):
        self.url = url  # string
        self.size = size  # int
        self.mime_type = mime_type  # string
        self.attributes = attributes  # Vector<DocumentAttribute>

    @staticmethod
    def read(b: BytesIO, *args) -> "WebDocumentNoProxy":
        # No flags
        
        url = String.read(b)
        
        size = Int.read(b)
        
        mime_type = String.read(b)
        
        attributes = Object.read(b)
        
        return WebDocumentNoProxy(url, size, mime_type, attributes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.size))
        
        b.write(String(self.mime_type))
        
        b.write(Vector(self.attributes))
        
        return b.getvalue()
