import sys
import os
import subprocess
import argparse
import concurrent.futures
import logging


def convert_file(input_file, output_file):
    try:
        subprocess.run(["ffmpeg", "-i", input_file, "-c:v",
                       "h264", "-c:a", "aac", output_file], check=True)
        os.remove(input_file)
        logging.info(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {input_file}: {e}")
    except FileNotFoundError:
        logging.error("ffmpeg not found. Please install ffmpeg.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert MTS files to MP4 format.")
    parser.add_argument(
        "path", help="Path to the directory containing MTS files")
    parser.add_argument(
        "--output-dir", help="Directory to store the converted MP4 files", default="./converted")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    logging.basicConfig(filename='conversion.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for root, _, files in os.walk(args.path):
                for file in files:
                    if file.endswith(".MTS"):
                        input_file = os.path.join(root, file)
                        output_file = os.path.join(
                            args.output_dir, os.path.splitext(file)[0] + ".mp4")
                        executor.submit(convert_file, input_file, output_file)
    except KeyboardInterrupt:
        logging.info("Conversion interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
