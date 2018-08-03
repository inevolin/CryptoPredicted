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


class PrivacyRules(Object):
    """Attributes:
        ID: ``0x554abb6f``

    Args:
        rules: List of either :obj:`PrivacyValueAllowContacts <pyrogram.api.types.PrivacyValueAllowContacts>`, :obj:`PrivacyValueAllowAll <pyrogram.api.types.PrivacyValueAllowAll>`, :obj:`PrivacyValueAllowUsers <pyrogram.api.types.PrivacyValueAllowUsers>`, :obj:`PrivacyValueDisallowContacts <pyrogram.api.types.PrivacyValueDisallowContacts>`, :obj:`PrivacyValueDisallowAll <pyrogram.api.types.PrivacyValueDisallowAll>` or :obj:`PrivacyValueDisallowUsers <pyrogram.api.types.PrivacyValueDisallowUsers>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`account.GetPrivacy <pyrogram.api.functions.account.GetPrivacy>` and :obj:`account.SetPrivacy <pyrogram.api.functions.account.SetPrivacy>`.
    """

    ID = 0x554abb6f

    def __init__(self, rules: list, users: list):
        self.rules = rules  # Vector<PrivacyRule>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "PrivacyRules":
        # No flags
        
        rules = Object.read(b)
        
        users = Object.read(b)
        
        return PrivacyRules(rules, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.rules))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
