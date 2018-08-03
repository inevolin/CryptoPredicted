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


class PageBlockEmbedPost(Object):
    """Attributes:
        ID: ``0x292c7be9``

    Args:
        url: ``str``
        webpage_id: ``int`` ``64-bit``
        author_photo_id: ``int`` ``64-bit``
        author: ``str``
        date: ``int`` ``32-bit``
        blocks: List of either :obj:`PageBlockUnsupported <pyrogram.api.types.PageBlockUnsupported>`, :obj:`PageBlockTitle <pyrogram.api.types.PageBlockTitle>`, :obj:`PageBlockSubtitle <pyrogram.api.types.PageBlockSubtitle>`, :obj:`PageBlockAuthorDate <pyrogram.api.types.PageBlockAuthorDate>`, :obj:`PageBlockHeader <pyrogram.api.types.PageBlockHeader>`, :obj:`PageBlockSubheader <pyrogram.api.types.PageBlockSubheader>`, :obj:`PageBlockParagraph <pyrogram.api.types.PageBlockParagraph>`, :obj:`PageBlockPreformatted <pyrogram.api.types.PageBlockPreformatted>`, :obj:`PageBlockFooter <pyrogram.api.types.PageBlockFooter>`, :obj:`PageBlockDivider <pyrogram.api.types.PageBlockDivider>`, :obj:`PageBlockAnchor <pyrogram.api.types.PageBlockAnchor>`, :obj:`PageBlockList <pyrogram.api.types.PageBlockList>`, :obj:`PageBlockBlockquote <pyrogram.api.types.PageBlockBlockquote>`, :obj:`PageBlockPullquote <pyrogram.api.types.PageBlockPullquote>`, :obj:`PageBlockPhoto <pyrogram.api.types.PageBlockPhoto>`, :obj:`PageBlockVideo <pyrogram.api.types.PageBlockVideo>`, :obj:`PageBlockCover <pyrogram.api.types.PageBlockCover>`, :obj:`PageBlockEmbed <pyrogram.api.types.PageBlockEmbed>`, :obj:`PageBlockEmbedPost <pyrogram.api.types.PageBlockEmbedPost>`, :obj:`PageBlockCollage <pyrogram.api.types.PageBlockCollage>`, :obj:`PageBlockSlideshow <pyrogram.api.types.PageBlockSlideshow>`, :obj:`PageBlockChannel <pyrogram.api.types.PageBlockChannel>` or :obj:`PageBlockAudio <pyrogram.api.types.PageBlockAudio>`
        caption: Either :obj:`TextEmpty <pyrogram.api.types.TextEmpty>`, :obj:`TextPlain <pyrogram.api.types.TextPlain>`, :obj:`TextBold <pyrogram.api.types.TextBold>`, :obj:`TextItalic <pyrogram.api.types.TextItalic>`, :obj:`TextUnderline <pyrogram.api.types.TextUnderline>`, :obj:`TextStrike <pyrogram.api.types.TextStrike>`, :obj:`TextFixed <pyrogram.api.types.TextFixed>`, :obj:`TextUrl <pyrogram.api.types.TextUrl>`, :obj:`TextEmail <pyrogram.api.types.TextEmail>` or :obj:`TextConcat <pyrogram.api.types.TextConcat>`
    """

    ID = 0x292c7be9

    def __init__(self, url: str, webpage_id: int, author_photo_id: int, author: str, date: int, blocks: list, caption):
        self.url = url  # string
        self.webpage_id = webpage_id  # long
        self.author_photo_id = author_photo_id  # long
        self.author = author  # string
        self.date = date  # int
        self.blocks = blocks  # Vector<PageBlock>
        self.caption = caption  # RichText

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockEmbedPost":
        # No flags
        
        url = String.read(b)
        
        webpage_id = Long.read(b)
        
        author_photo_id = Long.read(b)
        
        author = String.read(b)
        
        date = Int.read(b)
        
        blocks = Object.read(b)
        
        caption = Object.read(b)
        
        return PageBlockEmbedPost(url, webpage_id, author_photo_id, author, date, blocks, caption)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Long(self.webpage_id))
        
        b.write(Long(self.author_photo_id))
        
        b.write(String(self.author))
        
        b.write(Int(self.date))
        
        b.write(Vector(self.blocks))
        
        b.write(self.caption.write())
        
        return b.getvalue()
