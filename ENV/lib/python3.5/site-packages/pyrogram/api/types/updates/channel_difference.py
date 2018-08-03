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


class ChannelDifference(Object):
    """Attributes:
        ID: ``0x2064674e``

    Args:
        pts: ``int`` ``32-bit``
        new_messages: List of either :obj:`MessageEmpty <pyrogram.api.types.MessageEmpty>`, :obj:`Message <pyrogram.api.types.Message>` or :obj:`MessageService <pyrogram.api.types.MessageService>`
        other_updates: List of either :obj:`UpdateNewMessage <pyrogram.api.types.UpdateNewMessage>`, :obj:`UpdateMessageID <pyrogram.api.types.UpdateMessageID>`, :obj:`UpdateDeleteMessages <pyrogram.api.types.UpdateDeleteMessages>`, :obj:`UpdateUserTyping <pyrogram.api.types.UpdateUserTyping>`, :obj:`UpdateChatUserTyping <pyrogram.api.types.UpdateChatUserTyping>`, :obj:`UpdateChatParticipants <pyrogram.api.types.UpdateChatParticipants>`, :obj:`UpdateUserStatus <pyrogram.api.types.UpdateUserStatus>`, :obj:`UpdateUserName <pyrogram.api.types.UpdateUserName>`, :obj:`UpdateUserPhoto <pyrogram.api.types.UpdateUserPhoto>`, :obj:`UpdateContactRegistered <pyrogram.api.types.UpdateContactRegistered>`, :obj:`UpdateContactLink <pyrogram.api.types.UpdateContactLink>`, :obj:`UpdateNewEncryptedMessage <pyrogram.api.types.UpdateNewEncryptedMessage>`, :obj:`UpdateEncryptedChatTyping <pyrogram.api.types.UpdateEncryptedChatTyping>`, :obj:`UpdateEncryption <pyrogram.api.types.UpdateEncryption>`, :obj:`UpdateEncryptedMessagesRead <pyrogram.api.types.UpdateEncryptedMessagesRead>`, :obj:`UpdateChatParticipantAdd <pyrogram.api.types.UpdateChatParticipantAdd>`, :obj:`UpdateChatParticipantDelete <pyrogram.api.types.UpdateChatParticipantDelete>`, :obj:`UpdateDcOptions <pyrogram.api.types.UpdateDcOptions>`, :obj:`UpdateUserBlocked <pyrogram.api.types.UpdateUserBlocked>`, :obj:`UpdateNotifySettings <pyrogram.api.types.UpdateNotifySettings>`, :obj:`UpdateServiceNotification <pyrogram.api.types.UpdateServiceNotification>`, :obj:`UpdatePrivacy <pyrogram.api.types.UpdatePrivacy>`, :obj:`UpdateUserPhone <pyrogram.api.types.UpdateUserPhone>`, :obj:`UpdateReadHistoryInbox <pyrogram.api.types.UpdateReadHistoryInbox>`, :obj:`UpdateReadHistoryOutbox <pyrogram.api.types.UpdateReadHistoryOutbox>`, :obj:`UpdateWebPage <pyrogram.api.types.UpdateWebPage>`, :obj:`UpdateReadMessagesContents <pyrogram.api.types.UpdateReadMessagesContents>`, :obj:`UpdateChannelTooLong <pyrogram.api.types.UpdateChannelTooLong>`, :obj:`UpdateChannel <pyrogram.api.types.UpdateChannel>`, :obj:`UpdateNewChannelMessage <pyrogram.api.types.UpdateNewChannelMessage>`, :obj:`UpdateReadChannelInbox <pyrogram.api.types.UpdateReadChannelInbox>`, :obj:`UpdateDeleteChannelMessages <pyrogram.api.types.UpdateDeleteChannelMessages>`, :obj:`UpdateChannelMessageViews <pyrogram.api.types.UpdateChannelMessageViews>`, :obj:`UpdateChatAdmins <pyrogram.api.types.UpdateChatAdmins>`, :obj:`UpdateChatParticipantAdmin <pyrogram.api.types.UpdateChatParticipantAdmin>`, :obj:`UpdateNewStickerSet <pyrogram.api.types.UpdateNewStickerSet>`, :obj:`UpdateStickerSetsOrder <pyrogram.api.types.UpdateStickerSetsOrder>`, :obj:`UpdateStickerSets <pyrogram.api.types.UpdateStickerSets>`, :obj:`UpdateSavedGifs <pyrogram.api.types.UpdateSavedGifs>`, :obj:`UpdateBotInlineQuery <pyrogram.api.types.UpdateBotInlineQuery>`, :obj:`UpdateBotInlineSend <pyrogram.api.types.UpdateBotInlineSend>`, :obj:`UpdateEditChannelMessage <pyrogram.api.types.UpdateEditChannelMessage>`, :obj:`UpdateChannelPinnedMessage <pyrogram.api.types.UpdateChannelPinnedMessage>`, :obj:`UpdateBotCallbackQuery <pyrogram.api.types.UpdateBotCallbackQuery>`, :obj:`UpdateEditMessage <pyrogram.api.types.UpdateEditMessage>`, :obj:`UpdateInlineBotCallbackQuery <pyrogram.api.types.UpdateInlineBotCallbackQuery>`, :obj:`UpdateReadChannelOutbox <pyrogram.api.types.UpdateReadChannelOutbox>`, :obj:`UpdateDraftMessage <pyrogram.api.types.UpdateDraftMessage>`, :obj:`UpdateReadFeaturedStickers <pyrogram.api.types.UpdateReadFeaturedStickers>`, :obj:`UpdateRecentStickers <pyrogram.api.types.UpdateRecentStickers>`, :obj:`UpdateConfig <pyrogram.api.types.UpdateConfig>`, :obj:`UpdatePtsChanged <pyrogram.api.types.UpdatePtsChanged>`, :obj:`UpdateChannelWebPage <pyrogram.api.types.UpdateChannelWebPage>`, :obj:`UpdateDialogPinned <pyrogram.api.types.UpdateDialogPinned>`, :obj:`UpdatePinnedDialogs <pyrogram.api.types.UpdatePinnedDialogs>`, :obj:`UpdateBotWebhookJSON <pyrogram.api.types.UpdateBotWebhookJSON>`, :obj:`UpdateBotWebhookJSONQuery <pyrogram.api.types.UpdateBotWebhookJSONQuery>`, :obj:`UpdateBotShippingQuery <pyrogram.api.types.UpdateBotShippingQuery>`, :obj:`UpdateBotPrecheckoutQuery <pyrogram.api.types.UpdateBotPrecheckoutQuery>`, :obj:`UpdatePhoneCall <pyrogram.api.types.UpdatePhoneCall>`, :obj:`UpdateLangPackTooLong <pyrogram.api.types.UpdateLangPackTooLong>`, :obj:`UpdateLangPack <pyrogram.api.types.UpdateLangPack>`, :obj:`UpdateFavedStickers <pyrogram.api.types.UpdateFavedStickers>`, :obj:`UpdateChannelReadMessagesContents <pyrogram.api.types.UpdateChannelReadMessagesContents>`, :obj:`UpdateContactsReset <pyrogram.api.types.UpdateContactsReset>` or :obj:`UpdateChannelAvailableMessages <pyrogram.api.types.UpdateChannelAvailableMessages>`
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        final (optional): ``bool``
        timeout (optional): ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`updates.GetChannelDifference <pyrogram.api.functions.updates.GetChannelDifference>`.
    """

    ID = 0x2064674e

    def __init__(self, pts: int, new_messages: list, other_updates: list, chats: list, users: list, final: bool = None, timeout: int = None):
        self.final = final  # flags.0?true
        self.pts = pts  # int
        self.timeout = timeout  # flags.1?int
        self.new_messages = new_messages  # Vector<Message>
        self.other_updates = other_updates  # Vector<Update>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelDifference":
        flags = Int.read(b)
        
        final = True if flags & (1 << 0) else False
        pts = Int.read(b)
        
        timeout = Int.read(b) if flags & (1 << 1) else None
        new_messages = Object.read(b)
        
        other_updates = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return ChannelDifference(pts, new_messages, other_updates, chats, users, final, timeout)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.final is not None else 0
        flags |= (1 << 1) if self.timeout is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.pts))
        
        if self.timeout is not None:
            b.write(Int(self.timeout))
        
        b.write(Vector(self.new_messages))
        
        b.write(Vector(self.other_updates))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
