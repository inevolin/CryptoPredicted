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


class UpdatesCombined(Object):
    """Attributes:
        ID: ``0x725b04c3``

    Args:
        updates: List of either :obj:`UpdateNewMessage <pyrogram.api.types.UpdateNewMessage>`, :obj:`UpdateMessageID <pyrogram.api.types.UpdateMessageID>`, :obj:`UpdateDeleteMessages <pyrogram.api.types.UpdateDeleteMessages>`, :obj:`UpdateUserTyping <pyrogram.api.types.UpdateUserTyping>`, :obj:`UpdateChatUserTyping <pyrogram.api.types.UpdateChatUserTyping>`, :obj:`UpdateChatParticipants <pyrogram.api.types.UpdateChatParticipants>`, :obj:`UpdateUserStatus <pyrogram.api.types.UpdateUserStatus>`, :obj:`UpdateUserName <pyrogram.api.types.UpdateUserName>`, :obj:`UpdateUserPhoto <pyrogram.api.types.UpdateUserPhoto>`, :obj:`UpdateContactRegistered <pyrogram.api.types.UpdateContactRegistered>`, :obj:`UpdateContactLink <pyrogram.api.types.UpdateContactLink>`, :obj:`UpdateNewEncryptedMessage <pyrogram.api.types.UpdateNewEncryptedMessage>`, :obj:`UpdateEncryptedChatTyping <pyrogram.api.types.UpdateEncryptedChatTyping>`, :obj:`UpdateEncryption <pyrogram.api.types.UpdateEncryption>`, :obj:`UpdateEncryptedMessagesRead <pyrogram.api.types.UpdateEncryptedMessagesRead>`, :obj:`UpdateChatParticipantAdd <pyrogram.api.types.UpdateChatParticipantAdd>`, :obj:`UpdateChatParticipantDelete <pyrogram.api.types.UpdateChatParticipantDelete>`, :obj:`UpdateDcOptions <pyrogram.api.types.UpdateDcOptions>`, :obj:`UpdateUserBlocked <pyrogram.api.types.UpdateUserBlocked>`, :obj:`UpdateNotifySettings <pyrogram.api.types.UpdateNotifySettings>`, :obj:`UpdateServiceNotification <pyrogram.api.types.UpdateServiceNotification>`, :obj:`UpdatePrivacy <pyrogram.api.types.UpdatePrivacy>`, :obj:`UpdateUserPhone <pyrogram.api.types.UpdateUserPhone>`, :obj:`UpdateReadHistoryInbox <pyrogram.api.types.UpdateReadHistoryInbox>`, :obj:`UpdateReadHistoryOutbox <pyrogram.api.types.UpdateReadHistoryOutbox>`, :obj:`UpdateWebPage <pyrogram.api.types.UpdateWebPage>`, :obj:`UpdateReadMessagesContents <pyrogram.api.types.UpdateReadMessagesContents>`, :obj:`UpdateChannelTooLong <pyrogram.api.types.UpdateChannelTooLong>`, :obj:`UpdateChannel <pyrogram.api.types.UpdateChannel>`, :obj:`UpdateNewChannelMessage <pyrogram.api.types.UpdateNewChannelMessage>`, :obj:`UpdateReadChannelInbox <pyrogram.api.types.UpdateReadChannelInbox>`, :obj:`UpdateDeleteChannelMessages <pyrogram.api.types.UpdateDeleteChannelMessages>`, :obj:`UpdateChannelMessageViews <pyrogram.api.types.UpdateChannelMessageViews>`, :obj:`UpdateChatAdmins <pyrogram.api.types.UpdateChatAdmins>`, :obj:`UpdateChatParticipantAdmin <pyrogram.api.types.UpdateChatParticipantAdmin>`, :obj:`UpdateNewStickerSet <pyrogram.api.types.UpdateNewStickerSet>`, :obj:`UpdateStickerSetsOrder <pyrogram.api.types.UpdateStickerSetsOrder>`, :obj:`UpdateStickerSets <pyrogram.api.types.UpdateStickerSets>`, :obj:`UpdateSavedGifs <pyrogram.api.types.UpdateSavedGifs>`, :obj:`UpdateBotInlineQuery <pyrogram.api.types.UpdateBotInlineQuery>`, :obj:`UpdateBotInlineSend <pyrogram.api.types.UpdateBotInlineSend>`, :obj:`UpdateEditChannelMessage <pyrogram.api.types.UpdateEditChannelMessage>`, :obj:`UpdateChannelPinnedMessage <pyrogram.api.types.UpdateChannelPinnedMessage>`, :obj:`UpdateBotCallbackQuery <pyrogram.api.types.UpdateBotCallbackQuery>`, :obj:`UpdateEditMessage <pyrogram.api.types.UpdateEditMessage>`, :obj:`UpdateInlineBotCallbackQuery <pyrogram.api.types.UpdateInlineBotCallbackQuery>`, :obj:`UpdateReadChannelOutbox <pyrogram.api.types.UpdateReadChannelOutbox>`, :obj:`UpdateDraftMessage <pyrogram.api.types.UpdateDraftMessage>`, :obj:`UpdateReadFeaturedStickers <pyrogram.api.types.UpdateReadFeaturedStickers>`, :obj:`UpdateRecentStickers <pyrogram.api.types.UpdateRecentStickers>`, :obj:`UpdateConfig <pyrogram.api.types.UpdateConfig>`, :obj:`UpdatePtsChanged <pyrogram.api.types.UpdatePtsChanged>`, :obj:`UpdateChannelWebPage <pyrogram.api.types.UpdateChannelWebPage>`, :obj:`UpdateDialogPinned <pyrogram.api.types.UpdateDialogPinned>`, :obj:`UpdatePinnedDialogs <pyrogram.api.types.UpdatePinnedDialogs>`, :obj:`UpdateBotWebhookJSON <pyrogram.api.types.UpdateBotWebhookJSON>`, :obj:`UpdateBotWebhookJSONQuery <pyrogram.api.types.UpdateBotWebhookJSONQuery>`, :obj:`UpdateBotShippingQuery <pyrogram.api.types.UpdateBotShippingQuery>`, :obj:`UpdateBotPrecheckoutQuery <pyrogram.api.types.UpdateBotPrecheckoutQuery>`, :obj:`UpdatePhoneCall <pyrogram.api.types.UpdatePhoneCall>`, :obj:`UpdateLangPackTooLong <pyrogram.api.types.UpdateLangPackTooLong>`, :obj:`UpdateLangPack <pyrogram.api.types.UpdateLangPack>`, :obj:`UpdateFavedStickers <pyrogram.api.types.UpdateFavedStickers>`, :obj:`UpdateChannelReadMessagesContents <pyrogram.api.types.UpdateChannelReadMessagesContents>`, :obj:`UpdateContactsReset <pyrogram.api.types.UpdateContactsReset>` or :obj:`UpdateChannelAvailableMessages <pyrogram.api.types.UpdateChannelAvailableMessages>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        date: ``int`` ``32-bit``
        seq_start: ``int`` ``32-bit``
        seq: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.SendMessage <pyrogram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <pyrogram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <pyrogram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <pyrogram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <pyrogram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <pyrogram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <pyrogram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <pyrogram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <pyrogram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <pyrogram.api.functions.messages.StartBot>`, :obj:`messages.ToggleChatAdmins <pyrogram.api.functions.messages.ToggleChatAdmins>`, :obj:`messages.MigrateChat <pyrogram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <pyrogram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <pyrogram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <pyrogram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <pyrogram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <pyrogram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <pyrogram.api.functions.messages.SendMultiMedia>`, :obj:`help.GetAppChangelog <pyrogram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <pyrogram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <pyrogram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <pyrogram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <pyrogram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <pyrogram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <pyrogram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <pyrogram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <pyrogram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleInvites <pyrogram.api.functions.channels.ToggleInvites>`, :obj:`channels.ToggleSignatures <pyrogram.api.functions.channels.ToggleSignatures>`, :obj:`channels.UpdatePinnedMessage <pyrogram.api.functions.channels.UpdatePinnedMessage>`, :obj:`channels.EditBanned <pyrogram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <pyrogram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <pyrogram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <pyrogram.api.functions.phone.SetCallRating>`.
    """

    ID = 0x725b04c3

    def __init__(self, updates: list, users: list, chats: list, date: int, seq_start: int, seq: int):
        self.updates = updates  # Vector<Update>
        self.users = users  # Vector<User>
        self.chats = chats  # Vector<Chat>
        self.date = date  # int
        self.seq_start = seq_start  # int
        self.seq = seq  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatesCombined":
        # No flags
        
        updates = Object.read(b)
        
        users = Object.read(b)
        
        chats = Object.read(b)
        
        date = Int.read(b)
        
        seq_start = Int.read(b)
        
        seq = Int.read(b)
        
        return UpdatesCombined(updates, users, chats, date, seq_start, seq)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.updates))
        
        b.write(Vector(self.users))
        
        b.write(Vector(self.chats))
        
        b.write(Int(self.date))
        
        b.write(Int(self.seq_start))
        
        b.write(Int(self.seq))
        
        return b.getvalue()
