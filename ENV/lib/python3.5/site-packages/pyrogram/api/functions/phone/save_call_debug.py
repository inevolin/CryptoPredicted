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


class SaveCallDebug(Object):
    """Attributes:
        ID: ``0x277add7e``

    Args:
        peer: :obj:`InputPhoneCall <pyrogram.api.types.InputPhoneCall>`
        debug: :obj:`DataJSON <pyrogram.api.types.DataJSON>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x277add7e

    def __init__(self, peer, debug):
        self.peer = peer  # InputPhoneCall
        self.debug = debug  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args) -> "SaveCallDebug":
        # No flags
        
        peer = Object.read(b)
        
        debug = Object.read(b)
        
        return SaveCallDebug(peer, debug)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.debug.write())
        
        return b.getvalue()
