# The-finding-of-the-location-of-the-vehicle-registration-number

##This program has been designed to find the location of the number plate in images of Skoda cars taken from the "https://www.aaaauto.cz/skoda/" website. 
**The main file is "main.py"**. It imports the other two and runs them. 
File "image_download.py" parses the website and downloads the images from there into the "images" folder. Ps: **create a folder before launching**. 
File "find_location_nb_plate.py" processes the images from the "images" folder, marks where the program thinks the number plate should be and saves it in the "images_out" folder. Ps: **create a folder before launching**.

###The required libraries are: os, glob, requests, bs4, multiprocessing, numpy and cv2.

After starting the main file, you need to specify the number of pages you want to process, wait for the program to finish and look at the result in the folder "images_out". 

Program is able to locate number plate with 85%-95% accuracy for "AAA Auto", for Skoda cars.
