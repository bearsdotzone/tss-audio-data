# tss-audio-data
Reverse engineering the .AUDIO_DATA files for Lego Star Wars The Skywalker Saga.

## Tools

[Ogg-FMT-Header Instructions](tools/ogg-fmt-header/)
 - Converts OGG to AUDIO_DATA

## Technical

### OGG

This section assumes a passing familiarity with the OGG spec.

[In game example, replacing a Bib Fortuna voice line](https://youtu.be/uS7JjUNHu5I)

[Implementation example in ogg-fmt-header](tools/ogg-fmt-header/ogg-fmt-header.py)

#### FMT Header
```c
       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  0123456789ABCDEF
0000h: 46 4D 54 20 14 00 00 00 00 00 01 00 00 7D 00 00  FMT .........}.. 
0010h: B0 B0 00 00 01 20 00 00 78 24 03 00 53 45 45 4B  °°... ..x$..SEEK
```
The predominant header starts `46 4D 54 20 14` or `FMT2014` followed by `00 00 00 00 00 01 00`. Of the 130,000 audio data files, 110,000 have this header. 20,000 have `46 4D 54 20 13` and 6 have `46 4D 54 20 10`. In both of these cases, `0A` is 0.

From `0C`-`0F` is a little endian integer representing the sample rate.
Of the 130,000 audio data files, 110,000 are 32000hz. 20,000 are 24,000hz, 5,000 are 44,100hz, and 2 are 6,000hz.

From `10`-`13` is a little endian integer representing the number of samples.

`14` is the number of tracks. `15`-`17` appear to be packing against the track value.

`18`-`1B` is currently unknown. Across the files there are ten different formats, `78 24 03 00` is overwhelmingly the most common.

#### SEEK Header
```c
       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  0123456789ABCDEF
0010h: B0 B0 00 00 01 20 00 00 78 24 03 00 53 45 45 4B  °°... ..x$..SEEK 
0020h: 20 00 00 00 00 00 00 00 00 00 00 00 3A 00 00 00   ...........:... 
0030h: 00 00 00 00 18 0D 00 00 40 7D 00 00 D0 2D 00 00  ........@}..Ð-.. 
0040h: 70 33 00 00 44 41 54 41 E8 73 00 00 4F 67 67 53  p3..DATAès..OggS 
```
FMT rolls directly in to the SEEK header. This header describes the pages of the forthcoming OGG file.
Immediately following `SEEK` is an integer decribing how long the seek block is. This should be the number of pages in your OGG file plus one, and then multipled by eight.

After 8 empty bytes, which are likely the zeroeth page, we get into the meat of the SEEK block, a repeating pattern of two integers. The first integer is the address at which an OGG page starts. NB: This address is in reference to the OGG data minus any SEEK/FMT/DATA headers. Thus the first page's address should always be 3A.
The second integer is a delta between the granule of the earlier page and the current page. While an OGG file stores the granules as a sum, the SEEK header stores the difference.

010 editor is helpful for this until we can get an automated tool up and running.
![010 editor](images/granule.png)

#### DATA Header
```c
       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  0123456789ABCDEF
0040h: 70 33 00 00 44 41 54 41 E8 73 00 00 4F 67 67 53  p3..DATAès..OggS
```
This one's real simple and comes right after the end of SEEK. Simply put `DATA` and then an integer that is the length of the OGG file.

Immediately after this the OGG file begins in earnest with its header info.

### FRST
Theses files tend to be shorter, death sound effects and such. But not the sound effects in the SOUNDFX folder, those are just WAVs. This format is not fully understood yet.
```c
       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  0123456789ABCDEF
0000h: 46 4D 54 20 13 00 00 00 00 00 0A 00 C0 5D 00 00  FMT ........À].. 
0010h: 2B 3E 00 00 01 10 00 00 04 04 01 44 41 54 41 30  +>.........DATA0 
0020h: 20 00 00 46 52 53 54 00 00 00 00 02 00 00 00 EB   ..FRST........ë 
```
0x00 - 0x0B is static.

0x0C - 0x0F is the sample rate.
0x10 - 0x13 is the number of samples.

0x14 as a short is in some way meaningful. It is 4097 across all the files, I believe this points to a memory address 4097 bytes before the end of the file. I assume that address has something to do with samples remaining.

0x18 as a short is also meaningful. It is 1028 which when we go back 1028 from the end of the file we see the message LAST and then four bytes which I think also represents samples remaining.

0x1B says DATA then 0x1F is an int representing the remaining file size.

Then at 0x23 we get the FRST header. After that I don't know. It appears to be some sort of wav, consistent with the SOUNDFX files.

VO_YODA_DEATH_01 kinda works? I exported from audacity as microsoft acpdm because that's what the other WAVs appear to be but it doesn't *look* like the original so it's probably wrong in some way. But then again the SOUNDFX files don't look like the FRST files either? Would they use two different types of WAV encoding for two types of sounds?

TT also may have measured 4097 from the front and 1028 from the back which seems psychopathic. It seems important that these numbers are real close to powers of 2 but I don't know how. I wonder then if that is affected by the 35 offset. Yui suggested that some of the files are IMA ADPCM so I'll mess around with that.

Even very large FRST files only point to 1028 and 4097.

Rather than samples remaining it could be a summation thing. The tricky thing is measuring 4097, 1028 seems pretty clear. In the game files it's a little unclear if it *is* samples remaining because the numbers don't line up great for that. A WAV should theoretically be two samples per byte and they can average out to that but I don't understand how the values are decided in the real files.
