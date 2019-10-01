# -*- coding: utf-8 -*-
# Copyright (c) 2011 Erik Svensson <erik.public@gmail.com>
# Licensed under the MIT license.

import ctypes
from .system import ARCHITECTURE_BITS

library = 'IBFS64.DLL' if ARCHITECTURE_BITS == 64 else 'IBFS32.DLL'

try:
    dll = ctypes.windll.LoadLibrary(library)
except:
    raise Exception('Library '{}' not found'.format(library))


class TMEXException(Exception):
    pass


PortTypes = {
    1: 'Older DS9097E-type serial port adapter',
    2: 'Parallel port adapter',
    5: 'Standard DS90907U-type serial port adapter',
    6: 'USB port adapter',
}

###### Sections and definitions taken from https://files.maximintegrated.com/sia_bu/softdev/owdocs/Docs/TMEX/tmex3vlg.html


###### API: Session ######
TMSessionMessages = {
    0: 'Session is invalid',
    1: 'Session is valid',
    -200: 'Session is invalid',
    -201: 'Required hardware driver not found',
}

TMExtendedStartSession = dll.TMExtendedStartSession
TMExtendedStartSession.argtypes = [ctypes.c_short, ctypes.c_short, ctypes.c_void_p]
TMExtendedStartSession.restype = ctypes.c_long
TMExtendedStartSessionMessages = {
	**TMSessionMessages,
    0: 'Port not available, it is being used by another application',
}

TMValidSession = dll.TMValidSession
TMValidSession.argtypes = [ctypes.c_long]
TMValidSession.restype = ctypes.c_short
TMValidSessionMessages = {
	**TMSessionMessages,
    0: 'Session_handle is no longer valid',
    1: 'Session_handle is still valid for port',
}

TMEndSession = dll.TMEndSession
TMEndSession.argtypes = [ctypes.c_long]
TMEndSession.restype = ctypes.c_short
TMEndSessionMessages = {
	**TMSessionMessages,
    0: 'Session_handle already invalid',
    1: 'Session ended, session_handle no longer valid',
}


###### API: File Operations ######
class TMFamilySpec(ctypes.Structure):
    _fields_ = [('features', ctypes.c_ushort * 32), ('description', ctypes.c_char * 255)]

TMGetFamilySpec = dll.TMGetFamilySpec
TMGetFamilySpec.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.POINTER(TMFamilySpec)]
TMGetFamilySpec.restype = ctypes.c_short
TMGetFamilySpecMessages = {
    0: 'A FILE_OPERATIONS error has occured',
    1: 'Device family information is in buffer "FamSpec"',
}


###### API: Transport ######
TMTransportMessages = {
    -1: '1-Wire network not initialized with TMSetup',
    -2: 'Specified 1-Wire network nonexistent',
    -3: 'Function not supported',
    -4: 'Error reading or writing package',
    -5: 'Packet larger than provided buffer',
    -6: 'Not enough room for packet on device',
    -7: 'No device found',
    -8: 'Block transfer too long',
    -9: 'Wrong type of device for this function',
    -10: 'The page being read is redirected',
    -11: 'The device is written in a way that can not be changed',
    -200: 'Session not valid',
    -201: 'Hardware_Specific driver not found and is required',
}

TMCRC = dll.TMCRC
TMCRC.argtypes = [ctypes.c_short, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ushort, ctypes.c_short]
TMCRC.restype = ctypes.c_short
TMCRCMessages = {
    **TMTransportMessages
}


###### API: Network ######
TMNetworkMessages = {
    -1: 'Specified 1-Wire network has not been initialized with a call to the TMSetup function.',
    -2: 'Specified 1-Wire network nonexistent',
    -3: 'Function not supported',
    -200: 'Session not valid',
    -201: 'Hardware_Specific driver not found and is required',
}

TMFirst = dll.TMFirst
TMFirst.argtypes = [ctypes.c_long, ctypes.c_char_p]
TMFirst.restype = ctypes.c_short
TMFirstMessages = {
    **TMNetworkMessages,
    0: 'Device not found',
    1: 'First device on the 1-Wire network found',
}

