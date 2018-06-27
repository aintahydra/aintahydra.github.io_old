#!/bin/python
# Modified by aintahydra _at_ gmail _dot_ com , based on the code snippet appeared in "A Practical Guide to TPM 2.0". 
import os
import sys
import socket
from socket import socket, AF_INET, SOCK_STREAM

platformSock = socket(AF_INET, SOCK_STREAM)
#platformSock.connect(('localhost', 2324)
platformSock.connect(('localhost', 2322)) # ibm's SW TPM

# Power on the TPM
platformSock.send('\0\0\0\1')

cmdSock = socket(AF_INET, SOCK_STREAM)
#tpmSock.connect(('localhost', 2323))
cmdSock.connect(('localhost', 2321)) # ibm's SW TPM

# TPM_SEND_COMMAND : defined at the tpm service - (See the **Note below)
cmdSock.send('\x00\x00\x00\x08')

# 1. BYTE Locality
cmdSock.send('\x03')

# 2. UINT32 InBufferSize
# Send # of bytes : 12 bytes (The size of the following commands - 2 + 4 + 4 + 2)
cmdSock.send('\x00\x00\x00\x0c')

# 3. Start of : BYTE[InBufferSize] InBuffer - (See the **Note2 below)

# TPM_ST (Structure Tags)
# TPM2_ST_NO_SESSIONS : (UINT16)(0x8001) - Table 19 @ TPM 2.0 Part 2 v01.38
# command/response has no attached sessions
#   and no authorizationSize/parameterSize value is present
cmdSock.send('\x80\x01')

# Command Size
cmdSock.send('\x00\x00\x00\x0c')

# TPM2_CC_Startup : (UINT32)(0x00000144) - Table 12 @ TPM 2.0 Part 2 v01.38
cmdSock.send('\x00\x00\x01\x44')

# TPM_SU (Startup Type)
# TPM_SU_CLEAR : (UINT16) 0x0000 - Table 20 @ TPM 2.0 Part 2 v01.38
cmdSock.send('\x00\x00')

# 3. End of : BYTE[InBufferSize] InBuffer

# Receive the size of the response, the response, and 4 bytes of 0's
outBuffer = cmdSock.recv(18)
print " ".join("{:02x}".format(ord(c)) for c in outBuffer)

