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


class SetSecureValueErrors(Object):
    """Attributes:
        ID: ``0x90c894b5``

    Args:
        id: Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`
        errors: List of either :obj:`SecureValueErrorData <pyrogram.api.types.SecureValueErrorData>`, :obj:`SecureValueErrorFrontSide <pyrogram.api.types.SecureValueErrorFrontSide>`, :obj:`SecureValueErrorReverseSide <pyrogram.api.types.SecureValueErrorReverseSide>`, :obj:`SecureValueErrorSelfie <pyrogram.api.types.SecureValueErrorSelfie>`, :obj:`SecureValueErrorFile <pyrogram.api.types.SecureValueErrorFile>` or :obj:`SecureValueErrorFiles <pyrogram.api.types.SecureValueErrorFiles>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x90c894b5

    def __init__(self, id, errors: list):
        self.id = id  # InputUser
        self.errors = errors  # Vector<SecureValueError>

    @staticmethod
    def read(b: BytesIO, *args) -> "SetSecureValueErrors":
        # No flags
        
        id = Object.read(b)
        
        errors = Object.read(b)
        
        return SetSecureValueErrors(id, errors)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        b.write(Vector(self.errors))
        
        return b.getvalue()
