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


class SetPrivacy(Object):
    """Attributes:
        ID: ``0xc9f81ce8``

    Args:
        key: Either :obj:`InputPrivacyKeyStatusTimestamp <pyrogram.api.types.InputPrivacyKeyStatusTimestamp>`, :obj:`InputPrivacyKeyChatInvite <pyrogram.api.types.InputPrivacyKeyChatInvite>` or :obj:`InputPrivacyKeyPhoneCall <pyrogram.api.types.InputPrivacyKeyPhoneCall>`
        rules: List of either :obj:`InputPrivacyValueAllowContacts <pyrogram.api.types.InputPrivacyValueAllowContacts>`, :obj:`InputPrivacyValueAllowAll <pyrogram.api.types.InputPrivacyValueAllowAll>`, :obj:`InputPrivacyValueAllowUsers <pyrogram.api.types.InputPrivacyValueAllowUsers>`, :obj:`InputPrivacyValueDisallowContacts <pyrogram.api.types.InputPrivacyValueDisallowContacts>`, :obj:`InputPrivacyValueDisallowAll <pyrogram.api.types.InputPrivacyValueDisallowAll>` or :obj:`InputPrivacyValueDisallowUsers <pyrogram.api.types.InputPrivacyValueDisallowUsers>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`account.PrivacyRules <pyrogram.api.types.account.PrivacyRules>`
    """

    ID = 0xc9f81ce8

    def __init__(self, key, rules: list):
        self.key = key  # InputPrivacyKey
        self.rules = rules  # Vector<InputPrivacyRule>

    @staticmethod
    def read(b: BytesIO, *args) -> "SetPrivacy":
        # No flags
        
        key = Object.read(b)
        
        rules = Object.read(b)
        
        return SetPrivacy(key, rules)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        b.write(Vector(self.rules))
        
        return b.getvalue()
