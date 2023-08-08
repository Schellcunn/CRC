import zlib
import glob
import time
import argparse
from pathlib import Path

def verify_crc(file_location: Path) -> None:
    targetfiles = [f for f in Path(file_location).glob("*.mkv")]
    failed: list[str] = []
    ok: list[str] = []

    for file in targetfiles:
        # Extract just the file name without the directory path
        file_name = file.name
        expected_crc = file_name[-13:-5]
        
        with open(file, 'rb') as fd:
            crc_value = zlib.crc32(b"")  # Initialize CRC32 value
            while True:
                eachLine = fd.read(8192)  # Read in chunks of 8KB (adjust as needed)
                if not eachLine:
                    break
                crc_value = zlib.crc32(eachLine, crc_value)

        # Calculate the final CRC32 checksum
        calculated_crc = "%08X" % (crc_value & 0xFFFFFFFF)
        if expected_crc.upper() == calculated_crc:
            ok.append(str(file))
        else:
            failed.append(str(file))
        

    if len(failed) > 0:
        print(f"not ok, the following file(s) had wrong checksum: {failed}")
    else:
        print("ok")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate CRC32 checksum for MKV files in a given location.")
    parser.add_argument("file_location", help="Path to the directory containing MKV files.")
    args = parser.parse_args()
    file_location = (Path(args.file_location) if not isinstance(args.file_location, Path) else args.file_location).resolve()
    if not file_location.is_dir():
        raise FileNotFoundError()
    
    # Timing to compare performance
    start_time = time.time()
    verify_crc(file_location)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

