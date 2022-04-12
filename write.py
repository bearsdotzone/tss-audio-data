# Transforms the in OGG into an out.AUDIO_DATA. Embarrasingly manual at the moment.

f = open("VO_YODA_DEATH_01.AUDIO_DATA", "w+b")
i = open("in-yoda.ogg", "r+b")

rateHZ = 32000
numSamples = 52355
numTracks = 1

granules = [0, 11648, 27200, 45632, 52355]
granuleSum = 0
pages = [0x3a, 0xE9D, 0x1EF6, 0x2FC1, 0x40B7]

numPages = len(pages)
inLength = 16622

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

for p in range(numPages):
    f.write(pages[p].to_bytes(4, 'little'))
    f.write((granules[p] - granuleSum).to_bytes(4, 'little'))
    granuleSum = granules[p]


# data
f.write(bytes.fromhex("44 41 54 41"))

# length of ogg file
f.write(inLength.to_bytes(4, 'little'))

f.write(i.read())

f.close()
i.close()