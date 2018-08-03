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

from .register_device import RegisterDevice
from .unregister_device import UnregisterDevice
from .update_notify_settings import UpdateNotifySettings
from .get_notify_settings import GetNotifySettings
from .reset_notify_settings import ResetNotifySettings
from .update_profile import UpdateProfile
from .update_status import UpdateStatus
from .get_wall_papers import GetWallPapers
from .report_peer import ReportPeer
from .check_username import CheckUsername
from .update_username import UpdateUsername
from .get_privacy import GetPrivacy
from .set_privacy import SetPrivacy
from .delete_account import DeleteAccount
from .get_account_ttl import GetAccountTTL
from .set_account_ttl import SetAccountTTL
from .send_change_phone_code import SendChangePhoneCode
from .change_phone import ChangePhone
from .update_device_locked import UpdateDeviceLocked
from .get_authorizations import GetAuthorizations
from .reset_authorization import ResetAuthorization
from .get_password import GetPassword
from .get_password_settings import GetPasswordSettings
from .update_password_settings import UpdatePasswordSettings
from .send_confirm_phone_code import SendConfirmPhoneCode
from .confirm_phone import ConfirmPhone
from .get_tmp_password import GetTmpPassword
from .get_web_authorizations import GetWebAuthorizations
from .reset_web_authorization import ResetWebAuthorization
from .reset_web_authorizations import ResetWebAuthorizations
from .get_all_secure_values import GetAllSecureValues
from .get_secure_value import GetSecureValue
from .save_secure_value import SaveSecureValue
from .delete_secure_value import DeleteSecureValue
from .get_authorization_form import GetAuthorizationForm
from .accept_authorization import AcceptAuthorization
from .send_verify_phone_code import SendVerifyPhoneCode
from .verify_phone import VerifyPhone
from .send_verify_email_code import SendVerifyEmailCode
from .verify_email import VerifyEmail
