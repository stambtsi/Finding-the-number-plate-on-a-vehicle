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
              "P.S.: there are 36 images per page, pages with valid images 1-60")
        str_in = input()
        if str_in.isnumeric():
            pages = int(str_in)

    try:
        os.mkdir('images')
    except OSError:
        files = glob.glob('images/*.jpg')
        clear_folder(files)

    download(pages)

    finder(pages*36)


if __name__ == '__main__':
    main()
