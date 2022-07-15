import struct

def floatToRegister(val):
    buf = struct.pack('f',float(val))
    return [(buf[1]<<8)+buf[0],(buf[3]<<8)+buf[2]]
    # return [(buf[0]<<8)+buf[1],(buf[2]<<8)+buf[3]]
    # return [(buf[2]<<8)+buf[3],(buf[0]<<8)+buf[1]]
    # return [(buf[3]<<8)+buf[2],(buf[1]<<8)+buf[0]]

def registerToFloat(reg):
    buf = bytes([reg[0]>>8,reg[0]&0xff,reg[1]>>8,reg[1]&0xff])
    # buf = bytes([reg[0]&0xff,reg[0]>>8,reg[1]&0xff,reg[1]>>8])
    # buf = bytes([reg[1]>>8,reg[1]&0xff,reg[0]>>8,reg[0]&0xff])
    # buf = bytes([reg[1]&0xff,reg[1]>>8,reg[0]&0xff,reg[0]>>8])
    return struct.unpack('f',buf)[0]

def bytesToFloat(reg):
    # buf = bytes([reg[0],reg[1],reg[2],reg[3]])
    buf = bytes([reg[1],reg[0],reg[3],reg[2]])
    # buf = bytes([reg[2],reg[3],reg[0],reg[1]])
    # buf = bytes([reg[3],reg[2],reg[1],reg[0]])
    return struct.unpack('f',buf)[0]