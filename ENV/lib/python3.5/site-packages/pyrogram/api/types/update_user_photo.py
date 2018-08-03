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


class UpdateUserPhoto(Object):
    """Attributes:
        ID: ``0x95313b0c``

    Args:
        user_id: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        photo: Either :obj:`UserProfilePhotoEmpty <pyrogram.api.types.UserProfilePhotoEmpty>` or :obj:`UserProfilePhoto <pyrogram.api.types.UserProfilePhoto>`
        previous: ``bool``
    """

    ID = 0x95313b0c

    def __init__(self, user_id: int, date: int, photo, previous: bool):
        self.user_id = user_id  # int
        self.date = date  # int
        self.photo = photo  # UserProfilePhoto
        self.previous = previous  # Bool

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateUserPhoto":
        # No flags
        
        user_id = Int.read(b)
        
        date = Int.read(b)
        
        photo = Object.read(b)
        
        previous = Bool.read(b)
        
        return UpdateUserPhoto(user_id, date, photo, previous)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.date))
        
        b.write(self.photo.write())
        
        b.write(Bool(self.previous))
        
        return b.getvalue()
