# OGG-FMT-HEADER

[Releases](https://github.com/bearsdotzone/tss-audio-data/releases/latest)

Demonstration

![Demonstration](assets/demonstration.mp4)

## Simple Usage

Download the release package and extract it.

Drag and drop an ogg vorbis file onto the ogg-fmt-header executable in the extracted files.

This will create a .AUDIO_DATA file in the same folder as the original ogg file.

## Advanced Usage

Download the release package and extract it.

Run the ogg-fmt-header executable with the following flags

```
usage: ogg-fmt-header.py [-h] [-o OUTPUTFILE] [-d] inputfile

positional arguments:
  inputfile

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUTFILE, --outputfile OUTPUTFILE
  -d, --debug
```

## Python Usage

ogg-fmt-header.py has no dependencies, simply run it with the aforementioned flags

## Other Info

Package built with pyinstaller