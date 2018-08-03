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


class InitConnection(Object):
    """Attributes:
        ID: ``0x785188b8``

    Args:
        api_id: ``int`` ``32-bit``
        device_model: ``str``
        system_version: ``str``
        app_version: ``str``
        system_lang_code: ``str``
        lang_pack: ``str``
        lang_code: ``str``
        query: Any method from :obj:`pyrogram.api.functions`
        proxy (optional): :obj:`InputClientProxy <pyrogram.api.types.InputClientProxy>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Any object from :obj:`pyrogram.api.types`
    """

    ID = 0x785188b8

    def __init__(self, api_id: int, device_model: str, system_version: str, app_version: str, system_lang_code: str, lang_pack: str, lang_code: str, query, proxy=None):
        self.api_id = api_id  # int
        self.device_model = device_model  # string
        self.system_version = system_version  # string
        self.app_version = app_version  # string
        self.system_lang_code = system_lang_code  # string
        self.lang_pack = lang_pack  # string
        self.lang_code = lang_code  # string
        self.proxy = proxy  # flags.0?InputClientProxy
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InitConnection":
        flags = Int.read(b)
        
        api_id = Int.read(b)
        
        device_model = String.read(b)
        
        system_version = String.read(b)
        
        app_version = String.read(b)
        
        system_lang_code = String.read(b)
        
        lang_pack = String.read(b)
        
        lang_code = String.read(b)
        
        proxy = Object.read(b) if flags & (1 << 0) else None
        
        query = Object.read(b)
        
        return InitConnection(api_id, device_model, system_version, app_version, system_lang_code, lang_pack, lang_code, query, proxy)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.proxy is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.api_id))
        
        b.write(String(self.device_model))
        
        b.write(String(self.system_version))
        
        b.write(String(self.app_version))
        
        b.write(String(self.system_lang_code))
        
        b.write(String(self.lang_pack))
        
        b.write(String(self.lang_code))
        
        if self.proxy is not None:
            b.write(self.proxy.write())
        
        b.write(self.query.write())
        
        return b.getvalue()
