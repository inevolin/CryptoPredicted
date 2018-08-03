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
        ID: ``0x7bf2e6f6``

    Args:
        hash: ``int`` ``64-bit``
        flags: ``int`` ``32-bit``
        device_model: ``str``
        platform: ``str``
        system_version: ``str``
        api_id: ``int`` ``32-bit``
        app_name: ``str``
        app_version: ``str``
        date_created: ``int`` ``32-bit``
        date_active: ``int`` ``32-bit``
        ip: ``str``
        country: ``str``
        region: ``str``
    """

    ID = 0x7bf2e6f6

    def __init__(self, hash: int, flags: int, device_model: str, platform: str, system_version: str, api_id: int, app_name: str, app_version: str, date_created: int, date_active: int, ip: str, country: str, region: str):
        self.hash = hash  # long
        self.flags = flags  # int
        self.device_model = device_model  # string
        self.platform = platform  # string
        self.system_version = system_version  # string
        self.api_id = api_id  # int
        self.app_name = app_name  # string
        self.app_version = app_version  # string
        self.date_created = date_created  # int
        self.date_active = date_active  # int
        self.ip = ip  # string
        self.country = country  # string
        self.region = region  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "Authorization":
        # No flags
        
        hash = Long.read(b)
        
        flags = Int.read(b)
        
        device_model = String.read(b)
        
        platform = String.read(b)
        
        system_version = String.read(b)
        
        api_id = Int.read(b)
        
        app_name = String.read(b)
        
        app_version = String.read(b)
        
        date_created = Int.read(b)
        
        date_active = Int.read(b)
        
        ip = String.read(b)
        
        country = String.read(b)
        
        region = String.read(b)
        
        return Authorization(hash, flags, device_model, platform, system_version, api_id, app_name, app_version, date_created, date_active, ip, country, region)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Int(self.flags))
        
        b.write(String(self.device_model))
        
        b.write(String(self.platform))
        
        b.write(String(self.system_version))
        
        b.write(Int(self.api_id))
        
        b.write(String(self.app_name))
        
        b.write(String(self.app_version))
        
        b.write(Int(self.date_created))
        
        b.write(Int(self.date_active))
        
        b.write(String(self.ip))
        
        b.write(String(self.country))
        
        b.write(String(self.region))
        
        return b.getvalue()
