# i just use this script to mess around and do data analysis on a corpus of the entire unpacked game

import os
import sys
from collections import defaultdict
toRead = ['C:\\games\\LEGO Star Wars - The Skywalker Saga']
fileList = list()
byteList = dict()

byteList[0] = defaultdict(int)
max = 0
while toRead:
  files = os.scandir(toRead.pop(0))
  for f in files:
    if f.is_dir():
      toRead.append(f.path)
    else:
      if "AUDIO_DATA" in f.name:
        fileList.append(f.path)
counter = 0
for f in fileList:
  input = open(f, "r+b")
  if not input.readable:
    input.close()
    continue
  data = input.read(16)
  counter+=1
  # location = data.find(bytes.fromhex("5345454B"))
  # if location == -1:
  #   input.close()
  #   continue
  #   location = data.find(bytes.fromhex("524D53"))
  # if location != -1:
  #   byteList.append(data[:location])

  # if data[24] == 216:
  #   print(f)

  byteList[0][data[12:]]+=1

  if counter % 10000 == 1:
    print('*',end="")
  # print(str(data[32:34]))
  input.close()
print()
for k, v in byteList[0].items():
  # if len(byteList[x]) > 1:
  print(k.hex(), v)



