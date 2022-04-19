# Transforms the in OGG into an out.AUDIO_DATA. Embarrasingly manual at the moment.

import argparse
import os
import sys

# Return every location in the input where OggS occurs
def find_headers(byte_list):
    to_return = []
    for i in range(len(byte_list)-3):
        if (byte_list[i:i+4] == b'OggS'):
            to_return += [i]
    return to_return

def get_granule(byte_list, pos):
    granule = byte_list[pos+6:pos+14]
    granule_val = int.from_bytes(granule, "little")
    assert(granule_val > -1)
    # The largest audio file in the game is just short of 18 million samples
    return granule_val

def get_tracks(byte_list):
    tracks_val = byte_list[0x27]
    assert(tracks_val > 0)
    # I'm not confident what the max amount of tracks would be
    return tracks_val

def get_sample_rate(byte_list):
    sample_val = int.from_bytes(byte_list[0x28:0x2B], "little")
    assert(sample_val > 0)
    # I don't know the limits of what sample rates the engine supports
    return sample_val

def write_formatted(out_file, byte_list, header_list, granule_count, tracks_count, rate_count):
    f = open(out_file, "w+b")
    # FMT2014
    f.write(bytes.fromhex("46 4D 54 20 14 00 00 00 00 00 01 00"))
    # Write the sample rate
    f.write(rate_count.to_bytes(4, 'little'))
    # Write the number of samples
    f.write(granule_count.to_bytes(4, 'little'))
    # Write the number of tracks
    f.write(tracks_count.to_bytes(1, 'little'))
    # UNKNOWN - Likely packing
    f.write(bytes.fromhex("20 00 00"))

    # UNKNOWN - I don't know what these values represent but these are the only
    # ones that exist in all the files. It seems like it may have something to
    # do with size, going to a higher value doesn't appear to break things, but
    # going to a lower value can. I'm interpreting the breakpoints here as
    # roughly a megabyte. 🤷‍♀️ The game seems to support arbitrary values too so
    # it's unclear why there exist only these 11.
    magic_list = [205944,207112,218300,219464,230656,231832,232608,243004,244184,267716,268904]
    bytes_to_write = magic_list[min(len(byte_list) // 1000000, 10)]
    f.write(bytes_to_write.to_bytes(4, 'little'))
    
    # SEEK
    f.write(bytes.fromhex("53 45 45 4B"))
    # The length of the seek section as determined by number of pages
    f.write(((len(header_list))*8).to_bytes(4, 'little'))
    # The memory location of the pages, followed by a rolling sum of the granule
    granuleSum = 0

    for memory_location in header_list:
        granule = get_granule(byte_list, memory_location)
        f.write(memory_location.to_bytes(4, 'little'))
        f.write((granule - granuleSum).to_bytes(4, 'little'))
        granuleSum = granule

    # data
    f.write(bytes.fromhex("44 41 54 41"))
    # The length of the ogg file to be added
    f.write(len(byte_list).to_bytes(4, 'little'))
    # The supplied ogg file
    f.write(byte_list)

    f.close()



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('-o', '--outputfile')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()

    if not os.path.exists(args.inputfile):
        raise FileNotFoundError(args.inputfile)

    i = open(args.inputfile, "r+b")

    byte_list = i.read()

    assert(byte_list[0x0:0x4] == b'OggS')
    assert(byte_list[0x1D:0x23] == b'vorbis')

    i.close()
    
    fn = args.inputfile + ".AUDIO_DATA"

    if args.outputfile is not None:
        if os.path.exists(args.inputfile):
            fn = args.outputfile
        else:
            raise FileNotFoundError(args.inputfile)

    header_list=find_headers(byte_list)
    granule_count=get_granule(byte_list,header_list[-1])
    tracks_count=get_tracks(byte_list)
    rate_count=get_sample_rate(byte_list)
    if args.debug:
        for x in header_list:
            print("granule {} memory {}".format(get_granule(byte_list, x), x))
        print("Num Samples / Maximum Granule:", granule_count)
        print("Tracks:", tracks_count)
        print("Sample Rate:", rate_count)

    print("{} passes checks".format(args.inputfile))

    
    write_formatted(fn, byte_list, header_list, granule_count, tracks_count, rate_count)

    print("{} written successfully".format(fn))

    print("Press any key to exit")
    for line in sys.stdin:
        sys.exit(0)
    


if __name__ == "__main__":
    main()