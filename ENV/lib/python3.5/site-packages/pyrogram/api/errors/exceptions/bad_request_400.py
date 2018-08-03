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

from ..error import Error


class BadRequest(Error):
    """Bad Request"""
    CODE = 400
    """``int``: Error Code"""
    NAME = __doc__


class FirstnameInvalid(BadRequest):
    """The first name is invalid"""
    ID = "FIRSTNAME_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class LastnameInvalid(BadRequest):
    """The last name is invalid"""
    ID = "LASTNAME_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneNumberInvalid(BadRequest):
    """The phone number is invalid"""
    ID = "PHONE_NUMBER_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneCodeHashEmpty(BadRequest):
    """phone_code_hash is missing"""
    ID = "PHONE_CODE_HASH_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneCodeEmpty(BadRequest):
    """phone_code is missing"""
    ID = "PHONE_CODE_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneCodeExpired(BadRequest):
    """The confirmation code has expired"""
    ID = "PHONE_CODE_EXPIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneCodeInvalid(BadRequest):
    """The confirmation code is invalid"""
    ID = "PHONE_CODE_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class ApiIdInvalid(BadRequest):
    """The api_id/api_hash combination is invalid"""
    ID = "API_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneNumberOccupied(BadRequest):
    """The phone number is already in use"""
    ID = "PHONE_NUMBER_OCCUPIED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneNumberUnoccupied(BadRequest):
    """The phone number is not yet being used"""
    ID = "PHONE_NUMBER_UNOCCUPIED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UsersTooFew(BadRequest):
    """Not enough users (to create a chat, for example)"""
    ID = "USERS_TOO_FEW"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UsersTooMuch(BadRequest):
    """The maximum number of users has been exceeded (to create a chat, for example)"""
    ID = "USERS_TOO_MUCH"
    """``str``: Error ID"""
    MESSAGE = __doc__


class TypeConstructorInvalid(BadRequest):
    """The type constructor is invalid"""
    ID = "TYPE_CONSTRUCTOR_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FilePartInvalid(BadRequest):
    """The file part number is invalid"""
    ID = "FILE_PART_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FilePartsInvalid(BadRequest):
    """The number of file parts is invalid"""
    ID = "FILE_PARTS_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FilePartMissing(BadRequest):
    """Part {x} of the file is missing from storage"""
    ID = "FILE_PART_X_MISSING"
    """``str``: Error ID"""
    MESSAGE = __doc__


class Md5ChecksumInvalid(BadRequest):
    """The MD5 checksums do not match"""
    ID = "MD5_CHECKSUM_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhotoInvalidDimensions(BadRequest):
    """The photo dimensions are invalid"""
    ID = "PHOTO_INVALID_DIMENSIONS"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FieldNameInvalid(BadRequest):
    """The field with the name FIELD_NAME is invalid"""
    ID = "FIELD_NAME_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FieldNameEmpty(BadRequest):
    """The field with the name FIELD_NAME is missing"""
    ID = "FIELD_NAME_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MsgWaitFailed(BadRequest):
    """A waiting call returned an error"""
    ID = "MSG_WAIT_FAILED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PeerIdInvalid(BadRequest):
    """The id/access_hash combination is invalid"""
    ID = "PEER_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MessageEmpty(BadRequest):
    """The message sent is empty"""
    ID = "MESSAGE_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class EncryptedMessageInvalid(BadRequest):
    """The special binding message (bind_auth_key_inner) contains invalid data"""
    ID = "ENCRYPTED_MESSAGE_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class InputMethodInvalid(BadRequest):
    """The method called is invalid"""
    ID = "INPUT_METHOD_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PasswordHashInvalid(BadRequest):
    """Two-step verification password is invalid"""
    ID = "PASSWORD_HASH_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UsernameNotOccupied(BadRequest):
    """The username is not occupied by anyone"""
    ID = "USERNAME_NOT_OCCUPIED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UsernameInvalid(BadRequest):
    """The username is invalid"""
    ID = "USERNAME_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MessageIdInvalid(BadRequest):
    """The message id is invalid"""
    ID = "MESSAGE_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MessageNotModified(BadRequest):
    """The message was not modified"""
    ID = "MESSAGE_NOT_MODIFIED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class EntityMentionUserInvalid(BadRequest):
    """The mentioned entity is not an user"""
    ID = "ENTITY_MENTION_USER_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MessageTooLong(BadRequest):
    """The message text is over 4096 characters"""
    ID = "MESSAGE_TOO_LONG"
    """``str``: Error ID"""
    MESSAGE = __doc__


