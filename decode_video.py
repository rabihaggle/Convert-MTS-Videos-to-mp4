import sys
import os
import shutil
import subprocess
import argparse
import concurrent.futures
import logging


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        logging.error("ffmpeg not found. Please install ffmpeg.")
        sys.exit(1)


def get_unique_filename(output_dir, base_name):
    name, ext = os.path.splitext(base_name)
    counter = 1
    unique_name = base_name
    while os.path.exists(os.path.join(output_dir, unique_name)):
        unique_name = f"{name}_{counter}{ext}"
        counter += 1
    return unique_name


def convert_file(input_file, output_file, remove_original=True, crf=23, preset="medium"):
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_file, "-c:v", "libx264", "-preset", preset,
             "-crf", str(crf), "-c:a", "aac", "-b:a", "128k", "-y", output_file],
            check=True, capture_output=True, text=True)
        if remove_original:
            os.remove(input_file)
        logging.info(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {input_file}: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert MTS files to MP4 format.")
    parser.add_argument(
        "path", help="Path to the directory containing MTS files")
    parser.add_argument(
        "--output-dir", help="Directory to store the converted MP4 files", default="./converted")
    parser.add_argument(
        "--workers", type=int, default=2, help="Number of parallel workers (default: 2)")
    parser.add_argument(
        "--keep-original", action="store_true", help="Keep original files after conversion")
    parser.add_argument(
        "--crf", type=int, default=23, help="CRF value for video quality (0-51, lower is better)")
    parser.add_argument(
        "--preset", default="medium", choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "veryslow"], help="Encoding preset")
    parser.add_argument(
        "--formats", nargs="+", default=[".mts", ".MTS", ".m2ts", ".M2TS"], help="Input formats to process")
    args = parser.parse_args()

    check_ffmpeg()

    os.makedirs(args.output_dir, exist_ok=True)

    logging.basicConfig(
        filename='conversion.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(), logging.FileHandler('conversion.log')]
    )

    tasks = []
    for root, _, files in os.walk(args.path):
        for file in files:
            if any(file.endswith(fmt) for fmt in args.formats):
                input_file = os.path.join(root, file)
                unique_name = get_unique_filename(args.output_dir, os.path.splitext(file)[0] + ".mp4")
                output_file = os.path.join(args.output_dir, unique_name)
                tasks.append((input_file, output_file))

    if not tasks:
        logging.info("No files to convert.")
        return

    logging.info(f"Found {len(tasks)} files to convert.")

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(convert_file, inp, out, not args.keep_original, args.crf, args.preset): (inp, out) for inp, out in tasks}
            for future in concurrent.futures.as_completed(futures):
                inp, out = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing {inp}: {e}")
    except KeyboardInterrupt:
        logging.info("Conversion interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info("Conversion complete.")


if __name__ == "__main__":
    main()
