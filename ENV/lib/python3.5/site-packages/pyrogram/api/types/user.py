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


class User(Object):
    """Attributes:
        ID: ``0x2e13f4c3``

    Args:
        id: ``int`` ``32-bit``
        is_self (optional): ``bool``
        contact (optional): ``bool``
        mutual_contact (optional): ``bool``
        deleted (optional): ``bool``
        bot (optional): ``bool``
        bot_chat_history (optional): ``bool``
        bot_nochats (optional): ``bool``
        verified (optional): ``bool``
        restricted (optional): ``bool``
        min (optional): ``bool``
        bot_inline_geo (optional): ``bool``
        access_hash (optional): ``int`` ``64-bit``
        first_name (optional): ``str``
        last_name (optional): ``str``
        username (optional): ``str``
        phone (optional): ``str``
        photo (optional): Either :obj:`UserProfilePhotoEmpty <pyrogram.api.types.UserProfilePhotoEmpty>` or :obj:`UserProfilePhoto <pyrogram.api.types.UserProfilePhoto>`
        status (optional): Either :obj:`UserStatusEmpty <pyrogram.api.types.UserStatusEmpty>`, :obj:`UserStatusOnline <pyrogram.api.types.UserStatusOnline>`, :obj:`UserStatusOffline <pyrogram.api.types.UserStatusOffline>`, :obj:`UserStatusRecently <pyrogram.api.types.UserStatusRecently>`, :obj:`UserStatusLastWeek <pyrogram.api.types.UserStatusLastWeek>` or :obj:`UserStatusLastMonth <pyrogram.api.types.UserStatusLastMonth>`
        bot_info_version (optional): ``int`` ``32-bit``
        restriction_reason (optional): ``str``
        bot_inline_placeholder (optional): ``str``
        lang_code (optional): ``str``

    See Also:
        This object can be returned by :obj:`account.UpdateProfile <pyrogram.api.functions.account.UpdateProfile>`, :obj:`account.UpdateUsername <pyrogram.api.functions.account.UpdateUsername>`, :obj:`account.ChangePhone <pyrogram.api.functions.account.ChangePhone>`, :obj:`users.GetUsers <pyrogram.api.functions.users.GetUsers>` and :obj:`contacts.ImportCard <pyrogram.api.functions.contacts.ImportCard>`.
    """

    ID = 0x2e13f4c3

    def __init__(self, id: int, is_self: bool = None, contact: bool = None, mutual_contact: bool = None, deleted: bool = None, bot: bool = None, bot_chat_history: bool = None, bot_nochats: bool = None, verified: bool = None, restricted: bool = None, min: bool = None, bot_inline_geo: bool = None, access_hash: int = None, first_name: str = None, last_name: str = None, username: str = None, phone: str = None, photo=None, status=None, bot_info_version: int = None, restriction_reason: str = None, bot_inline_placeholder: str = None, lang_code: str = None):
        self.is_self = is_self  # flags.10?true
        self.contact = contact  # flags.11?true
        self.mutual_contact = mutual_contact  # flags.12?true
        self.deleted = deleted  # flags.13?true
        self.bot = bot  # flags.14?true
        self.bot_chat_history = bot_chat_history  # flags.15?true
        self.bot_nochats = bot_nochats  # flags.16?true
        self.verified = verified  # flags.17?true
        self.restricted = restricted  # flags.18?true
        self.min = min  # flags.20?true
        self.bot_inline_geo = bot_inline_geo  # flags.21?true
        self.id = id  # int
        self.access_hash = access_hash  # flags.0?long
        self.first_name = first_name  # flags.1?string
        self.last_name = last_name  # flags.2?string
        self.username = username  # flags.3?string
        self.phone = phone  # flags.4?string
        self.photo = photo  # flags.5?UserProfilePhoto
        self.status = status  # flags.6?UserStatus
        self.bot_info_version = bot_info_version  # flags.14?int
        self.restriction_reason = restriction_reason  # flags.18?string
        self.bot_inline_placeholder = bot_inline_placeholder  # flags.19?string
        self.lang_code = lang_code  # flags.22?string

    @staticmethod
    def read(b: BytesIO, *args) -> "User":
        flags = Int.read(b)
        
        is_self = True if flags & (1 << 10) else False
        contact = True if flags & (1 << 11) else False
        mutual_contact = True if flags & (1 << 12) else False
        deleted = True if flags & (1 << 13) else False
        bot = True if flags & (1 << 14) else False
        bot_chat_history = True if flags & (1 << 15) else False
        bot_nochats = True if flags & (1 << 16) else False
        verified = True if flags & (1 << 17) else False
        restricted = True if flags & (1 << 18) else False
        min = True if flags & (1 << 20) else False
        bot_inline_geo = True if flags & (1 << 21) else False
        id = Int.read(b)
        
        access_hash = Long.read(b) if flags & (1 << 0) else None
        first_name = String.read(b) if flags & (1 << 1) else None
        last_name = String.read(b) if flags & (1 << 2) else None
        username = String.read(b) if flags & (1 << 3) else None
        phone = String.read(b) if flags & (1 << 4) else None
        photo = Object.read(b) if flags & (1 << 5) else None
        
        status = Object.read(b) if flags & (1 << 6) else None
        
        bot_info_version = Int.read(b) if flags & (1 << 14) else None
        restriction_reason = String.read(b) if flags & (1 << 18) else None
        bot_inline_placeholder = String.read(b) if flags & (1 << 19) else None
        lang_code = String.read(b) if flags & (1 << 22) else None
        return User(id, is_self, contact, mutual_contact, deleted, bot, bot_chat_history, bot_nochats, verified, restricted, min, bot_inline_geo, access_hash, first_name, last_name, username, phone, photo, status, bot_info_version, restriction_reason, bot_inline_placeholder, lang_code)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 10) if self.is_self is not None else 0
        flags |= (1 << 11) if self.contact is not None else 0
        flags |= (1 << 12) if self.mutual_contact is not None else 0
        flags |= (1 << 13) if self.deleted is not None else 0
        flags |= (1 << 14) if self.bot is not None else 0
        flags |= (1 << 15) if self.bot_chat_history is not None else 0
        flags |= (1 << 16) if self.bot_nochats is not None else 0
        flags |= (1 << 17) if self.verified is not None else 0
        flags |= (1 << 18) if self.restricted is not None else 0
        flags |= (1 << 20) if self.min is not None else 0
        flags |= (1 << 21) if self.bot_inline_geo is not None else 0
        flags |= (1 << 0) if self.access_hash is not None else 0
        flags |= (1 << 1) if self.first_name is not None else 0
        flags |= (1 << 2) if self.last_name is not None else 0
        flags |= (1 << 3) if self.username is not None else 0
        flags |= (1 << 4) if self.phone is not None else 0
        flags |= (1 << 5) if self.photo is not None else 0
        flags |= (1 << 6) if self.status is not None else 0
        flags |= (1 << 14) if self.bot_info_version is not None else 0
        flags |= (1 << 18) if self.restriction_reason is not None else 0
        flags |= (1 << 19) if self.bot_inline_placeholder is not None else 0
        flags |= (1 << 22) if self.lang_code is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        if self.access_hash is not None:
            b.write(Long(self.access_hash))
        
        if self.first_name is not None:
            b.write(String(self.first_name))
        
        if self.last_name is not None:
            b.write(String(self.last_name))
        
        if self.username is not None:
            b.write(String(self.username))
        
        if self.phone is not None:
            b.write(String(self.phone))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.status is not None:
            b.write(self.status.write())
        
        if self.bot_info_version is not None:
            b.write(Int(self.bot_info_version))
        
        if self.restriction_reason is not None:
            b.write(String(self.restriction_reason))
        
        if self.bot_inline_placeholder is not None:
            b.write(String(self.bot_inline_placeholder))
        
        if self.lang_code is not None:
            b.write(String(self.lang_code))
        
        return b.getvalue()
