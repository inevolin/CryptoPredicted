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


class Unauthorized(Error):
    """Unauthorized"""
    CODE = 401
    """``int``: Error Code"""
    NAME = __doc__


class AuthKeyUnregistered(Unauthorized):
    """The key is not registered in the system"""
    ID = "AUTH_KEY_UNREGISTERED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class AuthKeyInvalid(Unauthorized):
    """The key is invalid"""
    ID = "AUTH_KEY_INVALID"
    """``str``: Error ID"""
    MESSAGE = __doc__


class UserDeactivated(Unauthorized):
    """The user has been deleted/deactivated"""
    ID = "USER_DEACTIVATED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class SessionRevoked(Unauthorized):
    """The authorization has been invalidated, because of the user terminating all sessions"""
    ID = "SESSION_REVOKED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class SessionExpired(Unauthorized):
    """The authorization has expired"""
    ID = "SESSION_EXPIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class ActiveUserRequired(Unauthorized):
    """The method is only available to already activated users"""
    ID = "ACTIVE_USER_REQUIRED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class AuthKeyPermEmpty(Unauthorized):
    """The method is unavailable for temporary authorization key, not bound to permanent"""
    ID = "AUTH_KEY_PERM_EMPTY"
    """``str``: Error ID"""
    MESSAGE = __doc__


class SessionPasswordNeeded(Unauthorized):
    """Two-step verification password required"""
    ID = "SESSION_PASSWORD_NEEDED"
    """``str``: Error ID"""
    MESSAGE = __doc__


