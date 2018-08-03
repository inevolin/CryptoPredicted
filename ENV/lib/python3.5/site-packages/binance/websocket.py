#!/usr/bin/env python
# coding=utf-8

import asyncio
import json
import websockets as ws

from binance.client import Client


class Websockets(object):

    _stream_url = 'wss://stream.binance.com:9443/'

    def __init__(self, client):
        """Initialise the BinanceSocketManager

        :param client: Binance API client
        :type client: binance.Client

        """
        self._conns = {}
        self._user_timer = None
        self._user_listen_key = None
        self._user_callback = None
        self._loop = asyncio.get_event_loop()
        self._client = client

    def _start_socket(self, path, prefix='ws/'):
        if path in self._conns:
            return False

        ws_url = self._stream_url + prefix + path

        async def _watch_for_events():

            # logger.debug('opening websocket connection: {ws_url}')
            async with ws.connect(ws_url) as socket:
                while True:
                    event = await socket.recv()
                    event_dict = json.loads(event)

                    if hasattr(self, 'on_event'):
                        print('on_event')
                        await self.on_candlesticks_event(event_dict)

        self._loop.run_until_complete(_watch_for_events())

        # self._conns[path] = connectWS(factory, context_factory)
        return path

    def start_kline_socket(self, symbol, interval=Client.KLINE_INTERVAL_1MINUTE):
        self._logger('watch_candlesticks').info('{symbol} {interval}')

        socket_name = '{}@kline_{}'.format(symbol.lower(), interval)
        return self._start_socket(socket_name)
