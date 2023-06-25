import os
import shutil
from datetime import datetime
import piexif
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm


def add_watermark(image_path, watermark_text, output_dir):
    # Open an image file
    with Image.open(image_path) as img:
        width, height = img.size

        draw = ImageDraw.Draw(img)
        textsize = 40  # this might need to be adjusted depending on the image size
        font = ImageFont.truetype(
            "arial.ttf", textsize
        )  # choose another font if you like
        textwidth, textheight = draw.textsize(watermark_text, font)

        # calculate the x,y coordinates of the text
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), watermark_text, font=font)

        # Make sure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the new image to the output directory
        img.save(os.path.join(output_dir, os.path.basename(image_path)))


def add_watermarks_to_tiff_files(directory, watermark_prefix=""):
    # Collect all TIFF files in directory
    tiff_files = [
        filename
        for filename in os.listdir(directory)
        if filename.lower().endswith(".tiff") or filename.lower().endswith(".tif")
    ]

    print(f"Found {len(tiff_files)} TIFF files")

    # Initialize progress bar
    progress_bar = tqdm(total=len(tiff_files), ncols=80)

    for filename in tiff_files:
        filepath = os.path.join(directory, filename)

        # Fetch the date taken
        exif_dict = piexif.load(filepath)
        if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
            date_taken_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode(
                "utf-8"
            )
            date_taken = datetime.strptime(date_taken_str, "%Y:%m:%d %H:%M:%S")
            watermark_text = (
                watermark_prefix + " " + date_taken.strftime("%Y-%m-%d %H:%M:%S")
            )

            # Add the watermark to the image
            add_watermark(filepath, watermark_text, os.path.join(directory, "output"))

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()


def main():
    # Replace this with the path to your directory
    directory_path = "g:/ip"
    add_watermarks_to_tiff_files(directory_path, watermark_prefix="Date Taken:")


if __name__ == "__main__":
    main()
