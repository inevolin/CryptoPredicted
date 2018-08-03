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

from .get_messages import GetMessages
from .get_dialogs import GetDialogs
from .get_history import GetHistory
from .search import Search
from .read_history import ReadHistory
from .delete_history import DeleteHistory
from .delete_messages import DeleteMessages
from .received_messages import ReceivedMessages
from .set_typing import SetTyping
from .send_message import SendMessage
from .send_media import SendMedia
from .forward_messages import ForwardMessages
from .report_spam import ReportSpam
from .hide_report_spam import HideReportSpam
from .get_peer_settings import GetPeerSettings
from .report import Report
from .get_chats import GetChats
from .get_full_chat import GetFullChat
from .edit_chat_title import EditChatTitle
from .edit_chat_photo import EditChatPhoto
from .add_chat_user import AddChatUser
from .delete_chat_user import DeleteChatUser
from .create_chat import CreateChat
from .get_dh_config import GetDhConfig
from .request_encryption import RequestEncryption
from .accept_encryption import AcceptEncryption
from .discard_encryption import DiscardEncryption
from .set_encrypted_typing import SetEncryptedTyping
from .read_encrypted_history import ReadEncryptedHistory
from .send_encrypted import SendEncrypted
from .send_encrypted_file import SendEncryptedFile
from .send_encrypted_service import SendEncryptedService
from .received_queue import ReceivedQueue
from .report_encrypted_spam import ReportEncryptedSpam
from .read_message_contents import ReadMessageContents
from .get_stickers import GetStickers
from .get_all_stickers import GetAllStickers
from .get_web_page_preview import GetWebPagePreview
from .export_chat_invite import ExportChatInvite
from .check_chat_invite import CheckChatInvite
from .import_chat_invite import ImportChatInvite
from .get_sticker_set import GetStickerSet
from .install_sticker_set import InstallStickerSet
from .uninstall_sticker_set import UninstallStickerSet
from .start_bot import StartBot
from .get_messages_views import GetMessagesViews
from .toggle_chat_admins import ToggleChatAdmins
from .edit_chat_admin import EditChatAdmin
from .migrate_chat import MigrateChat
from .search_global import SearchGlobal
from .reorder_sticker_sets import ReorderStickerSets
from .get_document_by_hash import GetDocumentByHash
from .search_gifs import SearchGifs
from .get_saved_gifs import GetSavedGifs
from .save_gif import SaveGif
from .get_inline_bot_results import GetInlineBotResults
from .set_inline_bot_results import SetInlineBotResults
from .send_inline_bot_result import SendInlineBotResult
from .get_message_edit_data import GetMessageEditData
from .edit_message import EditMessage
from .edit_inline_bot_message import EditInlineBotMessage
from .get_bot_callback_answer import GetBotCallbackAnswer
from .set_bot_callback_answer import SetBotCallbackAnswer
from .get_peer_dialogs import GetPeerDialogs
from .save_draft import SaveDraft
from .get_all_drafts import GetAllDrafts
from .get_featured_stickers import GetFeaturedStickers
from .read_featured_stickers import ReadFeaturedStickers
from .get_recent_stickers import GetRecentStickers
from .save_recent_sticker import SaveRecentSticker
from .clear_recent_stickers import ClearRecentStickers
from .get_archived_stickers import GetArchivedStickers
from .get_mask_stickers import GetMaskStickers
from .get_attached_stickers import GetAttachedStickers
from .set_game_score import SetGameScore
from .set_inline_game_score import SetInlineGameScore
from .get_game_high_scores import GetGameHighScores
from .get_inline_game_high_scores import GetInlineGameHighScores
from .get_common_chats import GetCommonChats
from .get_all_chats import GetAllChats
from .get_web_page import GetWebPage
from .toggle_dialog_pin import ToggleDialogPin
from .reorder_pinned_dialogs import ReorderPinnedDialogs
from .get_pinned_dialogs import GetPinnedDialogs
from .set_bot_shipping_results import SetBotShippingResults
from .set_bot_precheckout_results import SetBotPrecheckoutResults
from .upload_media import UploadMedia
from .send_screenshot_notification import SendScreenshotNotification
from .get_faved_stickers import GetFavedStickers
from .fave_sticker import FaveSticker
from .get_unread_mentions import GetUnreadMentions
from .read_mentions import ReadMentions
from .get_recent_locations import GetRecentLocations
from .send_multi_media import SendMultiMedia
from .upload_encrypted_file import UploadEncryptedFile
from .search_sticker_sets import SearchStickerSets
