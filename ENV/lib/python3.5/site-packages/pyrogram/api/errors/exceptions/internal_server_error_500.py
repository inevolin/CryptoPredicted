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


class InternalServerError(Error):
    """Internal Server Error"""
    CODE = 500
    """``int``: Error Code"""
    NAME = __doc__


class AuthRestart(InternalServerError):
    """User authorization has restarted"""
    ID = "AUTH_RESTART"
    """``str``: Error ID"""
    MESSAGE = __doc__


class RpcCallFail(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "RPC_CALL_FAIL"
    """``str``: Error ID"""
    MESSAGE = __doc__


class RpcMcgetFail(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "RPC_MCGET_FAIL"
    """``str``: Error ID"""
    MESSAGE = __doc__


class PersistentTimestampOutdated(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "PERSISTENT_TIMESTAMP_OUTDATED"
    """``str``: Error ID"""
    MESSAGE = __doc__


class HistoryGetFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "HISTORY_GET_FAILED"
    """``str``: Error ID"""
    MESSAGE = __doc__


