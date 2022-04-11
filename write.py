# Creates the out file Day Wanna Wanga, embarrasingly manual right now but a good PoC.


f = open("out", "w+b")
i = open("in", "r+b")

rateHZ = 32000
numSamples = 45232
numTracks = 1
numPages = 3
pages = [0x0000003a, 0x7d4000000d18, 0x337000002dd0]
inLength = 29672

offset = 0x2B + 8 * numPages + 8 + 1


# FMT2014
f.write(bytes.fromhex("46 4D 54 20 14 00 00 00 00 00 01 00"))
# HZ
f.write(rateHZ.to_bytes(4, 'little'))

# SAMPLES
f.write(numSamples.to_bytes(4, 'little'))

# TRACKS
f.write(numTracks.to_bytes(1, 'little'))

# IDK
f.write(bytes.fromhex("20 00 00"))

# One of ten values, nearly always the following
f.write(bytes.fromhex("78 24 03 00"))

# SEEK
f.write(bytes.fromhex("53 45 45 4B"))

# Length of seek
f.write(((numPages+1)*8).to_bytes(4, 'little'))
f.write(bytes.fromhex("00 00 00 00 00 00 00 00"))

# Location of pages, followed by a rolling sum of the granule

for p in pages:
    f.write(p.to_bytes(8, 'little'))


# data
f.write(bytes.fromhex("44 41 54 41"))

# length of ogg file
f.write(inLength.to_bytes(4, 'little'))

f.write(i.read())

f.close()
i.close()