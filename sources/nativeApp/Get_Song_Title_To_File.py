#!/usr/bin/env python

import sys
import json
import struct
import os
import sys


try:
    # Python 3.x version
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.buffer.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent).encode('utf-8')
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.buffer.write(encodedMessage['length'])
        sys.stdout.buffer.write(encodedMessage['content'])
        sys.stdout.buffer.flush()
        
    # Write message to file
    def writeMessage(message):
        path  = os.path.dirname(os.path.realpath(sys.argv[0])) + "\currentSong.txt"
        file = open(path, "w+")
        file.write(message)
        sendMessage(encodeMessage("writed 3 " + message))
        file.close()

    while True:
        receivedMessage = getMessage()
        writeMessage(receivedMessage)           
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
        encodedContent = json.dumps(messageContent)
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.write(encodedMessage['length'])
        sys.stdout.write(encodedMessage['content'])
        sys.stdout.flush()
        
    # Write message to file
    def writeMessage(message):
        path  = os.path.dirname(os.path.realpath(sys.argv[0])) + "\currentSong.txt"
        file = open(path, "w+")
        file.write(message)
        sendMessage(encodeMessage("writed 2 " + message))
        file.close()

    while True:
        receivedMessage = getMessage()
        writeMessage(receivedMessage)           
            
