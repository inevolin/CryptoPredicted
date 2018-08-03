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


class TermsOfServiceUpdate(Object):
    """Attributes:
        ID: ``0x28ecf961``

    Args:
        expires: ``int`` ``32-bit``
        terms_of_service: :obj:`help.TermsOfService <pyrogram.api.types.help.TermsOfService>`

    See Also:
        This object can be returned by :obj:`help.GetTermsOfServiceUpdate <pyrogram.api.functions.help.GetTermsOfServiceUpdate>`.
    """

    ID = 0x28ecf961

    def __init__(self, expires: int, terms_of_service):
        self.expires = expires  # int
        self.terms_of_service = terms_of_service  # help.TermsOfService

    @staticmethod
    def read(b: BytesIO, *args) -> "TermsOfServiceUpdate":
        # No flags
        
        expires = Int.read(b)
        
        terms_of_service = Object.read(b)
        
        return TermsOfServiceUpdate(expires, terms_of_service)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.expires))
        
        b.write(self.terms_of_service.write())
        
        return b.getvalue()