class AccessTokenExpired(BadRequest):
    """The bot token is invalid"""
    ID = "ACCESS_TOKEN_EXPIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class BotMethodInvalid(BadRequest):
    """The method can't be used by bots"""
    ID = "BOT_METHOD_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class QueryTooShort(BadRequest):
    """The query is too short"""
    ID = "QUERY_TOO_SHORT"
    """``str``: Error ID"""
    MESSAGE = __doc__


class SearchQueryEmpty(BadRequest):
    """The query is empty"""
    ID = "SEARCH_QUERY_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class ChatIdInvalid(BadRequest):
    """The chat id is invalid"""
    ID = "CHAT_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class DateEmpty(BadRequest):
    """The date argument is empty"""
    ID = "DATE_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PersistentTimestampEmpty(BadRequest):
    """The pts is empty"""
    ID = "PERSISTENT_TIMESTAMP_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class CdnMethodInvalid(BadRequest):
    """The method can't be used on CDN DCs"""
    ID = "CDN_METHOD_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class VolumeLocNotFound(BadRequest):
    """The volume location can't be found"""
    ID = "VOLUME_LOC_NOT_FOUND"
    """``str``: Error ID"""
    MESSAGE = __doc__


class FileIdInvalid(BadRequest):
    """The file id is invalid"""
    ID = "FILE_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class LocationInvalid(BadRequest):
    """The file location is invalid"""
    ID = "LOCATION_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class ChatAdminRequired(BadRequest):
    """The method requires chat admin privileges"""
    ID = "CHAT_ADMIN_REQUIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PhoneNumberBanned(BadRequest):
    """The phone number is banned"""
    ID = "PHONE_NUMBER_BANNED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class AboutTooLong(BadRequest):
    """The about text is too long"""
    ID = "ABOUT_TOO_LONG"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MultiMediaTooLong(BadRequest):
    """The album contains more than 10 items"""
    ID = "MULTI_MEDIA_TOO_LONG"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UsernameOccupied(BadRequest):
    """The username is already in use"""
    ID = "USERNAME_OCCUPIED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class BotInlineDisabled(BadRequest):
    """The inline feature of the bot is disabled"""
    ID = "BOT_INLINE_DISABLED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class InlineResultExpired(BadRequest):
    """The inline bot query expired"""
    ID = "INLINE_RESULT_EXPIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class InviteHashInvalid(BadRequest):
    """The invite link hash is invalid"""
    ID = "INVITE_HASH_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UserAlreadyParticipant(BadRequest):
    """The user is already a participant of this chat"""
    ID = "USER_ALREADY_PARTICIPANT"
    """``str``: Error ID"""
    MESSAGE = __doc__


class TtlMediaInvalid(BadRequest):
    """This kind of media does not support self-destruction"""
    ID = "TTL_MEDIA_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MaxIdInvalid(BadRequest):
    """The max_id parameter is invalid"""
    ID = "MAX_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class ChannelInvalid(BadRequest):
    """The channel parameter is invalid"""
    ID = "CHANNEL_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class DcIdInvalid(BadRequest):
    """The dc_id parameter is invalid"""
    ID = "DC_ID_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class LimitInvalid(BadRequest):
    """The limit parameter is invalid"""
    ID = "LIMIT_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class OffsetInvalid(BadRequest):
    """The offset parameter is invalid"""
    ID = "OFFSET_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class EmailInvalid(BadRequest):
    """The email provided is invalid"""
    ID = "EMAIL_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UserIsBot(BadRequest):
    """A bot cannot send messages to other bots or to itself"""
    ID = "USER_IS_BOT"
    """``str``: Error ID"""
    MESSAGE = __doc__


class WebpageCurlFailed(BadRequest):
    """Telegram could not fetch the provided URL"""
    ID = "WEBPAGE_CURL_FAILED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class StickersetInvalid(BadRequest):
    """The requested sticker set is invalid"""
    ID = "STICKERSET_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PeerFlood(BadRequest):
    """The method can't be used because your account is limited"""
    ID = "PEER_FLOOD"
    """``str``: Error ID"""
    MESSAGE = __doc__


class MediaCaptionTooLong(BadRequest):
    """The media caption is longer than 200 characters"""
    ID = "MEDIA_CAPTION_TOO_LONG"
    """``str``: Error ID"""
    MESSAGE = __doc__


