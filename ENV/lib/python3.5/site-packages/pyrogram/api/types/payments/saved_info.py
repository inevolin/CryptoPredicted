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


class SavedInfo(Object):
    """Attributes:
        ID: ``0xfb8fe43c``

    Args:
        has_saved_credentials (optional): ``bool``
        saved_info (optional): :obj:`PaymentRequestedInfo <pyrogram.api.types.PaymentRequestedInfo>`

    See Also:
        This object can be returned by :obj:`payments.GetSavedInfo <pyrogram.api.functions.payments.GetSavedInfo>`.
    """

    ID = 0xfb8fe43c

    def __init__(self, has_saved_credentials: bool = None, saved_info=None):
        self.has_saved_credentials = has_saved_credentials  # flags.1?true
        self.saved_info = saved_info  # flags.0?PaymentRequestedInfo

    @staticmethod
    def read(b: BytesIO, *args) -> "SavedInfo":
        flags = Int.read(b)
        
        has_saved_credentials = True if flags & (1 << 1) else False
        saved_info = Object.read(b) if flags & (1 << 0) else None
        
        return SavedInfo(has_saved_credentials, saved_info)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.has_saved_credentials is not None else 0
        flags |= (1 << 0) if self.saved_info is not None else 0
        b.write(Int(flags))
        
        if self.saved_info is not None:
            b.write(self.saved_info.write())
        
        return b.getvalue()
