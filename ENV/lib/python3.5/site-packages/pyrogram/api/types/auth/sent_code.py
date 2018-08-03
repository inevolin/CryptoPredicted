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


class SentCode(Object):
    """Attributes:
        ID: ``0x38faab5f``

    Args:
        type: Either :obj:`auth.SentCodeTypeApp <pyrogram.api.types.auth.SentCodeTypeApp>`, :obj:`auth.SentCodeTypeSms <pyrogram.api.types.auth.SentCodeTypeSms>`, :obj:`auth.SentCodeTypeCall <pyrogram.api.types.auth.SentCodeTypeCall>` or :obj:`auth.SentCodeTypeFlashCall <pyrogram.api.types.auth.SentCodeTypeFlashCall>`
        phone_code_hash: ``str``
        phone_registered (optional): ``bool``
        next_type (optional): Either :obj:`auth.CodeTypeSms <pyrogram.api.types.auth.CodeTypeSms>`, :obj:`auth.CodeTypeCall <pyrogram.api.types.auth.CodeTypeCall>` or :obj:`auth.CodeTypeFlashCall <pyrogram.api.types.auth.CodeTypeFlashCall>`
        timeout (optional): ``int`` ``32-bit``
        terms_of_service (optional): :obj:`help.TermsOfService <pyrogram.api.types.help.TermsOfService>`

    See Also:
        This object can be returned by :obj:`auth.SendCode <pyrogram.api.functions.auth.SendCode>`, :obj:`auth.ResendCode <pyrogram.api.functions.auth.ResendCode>`, :obj:`account.SendChangePhoneCode <pyrogram.api.functions.account.SendChangePhoneCode>`, :obj:`account.SendConfirmPhoneCode <pyrogram.api.functions.account.SendConfirmPhoneCode>` and :obj:`account.SendVerifyPhoneCode <pyrogram.api.functions.account.SendVerifyPhoneCode>`.
    """

    ID = 0x38faab5f

    def __init__(self, type, phone_code_hash: str, phone_registered: bool = None, next_type=None, timeout: int = None, terms_of_service=None):
        self.phone_registered = phone_registered  # flags.0?true
        self.type = type  # auth.SentCodeType
        self.phone_code_hash = phone_code_hash  # string
        self.next_type = next_type  # flags.1?auth.CodeType
        self.timeout = timeout  # flags.2?int
        self.terms_of_service = terms_of_service  # flags.3?help.TermsOfService

    @staticmethod
    def read(b: BytesIO, *args) -> "SentCode":
        flags = Int.read(b)
        
        phone_registered = True if flags & (1 << 0) else False
        type = Object.read(b)
        
        phone_code_hash = String.read(b)
        
        next_type = Object.read(b) if flags & (1 << 1) else None
        
        timeout = Int.read(b) if flags & (1 << 2) else None
        terms_of_service = Object.read(b) if flags & (1 << 3) else None
        
        return SentCode(type, phone_code_hash, phone_registered, next_type, timeout, terms_of_service)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.phone_registered is not None else 0
        flags |= (1 << 1) if self.next_type is not None else 0
        flags |= (1 << 2) if self.timeout is not None else 0
        flags |= (1 << 3) if self.terms_of_service is not None else 0
        b.write(Int(flags))
        
        b.write(self.type.write())
        
        b.write(String(self.phone_code_hash))
        
        if self.next_type is not None:
            b.write(self.next_type.write())
        
        if self.timeout is not None:
            b.write(Int(self.timeout))
        
        if self.terms_of_service is not None:
            b.write(self.terms_of_service.write())
        
        return b.getvalue()
