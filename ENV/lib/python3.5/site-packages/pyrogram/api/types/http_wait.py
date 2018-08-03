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


class HttpWait(Object):
    """Attributes:
        ID: ``0x9299359f``

    Args:
        max_delay: ``int`` ``32-bit``
        wait_after: ``int`` ``32-bit``
        max_wait: ``int`` ``32-bit``
    """

    ID = 0x9299359f

    def __init__(self, max_delay: int, wait_after: int, max_wait: int):
        self.max_delay = max_delay  # int
        self.wait_after = wait_after  # int
        self.max_wait = max_wait  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "HttpWait":
        # No flags
        
        max_delay = Int.read(b)
        
        wait_after = Int.read(b)
        
        max_wait = Int.read(b)
        
        return HttpWait(max_delay, wait_after, max_wait)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.max_delay))
        
        b.write(Int(self.wait_after))
        
        b.write(Int(self.max_wait))
        
        return b.getvalue()
