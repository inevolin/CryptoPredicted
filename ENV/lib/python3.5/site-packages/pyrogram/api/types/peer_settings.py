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


class PeerSettings(Object):
    """Attributes:
        ID: ``0x818426cd``

    Args:
        report_spam (optional): ``bool``

    See Also:
        This object can be returned by :obj:`messages.GetPeerSettings <pyrogram.api.functions.messages.GetPeerSettings>`.
    """

    ID = 0x818426cd

    def __init__(self, report_spam: bool = None):
        self.report_spam = report_spam  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args) -> "PeerSettings":
        flags = Int.read(b)
        
        report_spam = True if flags & (1 << 0) else False
        return PeerSettings(report_spam)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.report_spam is not None else 0
        b.write(Int(flags))
        
        return b.getvalue()
