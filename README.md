# Finding the number plate on a vehicle

## This program has been designed to find the location of the number plate in images of Skoda cars taken from the "https://www.aaaauto.cz/skoda/" website. 

**The executable code to run  is located in *main.py* file.**. It imports functions from *image_download.py* and *find_location_nb_plate.py*. 

File *image_download.py* parses the website and downloads the images from there into the "images" folder. P.S: **it is needed to create folder before running the programme**.

File *find_location_nb_plate.py* processes the images from the "images" folder, marks where the program thinks the number plate should be and saves output information to "images_out" folder. P.S: **it is needed to create folder before running the programme**.

After starting the main file, you need to specify the number of pages you want to process, wait for the program to finish and look at the result in the folder "images_out". 

Program is able to find number plate with 87%-97% accuracy from "AAA Auto" website, for Skoda cars.