TMNext = dll.TMNext
TMNext.argtypes = [ctypes.c_long, ctypes.c_char_p]
TMNext.restype = ctypes.c_short
TMNextMessages = {
    **TMNetworkMessages,
    0: 'Device not found',
    1: 'Next device on the 1-Wire network found',
}

TMRom = dll.TMRom
TMRom.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.POINTER(ctypes.c_short)]
TMRom.restype = ctypes.c_short
TMRomMessages = {
    **TMNetworkMessages,
    1: 'ROM read or set',
}

TMAccess = dll.TMAccess
TMAccess.argtypes = [ctypes.c_long, ctypes.c_char_p]
TMAccess.restype = ctypes.c_short
TMAccessMessages = {
    **TMNetworkMessages,
    0: 'No presence on 1-Wire network',
    1: 'Presence on 1-Wire network and ROM selected',
}

TMStrongAccess = dll.TMStrongAccess
TMStrongAccess.argtypes = [ctypes.c_long, ctypes.c_char_p]
TMStrongAccess.restype = ctypes.c_short
TMStrongAccessMessages = {
    **TMNetworkMessages,
    0: 'Device in ROM buffer not on 1-Wire network',
    1: 'Device in ROM buffer on 1-Wire network and it is selected',
}


###### API: Hardware Specific ######
TMHardwareSpecificMessages = {
    -1: 'Specified 1-Wire network has not been initialized with a call to the TMSetup function.',
    -2: 'Specified 1-Wire network nonexistent',
    -3: 'Function not supported',
    -12: 'Failure to communicate with hardware adapter',
    -13: 'An unsolicited event occured on the 1-Wire',
    -200: 'Session not valid',
    -201: 'Hardware_Specific driver not found and is required',
}

TMReadDefaultPort = dll.TMReadDefaultPort
TMReadDefaultPort.argtypes = [ctypes.POINTER(ctypes.c_short), ctypes.POINTER(ctypes.c_short)]
TMReadDefaultPort.restype = ctypes.c_short
TMReadDefaultPortMessages = {
    1: 'Defaults were returned',
    -2: 'Defaults not found',
}  # Does not use any TMHardwareSpecificMessages

TMSetup = dll.TMSetup
TMSetup.argtypes = [ctypes.c_long]
TMSetup.restype = ctypes.c_short
TMSetupMessages = {
    **TMHardwareSpecificMessages,
    0: 'Setup failed',
    1: 'Setup ok',
    2: 'Setup ok but 1-Wire network shorted',
    3: '1-Wire network does not exist',
    4: 'TMSetup not supported',
}

TMBlockStream = dll.TMBlockStream
TMBlockStream.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_short]
TMBlockStream.restype = ctypes.c_short
TMBlockStreamMessages = {
    **TMHardwareSpecificMessages,
    0: 'No bytes sent or received.'
}

TMTouchReset = dll.TMTouchReset
TMTouchReset.argtypes = [ctypes.c_long]
TMTouchReset.restype = ctypes.c_short
TMTouchResetMessages = {
	**TMHardwareSpecificMessages,
    0: 'No presence pulse detected',
    1: 'Non-alarming presence pulse detected',
    2: 'Alarming presence pulse detected',
    3: '1-Wire network shorted',
    5: 'TMTouchReset not supported',
}

TMTouchByte = dll.TMTouchByte
TMTouchByte.argtypes = [ctypes.c_long, ctypes.c_short]
TMTouchByte.restype = ctypes.c_short
TMTouchByteMessages = {
	**TMHardwareSpecificMessages,
    255: '1-Wire network shorted',
}

TMOneWireLevel = dll.TMOneWireLevel
TMOneWireLevel.argtypes = [ctypes.c_long, ctypes.c_short, ctypes.c_short, ctypes.c_short]
TMOneWireLevel.restype = ctypes.c_short
TMOneWireLevelMessages = {
	**TMHardwareSpecificMessages,
}
