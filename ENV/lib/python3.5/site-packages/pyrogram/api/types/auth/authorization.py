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


class Authorization(Object):
    """Attributes:
        ID: ``0xcd050916``

    Args:
        user: Either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        tmp_sessions (optional): ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`auth.SignUp <pyrogram.api.functions.auth.SignUp>`, :obj:`auth.SignIn <pyrogram.api.functions.auth.SignIn>`, :obj:`auth.ImportAuthorization <pyrogram.api.functions.auth.ImportAuthorization>`, :obj:`auth.ImportBotAuthorization <pyrogram.api.functions.auth.ImportBotAuthorization>`, :obj:`auth.CheckPassword <pyrogram.api.functions.auth.CheckPassword>` and :obj:`auth.RecoverPassword <pyrogram.api.functions.auth.RecoverPassword>`.
    """

    ID = 0xcd050916

    def __init__(self, user, tmp_sessions: int = None):
        self.tmp_sessions = tmp_sessions  # flags.0?int
        self.user = user  # User

    @staticmethod
    def read(b: BytesIO, *args) -> "Authorization":
        flags = Int.read(b)
        
        tmp_sessions = Int.read(b) if flags & (1 << 0) else None
        user = Object.read(b)
        
        return Authorization(user, tmp_sessions)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.tmp_sessions is not None else 0
        b.write(Int(flags))
        
        if self.tmp_sessions is not None:
            b.write(Int(self.tmp_sessions))
        
        b.write(self.user.write())
        
        return b.getvalue()
