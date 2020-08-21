# -*- coding: utf-8 -*-

import abc
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from test.common.classes import TestThreaderServer

from cryptoparser.tls.record import TlsRecord
from cryptoparser.tls.subprotocol import TlsAlertDescription

from cryptolyzer.common.exception import NetworkError, NetworkErrorType
from cryptolyzer.tls.client import L7ClientTlsBase
from cryptolyzer.tls.exception import TlsAlert
from cryptolyzer.tls.server import L7ServerTls, TlsServerHandshake


class TestTlsCases:
    class TestTlsBase(unittest.TestCase):
        @staticmethod
        @abc.abstractmethod
        def get_result(host, port, protocol_version=None, timeout=None):
            raise NotImplementedError()

        @mock.patch.object(
            L7ClientTlsBase, 'do_tls_handshake',
            side_effect=NetworkError(NetworkErrorType.NO_CONNECTION)
        )
        def test_error_network_error_no_response(self, _):
            with self.assertRaises(NetworkError) as context_manager:
                self.get_result('badssl.com', 443)
            self.assertEqual(context_manager.exception.error, NetworkErrorType.NO_CONNECTION)

        @mock.patch.object(
            L7ClientTlsBase, 'do_tls_handshake',
            side_effect=TlsAlert(TlsAlertDescription.UNEXPECTED_MESSAGE)
        )
        def test_error_tls_alert(self, _):
            with self.assertRaises(TlsAlert) as context_manager:
                self.get_result('badssl.com', 443)
            self.assertEqual(context_manager.exception.description, TlsAlertDescription.UNEXPECTED_MESSAGE)


class L7ServerTlsTest(TestThreaderServer):
    def __init__(self, l7_server):
        self.l7_server = l7_server
        super(L7ServerTlsTest, self).__init__(self.l7_server)

    def run(self):
        self.l7_server.do_handshake()


class TlsServerPlainTextResponse(TlsServerHandshake):
    def _process_handshake_message(self, record, last_handshake_message_type):
        self.l4_transfer.send(
            b'<!DOCTYPE html><html><body>Typical plain text response to TLS client hello message</body></html>'
        )


class L7ServerTlsPlainTextResponse(L7ServerTls):
    @staticmethod
    def _get_handshake_class(l4_transfer):
        return TlsServerPlainTextResponse


class TlsServerAlert(TlsServerHandshake):
    def _get_alert_message(self):
        raise NotImplementedError()

    def _process_handshake_message(self, record, last_handshake_message_type):
        handshake_message = self._get_alert_message()
        self.l4_transfer.send(TlsRecord([handshake_message, handshake_message]).compose())


class L7ServerTlsAlert(L7ServerTls):
    @staticmethod
    def _get_handshake_class(l4_transfer):
        return TlsServerAlert
