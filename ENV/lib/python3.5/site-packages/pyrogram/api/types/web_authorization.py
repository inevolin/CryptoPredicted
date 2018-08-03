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


class WebAuthorization(Object):
    """Attributes:
        ID: ``0xcac943f2``

    Args:
        hash: ``int`` ``64-bit``
        bot_id: ``int`` ``32-bit``
        domain: ``str``
        browser: ``str``
        platform: ``str``
        date_created: ``int`` ``32-bit``
        date_active: ``int`` ``32-bit``
        ip: ``str``
        region: ``str``
    """

    ID = 0xcac943f2

    def __init__(self, hash: int, bot_id: int, domain: str, browser: str, platform: str, date_created: int, date_active: int, ip: str, region: str):
        self.hash = hash  # long
        self.bot_id = bot_id  # int
        self.domain = domain  # string
        self.browser = browser  # string
        self.platform = platform  # string
        self.date_created = date_created  # int
        self.date_active = date_active  # int
        self.ip = ip  # string
        self.region = region  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "WebAuthorization":
        # No flags
        
        hash = Long.read(b)
        
        bot_id = Int.read(b)
        
        domain = String.read(b)
        
        browser = String.read(b)
        
        platform = String.read(b)
        
        date_created = Int.read(b)
        
        date_active = Int.read(b)
        
        ip = String.read(b)
        
        region = String.read(b)
        
        return WebAuthorization(hash, bot_id, domain, browser, platform, date_created, date_active, ip, region)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Int(self.bot_id))
        
        b.write(String(self.domain))
        
        b.write(String(self.browser))
        
        b.write(String(self.platform))
        
        b.write(Int(self.date_created))
        
        b.write(Int(self.date_active))
        
        b.write(String(self.ip))
        
        b.write(String(self.region))
        
        return b.getvalue()
