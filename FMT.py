# i just use this script to mess around and do data analysis on a corpus of the entire unpacked game

import os
import sys
from collections import defaultdict
toRead = ['C:\\Program Files (x86)\\Steam\\steamapps\\common\\LEGO Star Wars - The Skywalker Saga']
fileList = list()
byteList = dict()

for i in range(32):
  byteList[hex(i)] = defaultdict(int)
max = 0
while toRead:
  files = os.scandir(toRead.pop(0))
  for f in files:
    if f.is_dir():
      toRead.append(f.path)
    else:
      if "AUDIO_DATA" in f.name:
        fileList.append(f.path)
for f in fileList:
  input = open(f, "r+b")
  data = input.read(32)
  location = data.find(bytes.fromhex("5345454B"))
  if location != -1:
    continue
  #   location = data.find(bytes.fromhex("524D53"))
  # if location != -1:
  #   byteList.append(data[:location])

  # if data[24] == 216:
  #   print(f)

  for b in range(8):
    byteList[hex(b*4)][str(data[b*4:b*4+4])]+=1
  input.close()
for x in byteList:
  # if len(byteList[x]) > 1:
  print(x, byteList[x])



