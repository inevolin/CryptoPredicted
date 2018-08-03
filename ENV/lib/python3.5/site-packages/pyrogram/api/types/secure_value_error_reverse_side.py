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


class SecureValueErrorReverseSide(Object):
    """Attributes:
        ID: ``0x868a2aa5``

    Args:
        type: Either :obj:`SecureValueTypePersonalDetails <pyrogram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <pyrogram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <pyrogram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <pyrogram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <pyrogram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <pyrogram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <pyrogram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <pyrogram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <pyrogram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <pyrogram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <pyrogram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <pyrogram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <pyrogram.api.types.SecureValueTypeEmail>`
        file_hash: ``bytes``
        text: ``str``
    """

    ID = 0x868a2aa5

    def __init__(self, type, file_hash: bytes, text: str):
        self.type = type  # SecureValueType
        self.file_hash = file_hash  # bytes
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureValueErrorReverseSide":
        # No flags
        
        type = Object.read(b)
        
        file_hash = Bytes.read(b)
        
        text = String.read(b)
        
        return SecureValueErrorReverseSide(type, file_hash, text)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Bytes(self.file_hash))
        
        b.write(String(self.text))
        
        return b.getvalue()
