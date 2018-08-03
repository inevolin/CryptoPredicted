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


class UpdateProfilePhoto(Object):
    """Attributes:
        ID: ``0xf0bb5152``

    Args:
        id: Either :obj:`InputPhotoEmpty <pyrogram.api.types.InputPhotoEmpty>` or :obj:`InputPhoto <pyrogram.api.types.InputPhoto>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`UserProfilePhotoEmpty <pyrogram.api.types.UserProfilePhotoEmpty>` or :obj:`UserProfilePhoto <pyrogram.api.types.UserProfilePhoto>`
    """

    ID = 0xf0bb5152

    def __init__(self, id):
        self.id = id  # InputPhoto

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateProfilePhoto":
        # No flags
        
        id = Object.read(b)
        
        return UpdateProfilePhoto(id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
