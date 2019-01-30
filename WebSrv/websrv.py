""" HTTP Server for agent posts """

import SimpleHTTPServer
import SocketServer
import threading
import logging
import json
import urlparse
from ei.test.StringMatchers import StringCollator, MatchesPattern, ContainsStringsInOrder, assert_eventually
from ei.test.HttpServerMatchers import MessageCollator, assert_message_eventually
from ei.test.HttpServerMatchers import MatchesJSONExactly, MatchesJSONPartially
from ei.test.HttpServerMatchers import MatchesFormUrlEncodedExactly, MatchesFormUrlEncodedPartially
from hamcrest import contains_string, is_

logger = logging.getLogger(__name__)

HttpServerPort = 25504


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ Handler for post requests """
    postedMessages = ""
    postedJsonMessages = []
    postedFormUrlEncodedMessages = []
    postedPlainTextMessages = []
    messageLock = threading.Lock()
    customHandlers = {}

    # Override library logging
    def _log_message(self, format, *args):
        return ("%s: %s" % (self.client_address[0], format % args))

    def log_error(self, format, *args):
        logger.error(self._log_message(format, *args))

    def log_message(self, format, *args):
        logger.debug(self._log_message(format, *args))

    def do_GET(self):
        with ServerHandler.messageLock:
            logger.debug("Received get: %s", self.path)
            ServerHandler.postedMessages += "GET"

        try:
            handler = self.customHandlers[self.path]
            handler(self)
            return
        except KeyError:
            pass

        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        """ POST message handler """
        contentLength = int(self.headers.getheader('content-length'))
        request = ''
        if contentLength:
            readCount = contentLength
            while len(request) < contentLength:
                newData = self.rfile.read(readCount)
                readCount -= len(newData)
                request += newData

        response_status = 200
        with ServerHandler.messageLock:
            content_type = self.headers.getheader('content-type')
            logger.debug(
                'Received content-type: %s; data: %s',
                content_type,
                request)
            ServerHandler.postedMessages += request
            if content_type.startswith('application/json'):
                try:
                    self.postedJsonMessages.append(json.loads(request))
                except:
                    response_status = 400
                    logger.debug("Failed to parse json string %s", request)
            elif content_type.startswith('application/x-www-form-urlencoded'):
                try:
                    self.postedFormUrlEncodedMessages.append(
                        urlparse.parse_qs(request))
                except:
                    response_status = 400
                    logger.debug(
                        "Failed to parse x-www-form-urlencoded string %s",
                        request)
            elif content_type.startswith("text/plain"):
                self.postedPlainTextMessages.append(request)

        try:
            handler = self.customHandlers[self.path]
            handler(self)
            return
        except KeyError:
            pass

        self.send_response(response_status, "Agent Received " + request)
        self.end_headers()

    @classmethod
    def getPostedMessages(cls):
        """ get body of received POST """
        with cls.messageLock:
            postedMessages = cls.postedMessages
            cls.postedMessages = ""
        return postedMessages

    @classmethod
    def getPostedJsonMessages(cls):
        """ get body of received application/json POSTs """
        with cls.messageLock:
            postedJsonMessages = cls.postedJsonMessages
            cls.postedJsonMessages = []
        return postedJsonMessages

    @classmethod
    def getPostedFormUrlEncodedMessages(cls):
        """ get body of received application/x-www-form-urlencoded POSTs """
        with cls.messageLock:
            postedFormUrlEncodedMessages = cls.postedFormUrlEncodedMessages
            cls.postedFormUrlEncodedMessages = []
        return postedFormUrlEncodedMessages

    @classmethod
    def getPostedPlainTextMessages(cls):
        """ get body of received text/plain POSTs """
        with cls.messageLock:
            postedPlainTextMessages = cls.postedPlainTextMessages
            cls.postedPlainTextMessages = []
        return postedPlainTextMessages


class HttpServer():
    """ HTTP Server for agents / webhooks to talk to """

    def __init__(self, port=HttpServerPort):
        self.serverthread = None
        self.port = port
        SocketServer.TCPServer.allow_reuse_address = True
        ServerHandler.postedMessages = ""
        self.server = SocketServer.TCPServer(("", self.port), ServerHandler)
        self.agentMessages = StringCollator(ServerHandler.getPostedMessages)
        self.jsonMessages = MessageCollator(
            ServerHandler.getPostedJsonMessages)
        self.formUrlEncodedMessages = MessageCollator(
            ServerHandler.getPostedFormUrlEncodedMessages)
        self.plainTextMessages = MessageCollator(
            ServerHandler.getPostedPlainTextMessages)
        self.serverthread = threading.Thread(target=self.server.serve_forever)
        self.serverthread.daemon = True
        self.serverthread.name = "HttpServer"
        self.serverthread.start()

    def stop(self):
        """ stop the server """
        if self.serverthread:
            if self.serverthread.isAlive():
                self.server.shutdown()
                self.server.server_close()
                self.serverthread.join()

    def add_handler(self, path, handler):
        ServerHandler.customHandlers[path] = handler

    def reset(self):
        """ Set up by collating HTTP server messages """
        self.agentMessages = StringCollator(ServerHandler.getPostedMessages)
        self.jsonMessages = MessageCollator(
            ServerHandler.getPostedJsonMessages)
        self.formUrlEncodedMessages = MessageCollator(
            ServerHandler.getPostedFormUrlEncodedMessages)

    def get_url(self, path="/"):
        return "http://localhost:%d%s" % (self.port, path)

    def has_received_message(self, msg, timeout=60, poll=0.1):
        assert_eventually(
            self.agentMessages.getString,
            contains_string(
                msg),
            "Expected agent to have received %s" %
            msg,
            timeout,
            poll)

    def has_received_messages(self, messages, timeout=60, poll=0.1):
        """ Has the HTTP server received the messages """
        assert_eventually(self.agentMessages.getString,
                          ContainsStringsInOrder(messages), 'Failed to find agent messages', timeout, poll)

    def has_received_message_matching(self, pattern, timeout=60, poll=0.1):
        """ Has the HTTP server received a matching pattern """
        assert_eventually(self.agentMessages.getString,
                          MatchesPattern(pattern), 'Failed to match agent messages', timeout, poll)

    def has_received_json_matching(self, obj, timeout=60, poll=0.1):
        """ Has the HTTP server received a matching pattern """
        assert_message_eventually(self.jsonMessages.getObjects,
                                  MatchesJSONExactly(obj), 'Failed to match json messages', timeout, poll)

    def has_received_json_partially_matching(
            self, obj, timeout=60, poll=0.1):
        """ Has the HTTP server received a matching pattern """
        assert_message_eventually(self.jsonMessages.getObjects,
                                  MatchesJSONPartially(obj), 'Failed to match json messages', timeout, poll)

    def has_received_form_urlencoded_matching(
            self, obj, timeout=60, poll=0.1):
        """ Has the HTTP server received a matching pattern """
        assert_message_eventually(self.formUrlEncodedMessages.getObjects,
                                  MatchesFormUrlEncodedExactly(obj), 'Failed to match form-urlencoded messages',
                                  timeout, poll)

    def has_received_post_plain_text_matching(self, text, timeout=60, poll=0.1):
        assert_message_eventually(self.plainTextMessages.getObjects,
                                  is_(text), 'Failed to match text/plain messages', timeout, poll)

    def has_received_form_urlencoded_partially_matching(
            self, obj, timeout=60, poll=0.1):
        """ Has the HTTP server received a matching pattern """
        assert_message_eventually(self.formUrlEncodedMessages.getObjects,
                                  MatchesFormUrlEncodedPartially(obj), 'Failed to match form-urlencoded messages',
                                  timeout, poll)

    def __del__(self):
        self.stop()
