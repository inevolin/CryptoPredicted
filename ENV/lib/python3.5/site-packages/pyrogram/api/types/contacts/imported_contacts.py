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


class ImportedContacts(Object):
    """Attributes:
        ID: ``0x77d01c3b``

    Args:
        imported: List of :obj:`ImportedContact <pyrogram.api.types.ImportedContact>`
        popular_invites: List of :obj:`PopularContact <pyrogram.api.types.PopularContact>`
        retry_contacts: List of ``int`` ``64-bit``
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`contacts.ImportContacts <pyrogram.api.functions.contacts.ImportContacts>`.
    """

    ID = 0x77d01c3b

    def __init__(self, imported: list, popular_invites: list, retry_contacts: list, users: list):
        self.imported = imported  # Vector<ImportedContact>
        self.popular_invites = popular_invites  # Vector<PopularContact>
        self.retry_contacts = retry_contacts  # Vector<long>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ImportedContacts":
        # No flags
        
        imported = Object.read(b)
        
        popular_invites = Object.read(b)
        
        retry_contacts = Object.read(b, Long)
        
        users = Object.read(b)
        
        return ImportedContacts(imported, popular_invites, retry_contacts, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.imported))
        
        b.write(Vector(self.popular_invites))
        
        b.write(Vector(self.retry_contacts, Long))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
