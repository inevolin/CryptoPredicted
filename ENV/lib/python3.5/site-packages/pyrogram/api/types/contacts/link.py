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


class Link(Object):
    """Attributes:
        ID: ``0x3ace484c``

    Args:
        my_link: Either :obj:`ContactLinkUnknown <pyrogram.api.types.ContactLinkUnknown>`, :obj:`ContactLinkNone <pyrogram.api.types.ContactLinkNone>`, :obj:`ContactLinkHasPhone <pyrogram.api.types.ContactLinkHasPhone>` or :obj:`ContactLinkContact <pyrogram.api.types.ContactLinkContact>`
        foreign_link: Either :obj:`ContactLinkUnknown <pyrogram.api.types.ContactLinkUnknown>`, :obj:`ContactLinkNone <pyrogram.api.types.ContactLinkNone>`, :obj:`ContactLinkHasPhone <pyrogram.api.types.ContactLinkHasPhone>` or :obj:`ContactLinkContact <pyrogram.api.types.ContactLinkContact>`
        user: Either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`contacts.DeleteContact <pyrogram.api.functions.contacts.DeleteContact>`.
    """

    ID = 0x3ace484c

    def __init__(self, my_link, foreign_link, user):
        self.my_link = my_link  # ContactLink
        self.foreign_link = foreign_link  # ContactLink
        self.user = user  # User

    @staticmethod
    def read(b: BytesIO, *args) -> "Link":
        # No flags
        
        my_link = Object.read(b)
        
        foreign_link = Object.read(b)
        
        user = Object.read(b)
        
        return Link(my_link, foreign_link, user)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.my_link.write())
        
        b.write(self.foreign_link.write())
        
        b.write(self.user.write())
        
        return b.getvalue()
