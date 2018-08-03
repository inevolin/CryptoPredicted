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


class AuthorizationForm(Object):
    """Attributes:
        ID: ``0xcb976d53``

    Args:
        required_types: List of either :obj:`SecureValueTypePersonalDetails <pyrogram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <pyrogram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <pyrogram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <pyrogram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <pyrogram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <pyrogram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <pyrogram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <pyrogram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <pyrogram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <pyrogram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <pyrogram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <pyrogram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <pyrogram.api.types.SecureValueTypeEmail>`
        values: List of :obj:`SecureValue <pyrogram.api.types.SecureValue>`
        errors: List of either :obj:`SecureValueErrorData <pyrogram.api.types.SecureValueErrorData>`, :obj:`SecureValueErrorFrontSide <pyrogram.api.types.SecureValueErrorFrontSide>`, :obj:`SecureValueErrorReverseSide <pyrogram.api.types.SecureValueErrorReverseSide>`, :obj:`SecureValueErrorSelfie <pyrogram.api.types.SecureValueErrorSelfie>`, :obj:`SecureValueErrorFile <pyrogram.api.types.SecureValueErrorFile>` or :obj:`SecureValueErrorFiles <pyrogram.api.types.SecureValueErrorFiles>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        selfie_required (optional): ``bool``
        privacy_policy_url (optional): ``str``

    See Also:
        This object can be returned by :obj:`account.GetAuthorizationForm <pyrogram.api.functions.account.GetAuthorizationForm>`.
    """

    ID = 0xcb976d53

    def __init__(self, required_types: list, values: list, errors: list, users: list, selfie_required: bool = None, privacy_policy_url: str = None):
        self.selfie_required = selfie_required  # flags.1?true
        self.required_types = required_types  # Vector<SecureValueType>
        self.values = values  # Vector<SecureValue>
        self.errors = errors  # Vector<SecureValueError>
        self.users = users  # Vector<User>
        self.privacy_policy_url = privacy_policy_url  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args) -> "AuthorizationForm":
        flags = Int.read(b)
        
        selfie_required = True if flags & (1 << 1) else False
        required_types = Object.read(b)
        
        values = Object.read(b)
        
        errors = Object.read(b)
        
        users = Object.read(b)
        
        privacy_policy_url = String.read(b) if flags & (1 << 0) else None
        return AuthorizationForm(required_types, values, errors, users, selfie_required, privacy_policy_url)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.selfie_required is not None else 0
        flags |= (1 << 0) if self.privacy_policy_url is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.required_types))
        
        b.write(Vector(self.values))
        
        b.write(Vector(self.errors))
        
        b.write(Vector(self.users))
        
        if self.privacy_policy_url is not None:
            b.write(String(self.privacy_policy_url))
        
        return b.getvalue()
