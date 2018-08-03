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


class Difference(Object):
    """Attributes:
        ID: ``0x00f49ca0``

    Args:
        new_messages: List of either :obj:`MessageEmpty <pyrogram.api.types.MessageEmpty>`, :obj:`Message <pyrogram.api.types.Message>` or :obj:`MessageService <pyrogram.api.types.MessageService>`
        new_encrypted_messages: List of either :obj:`EncryptedMessage <pyrogram.api.types.EncryptedMessage>` or :obj:`EncryptedMessageService <pyrogram.api.types.EncryptedMessageService>`
        other_updates: List of either :obj:`UpdateNewMessage <pyrogram.api.types.UpdateNewMessage>`, :obj:`UpdateMessageID <pyrogram.api.types.UpdateMessageID>`, :obj:`UpdateDeleteMessages <pyrogram.api.types.UpdateDeleteMessages>`, :obj:`UpdateUserTyping <pyrogram.api.types.UpdateUserTyping>`, :obj:`UpdateChatUserTyping <pyrogram.api.types.UpdateChatUserTyping>`, :obj:`UpdateChatParticipants <pyrogram.api.types.UpdateChatParticipants>`, :obj:`UpdateUserStatus <pyrogram.api.types.UpdateUserStatus>`, :obj:`UpdateUserName <pyrogram.api.types.UpdateUserName>`, :obj:`UpdateUserPhoto <pyrogram.api.types.UpdateUserPhoto>`, :obj:`UpdateContactRegistered <pyrogram.api.types.UpdateContactRegistered>`, :obj:`UpdateContactLink <pyrogram.api.types.UpdateContactLink>`, :obj:`UpdateNewEncryptedMessage <pyrogram.api.types.UpdateNewEncryptedMessage>`, :obj:`UpdateEncryptedChatTyping <pyrogram.api.types.UpdateEncryptedChatTyping>`, :obj:`UpdateEncryption <pyrogram.api.types.UpdateEncryption>`, :obj:`UpdateEncryptedMessagesRead <pyrogram.api.types.UpdateEncryptedMessagesRead>`, :obj:`UpdateChatParticipantAdd <pyrogram.api.types.UpdateChatParticipantAdd>`, :obj:`UpdateChatParticipantDelete <pyrogram.api.types.UpdateChatParticipantDelete>`, :obj:`UpdateDcOptions <pyrogram.api.types.UpdateDcOptions>`, :obj:`UpdateUserBlocked <pyrogram.api.types.UpdateUserBlocked>`, :obj:`UpdateNotifySettings <pyrogram.api.types.UpdateNotifySettings>`, :obj:`UpdateServiceNotification <pyrogram.api.types.UpdateServiceNotification>`, :obj:`UpdatePrivacy <pyrogram.api.types.UpdatePrivacy>`, :obj:`UpdateUserPhone <pyrogram.api.types.UpdateUserPhone>`, :obj:`UpdateReadHistoryInbox <pyrogram.api.types.UpdateReadHistoryInbox>`, :obj:`UpdateReadHistoryOutbox <pyrogram.api.types.UpdateReadHistoryOutbox>`, :obj:`UpdateWebPage <pyrogram.api.types.UpdateWebPage>`, :obj:`UpdateReadMessagesContents <pyrogram.api.types.UpdateReadMessagesContents>`, :obj:`UpdateChannelTooLong <pyrogram.api.types.UpdateChannelTooLong>`, :obj:`UpdateChannel <pyrogram.api.types.UpdateChannel>`, :obj:`UpdateNewChannelMessage <pyrogram.api.types.UpdateNewChannelMessage>`, :obj:`UpdateReadChannelInbox <pyrogram.api.types.UpdateReadChannelInbox>`, :obj:`UpdateDeleteChannelMessages <pyrogram.api.types.UpdateDeleteChannelMessages>`, :obj:`UpdateChannelMessageViews <pyrogram.api.types.UpdateChannelMessageViews>`, :obj:`UpdateChatAdmins <pyrogram.api.types.UpdateChatAdmins>`, :obj:`UpdateChatParticipantAdmin <pyrogram.api.types.UpdateChatParticipantAdmin>`, :obj:`UpdateNewStickerSet <pyrogram.api.types.UpdateNewStickerSet>`, :obj:`UpdateStickerSetsOrder <pyrogram.api.types.UpdateStickerSetsOrder>`, :obj:`UpdateStickerSets <pyrogram.api.types.UpdateStickerSets>`, :obj:`UpdateSavedGifs <pyrogram.api.types.UpdateSavedGifs>`, :obj:`UpdateBotInlineQuery <pyrogram.api.types.UpdateBotInlineQuery>`, :obj:`UpdateBotInlineSend <pyrogram.api.types.UpdateBotInlineSend>`, :obj:`UpdateEditChannelMessage <pyrogram.api.types.UpdateEditChannelMessage>`, :obj:`UpdateChannelPinnedMessage <pyrogram.api.types.UpdateChannelPinnedMessage>`, :obj:`UpdateBotCallbackQuery <pyrogram.api.types.UpdateBotCallbackQuery>`, :obj:`UpdateEditMessage <pyrogram.api.types.UpdateEditMessage>`, :obj:`UpdateInlineBotCallbackQuery <pyrogram.api.types.UpdateInlineBotCallbackQuery>`, :obj:`UpdateReadChannelOutbox <pyrogram.api.types.UpdateReadChannelOutbox>`, :obj:`UpdateDraftMessage <pyrogram.api.types.UpdateDraftMessage>`, :obj:`UpdateReadFeaturedStickers <pyrogram.api.types.UpdateReadFeaturedStickers>`, :obj:`UpdateRecentStickers <pyrogram.api.types.UpdateRecentStickers>`, :obj:`UpdateConfig <pyrogram.api.types.UpdateConfig>`, :obj:`UpdatePtsChanged <pyrogram.api.types.UpdatePtsChanged>`, :obj:`UpdateChannelWebPage <pyrogram.api.types.UpdateChannelWebPage>`, :obj:`UpdateDialogPinned <pyrogram.api.types.UpdateDialogPinned>`, :obj:`UpdatePinnedDialogs <pyrogram.api.types.UpdatePinnedDialogs>`, :obj:`UpdateBotWebhookJSON <pyrogram.api.types.UpdateBotWebhookJSON>`, :obj:`UpdateBotWebhookJSONQuery <pyrogram.api.types.UpdateBotWebhookJSONQuery>`, :obj:`UpdateBotShippingQuery <pyrogram.api.types.UpdateBotShippingQuery>`, :obj:`UpdateBotPrecheckoutQuery <pyrogram.api.types.UpdateBotPrecheckoutQuery>`, :obj:`UpdatePhoneCall <pyrogram.api.types.UpdatePhoneCall>`, :obj:`UpdateLangPackTooLong <pyrogram.api.types.UpdateLangPackTooLong>`, :obj:`UpdateLangPack <pyrogram.api.types.UpdateLangPack>`, :obj:`UpdateFavedStickers <pyrogram.api.types.UpdateFavedStickers>`, :obj:`UpdateChannelReadMessagesContents <pyrogram.api.types.UpdateChannelReadMessagesContents>`, :obj:`UpdateContactsReset <pyrogram.api.types.UpdateContactsReset>` or :obj:`UpdateChannelAvailableMessages <pyrogram.api.types.UpdateChannelAvailableMessages>`
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        state: :obj:`updates.State <pyrogram.api.types.updates.State>`

    See Also:
        This object can be returned by :obj:`updates.GetDifference <pyrogram.api.functions.updates.GetDifference>`.
    """

    ID = 0x00f49ca0

    def __init__(self, new_messages: list, new_encrypted_messages: list, other_updates: list, chats: list, users: list, state):
        self.new_messages = new_messages  # Vector<Message>
        self.new_encrypted_messages = new_encrypted_messages  # Vector<EncryptedMessage>
        self.other_updates = other_updates  # Vector<Update>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.state = state  # updates.State

    @staticmethod
    def read(b: BytesIO, *args) -> "Difference":
        # No flags
        
        new_messages = Object.read(b)
        
        new_encrypted_messages = Object.read(b)
        
        other_updates = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        state = Object.read(b)
        
        return Difference(new_messages, new_encrypted_messages, other_updates, chats, users, state)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.new_messages))
        
        b.write(Vector(self.new_encrypted_messages))
        
        b.write(Vector(self.other_updates))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(self.state.write())
        
        return b.getvalue()
