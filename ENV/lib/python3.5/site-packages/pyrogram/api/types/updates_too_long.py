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


class UpdatesTooLong(Object):
    """Attributes:
        ID: ``0xe317af7e``

    No parameters required.

    See Also:
        This object can be returned by :obj:`messages.SendMessage <pyrogram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <pyrogram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <pyrogram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <pyrogram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <pyrogram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <pyrogram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <pyrogram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <pyrogram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <pyrogram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <pyrogram.api.functions.messages.StartBot>`, :obj:`messages.ToggleChatAdmins <pyrogram.api.functions.messages.ToggleChatAdmins>`, :obj:`messages.MigrateChat <pyrogram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <pyrogram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <pyrogram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <pyrogram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <pyrogram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <pyrogram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <pyrogram.api.functions.messages.SendMultiMedia>`, :obj:`help.GetAppChangelog <pyrogram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <pyrogram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <pyrogram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <pyrogram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <pyrogram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <pyrogram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <pyrogram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <pyrogram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <pyrogram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleInvites <pyrogram.api.functions.channels.ToggleInvites>`, :obj:`channels.ToggleSignatures <pyrogram.api.functions.channels.ToggleSignatures>`, :obj:`channels.UpdatePinnedMessage <pyrogram.api.functions.channels.UpdatePinnedMessage>`, :obj:`channels.EditBanned <pyrogram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <pyrogram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <pyrogram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <pyrogram.api.functions.phone.SetCallRating>`.
    """

    ID = 0xe317af7e

    def __init__(self):
        pass

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatesTooLong":
        # No flags
        
        return UpdatesTooLong()

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
