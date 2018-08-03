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


class UploadEncryptedFile(Object):
    """Attributes:
        ID: ``0x5057c497``

    Args:
        peer: :obj:`InputEncryptedChat <pyrogram.api.types.InputEncryptedChat>`
        file: Either :obj:`InputEncryptedFileEmpty <pyrogram.api.types.InputEncryptedFileEmpty>`, :obj:`InputEncryptedFileUploaded <pyrogram.api.types.InputEncryptedFileUploaded>`, :obj:`InputEncryptedFile <pyrogram.api.types.InputEncryptedFile>` or :obj:`InputEncryptedFileBigUploaded <pyrogram.api.types.InputEncryptedFileBigUploaded>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`EncryptedFileEmpty <pyrogram.api.types.EncryptedFileEmpty>` or :obj:`EncryptedFile <pyrogram.api.types.EncryptedFile>`
    """

    ID = 0x5057c497

    def __init__(self, peer, file):
        self.peer = peer  # InputEncryptedChat
        self.file = file  # InputEncryptedFile

    @staticmethod
    def read(b: BytesIO, *args) -> "UploadEncryptedFile":
        # No flags
        
        peer = Object.read(b)
        
        file = Object.read(b)
        
        return UploadEncryptedFile(peer, file)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.file.write())
        
        return b.getvalue()
