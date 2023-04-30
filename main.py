from image_download import main as download
from find_location_nb_plate import main as finder
import os
import glob


def clear_folder(files: [str]):
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def main():
    pages = -1
    while pages < 1 or pages > 60:
        print("Enter the number of pages you would like to download and find location of number_plate\n"
              "Ps: there are 36 images per page, pages with valid images 1-60")

        pages = int(input())

    files = glob.glob('images/*.jpg')
    clear_folder(files)

    download(pages)

    files = glob.glob('images_out/*.jpg')
    clear_folder(files)

    finder(pages*36)


if __name__ == '__main__':
    main()
