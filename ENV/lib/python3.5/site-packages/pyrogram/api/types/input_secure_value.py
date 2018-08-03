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


class InputSecureValue(Object):
    """Attributes:
        ID: ``0x067872e8``

    Args:
        type: Either :obj:`SecureValueTypePersonalDetails <pyrogram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <pyrogram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <pyrogram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <pyrogram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <pyrogram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <pyrogram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <pyrogram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <pyrogram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <pyrogram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <pyrogram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <pyrogram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <pyrogram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <pyrogram.api.types.SecureValueTypeEmail>`
        data (optional): :obj:`SecureData <pyrogram.api.types.SecureData>`
        front_side (optional): Either :obj:`InputSecureFileUploaded <pyrogram.api.types.InputSecureFileUploaded>` or :obj:`InputSecureFile <pyrogram.api.types.InputSecureFile>`
        reverse_side (optional): Either :obj:`InputSecureFileUploaded <pyrogram.api.types.InputSecureFileUploaded>` or :obj:`InputSecureFile <pyrogram.api.types.InputSecureFile>`
        selfie (optional): Either :obj:`InputSecureFileUploaded <pyrogram.api.types.InputSecureFileUploaded>` or :obj:`InputSecureFile <pyrogram.api.types.InputSecureFile>`
        files (optional): List of either :obj:`InputSecureFileUploaded <pyrogram.api.types.InputSecureFileUploaded>` or :obj:`InputSecureFile <pyrogram.api.types.InputSecureFile>`
        plain_data (optional): Either :obj:`SecurePlainPhone <pyrogram.api.types.SecurePlainPhone>` or :obj:`SecurePlainEmail <pyrogram.api.types.SecurePlainEmail>`
    """

    ID = 0x067872e8

    def __init__(self, type, data=None, front_side=None, reverse_side=None, selfie=None, files: list = None, plain_data=None):
        self.type = type  # SecureValueType
        self.data = data  # flags.0?SecureData
        self.front_side = front_side  # flags.1?InputSecureFile
        self.reverse_side = reverse_side  # flags.2?InputSecureFile
        self.selfie = selfie  # flags.3?InputSecureFile
        self.files = files  # flags.4?Vector<InputSecureFile>
        self.plain_data = plain_data  # flags.5?SecurePlainData

    @staticmethod
    def read(b: BytesIO, *args) -> "InputSecureValue":
        flags = Int.read(b)
        
        type = Object.read(b)
        
        data = Object.read(b) if flags & (1 << 0) else None
        
        front_side = Object.read(b) if flags & (1 << 1) else None
        
        reverse_side = Object.read(b) if flags & (1 << 2) else None
        
        selfie = Object.read(b) if flags & (1 << 3) else None
        
        files = Object.read(b) if flags & (1 << 4) else []
        
        plain_data = Object.read(b) if flags & (1 << 5) else None
        
        return InputSecureValue(type, data, front_side, reverse_side, selfie, files, plain_data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.data is not None else 0
        flags |= (1 << 1) if self.front_side is not None else 0
        flags |= (1 << 2) if self.reverse_side is not None else 0
        flags |= (1 << 3) if self.selfie is not None else 0
        flags |= (1 << 4) if self.files is not None else 0
        flags |= (1 << 5) if self.plain_data is not None else 0
        b.write(Int(flags))
        
        b.write(self.type.write())
        
        if self.data is not None:
            b.write(self.data.write())
        
        if self.front_side is not None:
            b.write(self.front_side.write())
        
        if self.reverse_side is not None:
            b.write(self.reverse_side.write())
        
        if self.selfie is not None:
            b.write(self.selfie.write())
        
        if self.files is not None:
            b.write(Vector(self.files))
        
        if self.plain_data is not None:
            b.write(self.plain_data.write())
        
        return b.getvalue()
