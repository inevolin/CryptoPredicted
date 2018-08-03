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


class UserProfilePhoto(Object):
    """Attributes:
        ID: ``0xd559d8c8``

    Args:
        photo_id: ``int`` ``64-bit``
        photo_small: Either :obj:`FileLocationUnavailable <pyrogram.api.types.FileLocationUnavailable>` or :obj:`FileLocation <pyrogram.api.types.FileLocation>`
        photo_big: Either :obj:`FileLocationUnavailable <pyrogram.api.types.FileLocationUnavailable>` or :obj:`FileLocation <pyrogram.api.types.FileLocation>`

    See Also:
        This object can be returned by :obj:`photos.UpdateProfilePhoto <pyrogram.api.functions.photos.UpdateProfilePhoto>`.
    """

    ID = 0xd559d8c8

    def __init__(self, photo_id: int, photo_small, photo_big):
        self.photo_id = photo_id  # long
        self.photo_small = photo_small  # FileLocation
        self.photo_big = photo_big  # FileLocation

    @staticmethod
    def read(b: BytesIO, *args) -> "UserProfilePhoto":
        # No flags
        
        photo_id = Long.read(b)
        
        photo_small = Object.read(b)
        
        photo_big = Object.read(b)
        
        return UserProfilePhoto(photo_id, photo_small, photo_big)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.photo_id))
        
        b.write(self.photo_small.write())
        
        b.write(self.photo_big.write())
        
        return b.getvalue()
