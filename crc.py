import zlib
import glob
import time

targetfiles = [f for f in glob.glob("*.mkv")]
#print(targetfiles)

crc32_map: dict[str, str] = {}
failed: list[str] = []
ok: list[str] = []


def crc() -> None:
  """lolwat"""
  for file in targetfiles:
    crc32_map[file] = file[-13:-5]
    with open(file, 'rb') as fd: 
      eachLine = fd.readline()
      prev = None
      while eachLine:
        if not prev:
          prev = zlib.crc32(eachLine)
        else:
          prev = zlib.crc32(eachLine, prev)
        eachLine = fd.readline()   
    calculated_crc = ("%X"%(prev & 0xFFFFFFFF)) #returns 8 digits crc

    if crc32_map[file] == calculated_crc:
      ok.append(file)
      continue  
    failed.append(file)


if __name__ == "__main__":
    start_time = time.time()
    crc()
    end_time = time.time()
    if len(failed) > 0:
        print(f"not ok, the following file(s) had wrong checksum: [{failed}]")
    else:
        print("ok")

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")
        