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


class WebDocument(Object):
    """Attributes:
        ID: ``0xc61acbd8``

    Args:
        url: ``str``
        access_hash: ``int`` ``64-bit``
        size: ``int`` ``32-bit``
        mime_type: ``str``
        attributes: List of either :obj:`DocumentAttributeImageSize <pyrogram.api.types.DocumentAttributeImageSize>`, :obj:`DocumentAttributeAnimated <pyrogram.api.types.DocumentAttributeAnimated>`, :obj:`DocumentAttributeSticker <pyrogram.api.types.DocumentAttributeSticker>`, :obj:`DocumentAttributeVideo <pyrogram.api.types.DocumentAttributeVideo>`, :obj:`DocumentAttributeAudio <pyrogram.api.types.DocumentAttributeAudio>`, :obj:`DocumentAttributeFilename <pyrogram.api.types.DocumentAttributeFilename>` or :obj:`DocumentAttributeHasStickers <pyrogram.api.types.DocumentAttributeHasStickers>`
        dc_id: ``int`` ``32-bit``
    """

    ID = 0xc61acbd8

    def __init__(self, url: str, access_hash: int, size: int, mime_type: str, attributes: list, dc_id: int):
        self.url = url  # string
        self.access_hash = access_hash  # long
        self.size = size  # int
        self.mime_type = mime_type  # string
        self.attributes = attributes  # Vector<DocumentAttribute>
        self.dc_id = dc_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "WebDocument":
        # No flags
        
        url = String.read(b)
        
        access_hash = Long.read(b)
        
        size = Int.read(b)
        
        mime_type = String.read(b)
        
        attributes = Object.read(b)
        
        dc_id = Int.read(b)
        
        return WebDocument(url, access_hash, size, mime_type, attributes, dc_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Long(self.access_hash))
        
        b.write(Int(self.size))
        
        b.write(String(self.mime_type))
        
        b.write(Vector(self.attributes))
        
        b.write(Int(self.dc_id))
        
        return b.getvalue()
