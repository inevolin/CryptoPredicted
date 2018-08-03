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


class DocumentAttributeAudio(Object):
    """Attributes:
        ID: ``0x9852f9c6``

    Args:
        duration: ``int`` ``32-bit``
        voice (optional): ``bool``
        title (optional): ``str``
        performer (optional): ``str``
        waveform (optional): ``bytes``
    """

    ID = 0x9852f9c6

    def __init__(self, duration: int, voice: bool = None, title: str = None, performer: str = None, waveform: bytes = None):
        self.voice = voice  # flags.10?true
        self.duration = duration  # int
        self.title = title  # flags.0?string
        self.performer = performer  # flags.1?string
        self.waveform = waveform  # flags.2?bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "DocumentAttributeAudio":
        flags = Int.read(b)
        
        voice = True if flags & (1 << 10) else False
        duration = Int.read(b)
        
        title = String.read(b) if flags & (1 << 0) else None
        performer = String.read(b) if flags & (1 << 1) else None
        waveform = Bytes.read(b) if flags & (1 << 2) else None
        return DocumentAttributeAudio(duration, voice, title, performer, waveform)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 10) if self.voice is not None else 0
        flags |= (1 << 0) if self.title is not None else 0
        flags |= (1 << 1) if self.performer is not None else 0
        flags |= (1 << 2) if self.waveform is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.duration))
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.performer is not None:
            b.write(String(self.performer))
        
        if self.waveform is not None:
            b.write(Bytes(self.waveform))
        
        return b.getvalue()
