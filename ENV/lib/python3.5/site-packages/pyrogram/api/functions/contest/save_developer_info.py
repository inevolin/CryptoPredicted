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


class SaveDeveloperInfo(Object):
    """Attributes:
        ID: ``0x9a5f6e95``

    Args:
        vk_id: ``int`` ``32-bit``
        name: ``str``
        phone_number: ``str``
        age: ``int`` ``32-bit``
        city: ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x9a5f6e95

    def __init__(self, vk_id: int, name: str, phone_number: str, age: int, city: str):
        self.vk_id = vk_id  # int
        self.name = name  # string
        self.phone_number = phone_number  # string
        self.age = age  # int
        self.city = city  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "SaveDeveloperInfo":
        # No flags
        
        vk_id = Int.read(b)
        
        name = String.read(b)
        
        phone_number = String.read(b)
        
        age = Int.read(b)
        
        city = String.read(b)
        
        return SaveDeveloperInfo(vk_id, name, phone_number, age, city)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.vk_id))
        
        b.write(String(self.name))
        
        b.write(String(self.phone_number))
        
        b.write(Int(self.age))
        
        b.write(String(self.city))
        
        return b.getvalue()
