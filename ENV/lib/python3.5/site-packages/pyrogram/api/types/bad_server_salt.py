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


class BadServerSalt(Object):
    """Attributes:
        ID: ``0xedab447b``

    Args:
        bad_msg_id: ``int`` ``64-bit``
        bad_msg_seqno: ``int`` ``32-bit``
        error_code: ``int`` ``32-bit``
        new_server_salt: ``int`` ``64-bit``
    """

    ID = 0xedab447b

    def __init__(self, bad_msg_id: int, bad_msg_seqno: int, error_code: int, new_server_salt: int):
        self.bad_msg_id = bad_msg_id  # long
        self.bad_msg_seqno = bad_msg_seqno  # int
        self.error_code = error_code  # int
        self.new_server_salt = new_server_salt  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "BadServerSalt":
        # No flags
        
        bad_msg_id = Long.read(b)
        
        bad_msg_seqno = Int.read(b)
        
        error_code = Int.read(b)
        
        new_server_salt = Long.read(b)
        
        return BadServerSalt(bad_msg_id, bad_msg_seqno, error_code, new_server_salt)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.bad_msg_id))
        
        b.write(Int(self.bad_msg_seqno))
        
        b.write(Int(self.error_code))
        
        b.write(Long(self.new_server_salt))
        
        return b.getvalue()
