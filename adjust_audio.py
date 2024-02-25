
import aifc
import os
import shutil
import json
from pydub import AudioSegment

with open('config.json', 'r') as f:
    config = json.load(f)

DIRECTORY = config["game_sound_directory"]
FACTOR = config["speed_factor"]

# NB, one octave (12) for every factor
if FACTOR < 1:
    KEY_ADJUSTMENT_INT = int(-12 * ((1 / FACTOR) - 1))
else:
    KEY_ADJUSTMENT_INT = int(12 * FACTOR)

if KEY_ADJUSTMENT_INT < 0:
    KEY_ADJUSTMENT_STR = str(KEY_ADJUSTMENT_INT)
else:
    KEY_ADJUSTMENT_STR = "+" + str(KEY_ADJUSTMENT_INT)


def crawl_directory(directory):
    # Iterate over all files and subdirectories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Construct the absolute path to each file
            file_path = os.path.join(root, file)
            # Print or process the file however you want
            yield file_path


def speed_s_file(path):
    processed = ""

    with open(path + ".backup", "r") as f:
        for line in f.readlines():
            new_line = line
            if "TEMPO" in line:
                start = line[:15]
                if "*" not in line:
                    print("Warning: Missing *")
                else:
                    number, end = line[15:].split("*", 1)
                    number = str(int(int(number) * FACTOR))
                    new_line = start + number + "*" + end

            if "KEYSH" in new_line:
                new_line = new_line.replace("+0", KEY_ADJUSTMENT_STR)

            processed += new_line

    with open(path, "w") as f:
        f.write(processed)


def speed_aif_file(path):
    audio = AudioSegment.from_file(path + ".backup")
    new_frame_rate = int(audio.frame_rate * FACTOR)
    adjusted_file = audio.set_frame_rate(new_frame_rate)

    # Convert audio to 8-bit
    adjusted_file = adjusted_file.set_sample_width(1)

    # Export the adjusted file
    audio_data = adjusted_file.raw_data

    # Write the AIFF file with FORM header
    with aifc.open(path + ".aiff", 'w') as f:
        f.setnchannels(adjusted_file.channels)
        f.setsampwidth(1)  # 8-bit precision
        f.setframerate(new_frame_rate)
        f.setcomptype(b'NONE', b'NONE')  # No compression
        f.writeframes(audio_data)
    os.replace(path + ".aiff", path)


if __name__ == "__main__":
    for path in crawl_directory(DIRECTORY):
        print(path)
        extension = path.lower().split(".")[-1]
        if extension == "backup":
            continue
        if extension == "":
            continue
        if extension not in ["s", "aif"]:
            continue
        if os.path.isdir(path):
            continue
        if "MPlayDef" in path:
            continue

        if not os.path.exists(path + ".backup"):
            shutil.copyfile(path, path + ".backup")

        if extension == "s":
            speed_s_file(path)
        if extension == "aif":
            speed_aif_file(path)
