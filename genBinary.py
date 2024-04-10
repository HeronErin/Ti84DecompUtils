import struct

deviceTypeLookup = {
    0x74: "TI73",
    0x73: "TI83+",
    0x98: "TI89",
    0x88: "TI92+"
}
dataTypeLookup = {
    0x23: "os",
    0x24: "application",
    0x25: "certificate",
    0x3E: "license",
}

# https://merthsoft.com/linkguide/ti83+/fformat.html
def decode8XK(file):
    f = open(file, "rb")

    if b'**TIFL**' != f.read(8):
        raise ValueError("Invalid file format (Magic number invalid)")
    version = [f.read(1)[0], f.read(1)[0]]
    flags = f.read(1)[0]
    objType = f.read(1)[0]
    
    if objType != 0x88:
        raise ValueError("Invalid file format (invalid object type)")
    date = f.read(4)
    nameLen = f.read(1)[0]
    name = str(f.read(nameLen))
    
    trashData = f.read(23)
    deviceTypeByte = f.read(1)[0]

    if not deviceTypeByte in deviceTypeLookup:
        raise ValueError("Invalid file format (unexpected device type)")
    deviceType = deviceTypeLookup[deviceTypeByte]

    dataTypeByte = f.read(1)[0]
    if not dataTypeByte in dataTypeLookup:
        raise ValueError("Invalid file format (unexpected data type)")
    dataType = dataTypeLookup[dataTypeByte]
    
    moreTrashData = f.read(24)

    sizeOfByteData = struct.unpack("<I", f.read(4))[0]
    intelHex = f.read(sizeOfByteData )
    
    checkSumBytes = f.read()
    if len(checkSumBytes) != 2:
        raise ValueError("Invalid file format (Length apears to be incorrect)")
    checkSum = struct.unpack("<H", checkSumBytes)[0]

    f.close()

    return {
        "version": version,
        "flags": flags,
        "date": date,
        "name": name,
        "deviceType": deviceType,
        "dataType": dataType,
        "checkSum": checkSum,
        "intelHex": intelHex
    }
def handlePages(intelHex):
    pages = []
    for line in intelHex.split(b"\r\n"):
        print(line[1+2:])



decoded = decode8XK("PlySmlt2.8xk")
handlePages(decoded["intelHex"])
