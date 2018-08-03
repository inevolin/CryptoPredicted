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


class CdnFileReuploadNeeded(Object):
    """Attributes:
        ID: ``0xeea8e46e``

    Args:
        request_token: ``bytes``

    See Also:
        This object can be returned by :obj:`upload.GetCdnFile <pyrogram.api.functions.upload.GetCdnFile>`.
    """

    ID = 0xeea8e46e

    def __init__(self, request_token: bytes):
        self.request_token = request_token  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "CdnFileReuploadNeeded":
        # No flags
        
        request_token = Bytes.read(b)
        
        return CdnFileReuploadNeeded(request_token)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.request_token))
        
        return b.getvalue()
