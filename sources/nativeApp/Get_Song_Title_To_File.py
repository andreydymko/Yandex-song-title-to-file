#!/usr/bin/env python

import sys
import json
import struct
import os
import sys
import logging
import unicodedata

logging.basicConfig(filename=os.path.dirname(os.path.realpath(sys.argv[0])) + "\latest_error.txt",
                    level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)

try:
    # Python 3.x version
    # Read a message from stdin and decode it.
    def getMessage():
        try:
            rawLength = sys.stdin.buffer.read(4)
            if len(rawLength) == 0:
                return json.loads('null')
                #sys.exit(0)
            messageLength = struct.unpack('@I', rawLength)[0]
            message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        except Exception as e:
            logger.error(e)
            message = 'error'
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        try:
            encodedContent = json.dumps(messageContent).encode('utf-8')
            encodedLength = struct.pack('@I', len(encodedContent))
        except Exception as e:
            logger.error(e)
            encodedContent = json.dumps("Error encoding symbol.").encode('utf-8')
            encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        try:
            sys.stdout.buffer.write(encodedMessage['length'])
            sys.stdout.buffer.write(encodedMessage['content'])
            sys.stdout.buffer.flush()
        except Exception as e:
            logger.error(e)

    # Write message to file
    def writeMessage(message):
        try:
            path = os.path.dirname(os.path.realpath(sys.argv[0])) + "\currentSong.txt"
            file = open(path, "w+")
            file.write(message)
            sendMessage(encodeMessage("written 3 " + message))
            file.close()
        except Exception as e:
            logger.error(e)

    while True:
        receivedMessage = getMessage()
        writeMessage(unicodedata.normalize('NFKD', receivedMessage))
except AttributeError:
    # Python 2.x version (if sys.stdin.buffer is not defined)
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.read(messageLength)
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        try:
            encodedContent = json.dumps(messageContent).encode('utf-8')
            encodedLength = struct.pack('@I', len(encodedContent))
        except UnicodeError as e:
            encodedContent = json.dumps("Error encoding symbol.").encode('utf-8')
            encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.write(encodedMessage['length'])
        sys.stdout.write(encodedMessage['content'])
        sys.stdout.flush()

    # Write message to file
    def writeMessage(message):
        path = os.path.dirname(os.path.realpath(sys.argv[0])) + "\currentSong.txt"
        file = open(path, "w+")
        file.write(message)
        sendMessage(encodeMessage("writed 2 " + message))
        file.close()

    while True:
        receivedMessage = getMessage()
        writeMessage(receivedMessage)