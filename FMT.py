# i just use this script to mess around and do data analysis on a corpus of the entire unpacked game

from cgi import test
import os
import sys
from collections import defaultdict, Counter

from numpy import byte
from sortedcollections import SortedList
toRead = ['C:\\games\\LEGO Star Wars - The Skywalker Saga']
fileList = list()
byteList = dict()

testList = dict()

for a in range(5):
  byteList[a] = defaultdict(int)

analysis = SortedList()
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
  data = input.read(512)
  counter+=1
  if counter % 10000 == 1:
    print('*',end="", flush=True)

  # location = data.find(bytes.fromhex("52 4D 53"))
  # if location != -1:
  #   input.close()
  #   continue

  # location = data.find(bytes.fromhex("46 52 53 54"))
  # if location == -1:
  #   input.close()
  #   continue

  # location = data.find(bytes.fromhex("4C 41 53 54"))
  # if location == -1:
  #   input.close()
  #   continue

  # SEEK
  location = data.find(bytes.fromhex('53 45 45 4B'))
  if location == -1:
    input.close()
    continue

  watchValue = int.from_bytes(data[0x18:0x1C], 'little')
  if watchValue not in testList:
    testList[watchValue]  = defaultdict(int)
  
  # just_filename = os.path.basename(f)
  # just_filename = just_filename.split('_')[0]
  # testList[watchValue][just_filename] += 1

  testList[watchValue][os.path.getsize(f) // 10000] += 1
  
  # 4097 from front
  # 4097 from front + offset (0x23)
  # 4097 from back
  # 4097 from back - offset
  # 1028 from back

  # byteList[0][int.from_bytes(data[0x14:0x16], 'little')]+=1
  # byteList[1][int.from_bytes(data[0x18:0x1A], 'little')]+=1

  # first_offset=int.from_bytes(data[0x14:0x16], 'little')
  # second_offset=int.from_bytes(data[0x18:0x1A], 'little')

  # byteList[0][data[first_offset:first_offset+2]]+=1
  # byteList[1][data[first_offset + 0x23:first_offset+2 + 0x23]]+=1
  # byteList[2][data[-(first_offset+2):-(first_offset)]]+=1
  # byteList[3][data[-(first_offset+2 + 0x23):-(first_offset + 0x23)]]+=1
  # byteList[4][data[-(second_offset + 8):-(second_offset)]]+=1

  # if data[-(second_offset + 8):-(second_offset+4)] != b'LAST':
  #   print("ZZZ", f)

  # location = data.find(bytes.fromhex("5345454B"))
  # if location == -1:
  #   input.close()
  #   continue
  #   location = data.find(bytes.fromhex("524D53"))
  # if location != -1:
  #   byteList.append(data[:location])

  # if data[24] == 216:
  #   print(f)

  # byteList[0][data[12:]]+=1

  
  # print(str(data[32:34]))
  input.close()
print()
# for x in range(5):
#   print("=====", x)
#   for k, v in byteList[x].items():
#     # if len(byteList[x]) > 1:
#     print(k, v)
# print("min", analysis[0])
# print("max", analysis[-1])
# print("len", len(analysis))
# print("avg", sum(analysis) / len(analysis))

# Elements_with_frequency = Counter(analysis)
# print("mode", Elements_with_frequency.most_common(10))

for k,v in sorted(testList.items()):
  print(k, sorted(v.items())[-10:])
  sum = 0
  num = 0
  for l, w in v.items():
    sum += l * w
    num += w
  # print(sum / num )
