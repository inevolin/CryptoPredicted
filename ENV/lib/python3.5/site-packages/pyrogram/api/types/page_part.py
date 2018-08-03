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


class PagePart(Object):
    """Attributes:
        ID: ``0x8e3f9ebe``

    Args:
        blocks: List of either :obj:`PageBlockUnsupported <pyrogram.api.types.PageBlockUnsupported>`, :obj:`PageBlockTitle <pyrogram.api.types.PageBlockTitle>`, :obj:`PageBlockSubtitle <pyrogram.api.types.PageBlockSubtitle>`, :obj:`PageBlockAuthorDate <pyrogram.api.types.PageBlockAuthorDate>`, :obj:`PageBlockHeader <pyrogram.api.types.PageBlockHeader>`, :obj:`PageBlockSubheader <pyrogram.api.types.PageBlockSubheader>`, :obj:`PageBlockParagraph <pyrogram.api.types.PageBlockParagraph>`, :obj:`PageBlockPreformatted <pyrogram.api.types.PageBlockPreformatted>`, :obj:`PageBlockFooter <pyrogram.api.types.PageBlockFooter>`, :obj:`PageBlockDivider <pyrogram.api.types.PageBlockDivider>`, :obj:`PageBlockAnchor <pyrogram.api.types.PageBlockAnchor>`, :obj:`PageBlockList <pyrogram.api.types.PageBlockList>`, :obj:`PageBlockBlockquote <pyrogram.api.types.PageBlockBlockquote>`, :obj:`PageBlockPullquote <pyrogram.api.types.PageBlockPullquote>`, :obj:`PageBlockPhoto <pyrogram.api.types.PageBlockPhoto>`, :obj:`PageBlockVideo <pyrogram.api.types.PageBlockVideo>`, :obj:`PageBlockCover <pyrogram.api.types.PageBlockCover>`, :obj:`PageBlockEmbed <pyrogram.api.types.PageBlockEmbed>`, :obj:`PageBlockEmbedPost <pyrogram.api.types.PageBlockEmbedPost>`, :obj:`PageBlockCollage <pyrogram.api.types.PageBlockCollage>`, :obj:`PageBlockSlideshow <pyrogram.api.types.PageBlockSlideshow>`, :obj:`PageBlockChannel <pyrogram.api.types.PageBlockChannel>` or :obj:`PageBlockAudio <pyrogram.api.types.PageBlockAudio>`
        photos: List of either :obj:`PhotoEmpty <pyrogram.api.types.PhotoEmpty>` or :obj:`Photo <pyrogram.api.types.Photo>`
        documents: List of either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`
    """

    ID = 0x8e3f9ebe

    def __init__(self, blocks: list, photos: list, documents: list):
        self.blocks = blocks  # Vector<PageBlock>
        self.photos = photos  # Vector<Photo>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "PagePart":
        # No flags
        
        blocks = Object.read(b)
        
        photos = Object.read(b)
        
        documents = Object.read(b)
        
        return PagePart(blocks, photos, documents)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.blocks))
        
        b.write(Vector(self.photos))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
