#change screenshot function to accept bounding box coordinates
#create a function for determining the hemisphere
#make better names for functions and provide descriptions of each functions exact function. 
#consider the cropping region for taking screenshots and whether it should be changed/improved
#improve variable names and use all caps for constants. constants should be global. try to make variable names descriptive yet as short as possible. use "underscore" syntax
#get rid of any "magic" variables by creating more constants
#improve the names given to screenshots

#make it so the hemisphere can be determined without centering the sun on the screen?
#improve sun detection (filter out electrical distribution cables, improve how it ignores the top right corner icon, etc)
#add dictionary with list of countries and their probabilities
#make function that guesses which country it thinks its in
#optimize compass deviation from west/east
#optimize what countries it finds to be more likely if the sun is not detected 
#add language detection, being able to detect what side of the road people are driving on (based on road signs, road markings and possibly the direction of other cars
#make a formula to calculate the minimum possible duration for when the drag function is called. This way the programmer doesn't enter in anything.

#image quality (USA and Australia)
#roof rack (and black tape on roof rack)
#kenya snorkel, ghana tape
#license plates (yellow, white, white with blue, length)
#side of the road people are driving on (determine what side of the road you are driving on using your own car?)
#language
#road markings (centerline and also if dashed white outer lines)
#car models, types of vehicles (trucks or not)
#red houses in nordic countries


# Standard imports
# --------------------------------------------------------------------------------------------------------------------------------------------------
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
import win32gui
import time
import math
import matplotlib.pyplot as plt 
import imutils
import itertools
from collections import Counter
#from imageai.Detection import ObjectDetection
import os
import pytesseract
from textblob import TextBlob
from pytesseract import Output
import fasttext
model = fasttext.load_model('lid.176.bin')

# Constant Variables
#--------------------------------------------------------------------------------------------------------------------------------------------------

#rows, columns, channels = image.shape
default_width=2558 #used to be 2582 for some reason
default_height=1438 #used to be 1402 for some reason
turn_dist=(1500/2558)*default_width #1500
turn_start_x=(2100/2558)*default_width #2100
turn_start_y=(600/1438)*default_height #600
turn_time=0.3
look_up_dist=(1000/1438)*default_height #1000
look_up_start_x=(2100/2558)*default_width #2100
look_up_start_y=(300/1438)*default_height #300
look_up_time=0.3

trim_x_1 = (116/2558)*default_width #116
trim_x_2 = (2102/2558)*default_width #2102 (used to be 2306)
trim_y_1 = (287/1438)*default_height #287
trim_y_2 = (1378/1438)*default_height #1378

iterations=5
sky_iterations=5
min_size_of_sun=10000 #Assumes min area of the sun is 10,000 pixels

guess_btn_x = 2126 #x coordinate of guess button
guess_btn_y = 1337 #y coordinate of guess button
nextround_btn_x = 1281 #x coordinate of next round button
nextround_btn_y = 1123 #y coordinate of next round button
return_to_start_btn_x = 65 #x coordinate of return to start button
return_to_start_btn_y = 1180 #y coordinate of return to start button

#Non-constant Variables
geo_round=1 #round=1
program_images_directory="C:\\Users\\Andrew Callam\\Downloads\\OpenCV\\Geoguessr\\Program Images\\Round {}\\".format(geo_round)

camera_gen="Unknown"
japan_blur="Unknown"
camera_blur=0
i=0
sun_lower_limit=(200, 126, 120)
sun_upper_limit=(255, 140, 128)

#Language Variables
rotated=False
error=False
min_conf=0.5
min_word_conf=79 #percentage
padding = 0.01
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
config = ("-l afr+ara+bul+ces+dan+deu+eng+est+fin+fra+heb+hrv+hun+ind+isl+ita+kor+lav+lit+mkd+mlt+msa+nld+nor+pol+por+ron+rus+slk+slv+spa+sqi+srp+swa+swe+tha+tur+ukr --oem 1 --psm 3")
all_languages = []

#Country Coordinates
country_xy = {
    "USA": [2276, 994],
    "Japan": [2022, 1002],
    "France": [2497, 971],
    "Russia": [1827, 935],
    "UK": [2490, 954], 
    "South Africa": [1774, 1157],
    "Canada": [2323, 978],
    "Australia": [2034, 1158],
    "Brazil": [2385, 1135],
    "Finland": [1783, 907],
    "Spain": [2485, 992],
    "Germany": [1749, 955],
    "Mexico": [2280, 1041],
    "Chile": [2340, 1165],
    "Norway": [1748, 917],
    "Argentina": [2352, 1176],
    "Austria": [1758, 972],
    "India": [1891, 1037], 
    "Singapore": [2214, 1153],
    "Sweden": [1756, 916],
    "Thailand": [1941, 1054],
    "Ireland": [2475, 952],
    "Italy": [1753, 986],
    "Lithuania": [1777, 946],
    "Netherlands": [2505, 955],
    "Poland": [1767, 958],
    "South Korea": [1996, 1006],
    "Taiwan": [1983, 1035],
    "Botswana": [1776, 1136],
    "Indonesia": [1946, 1093],
    "Malaysia": [1943, 1079],
    "Peru": [2333, 1110],
    "Turkey": [1799, 998],
    "United Arab Emirates": [1841, 1035],
    "Bangladesh": [1917, 1035],
    "Belgium": [2504, 962],
    "Bolivia": [2353, 1124],
    "China": [1973, 1027],
    "Colombia": [2336, 1079],
    "Costa Rica": [2314, 1066],
    "Croatia": [1762, 978],
    "Albania": [1768, 991],
    "Andorra": [1778, 958], 
    "Bulgaria": [1779, 986],
    "Cambodia": [1950, 1060],
    "Czechia": [1759, 966],
    "Denmark": [1746, 943],
    "Ecuador": [2324, 1089],
    "Egypt": [1789, 1028],
    "Estonia": [1780, 933],
    "Eswatini": [1793, 1147],
    "Ghana": [2491, 1072],
    "Greece":[1773, 998], 
    "Hungary": [1765, 974],
    "Iceland": [2453, 904],
    "Israel": [1799, 1018],
    "Kenya": [1806, 1087],
    "Kyrgyzstan": [1887, 989],
    "Lebanon": [1802, 1011],
    "Lesotho": [1785, 1154],
    "Malta": [1833, 995], 
    "New Zealand": [2093, 1188],
    "Portugal": [2476, 995],
    "Romania": [1778, 977],
    "Senegal": [2460, 1054],
    "Serbia": [1770, 983],
    "Slovakia": [1767, 969],
    "Slovenia": [1756, 976],
    "Tunisia": [1746, 1006],
    "Uganda": [1794, 1088],
    "Ukraine": [1790, 966],
    "Dominican Republic": [2343, 1047],
    "Latvia": [1777, 940], 
    "Uruguay": [2373, 1160],
    "Bhutan": [1918, 1026],
    "Guatemala": [2300, 1054],
    "Jordan": [1802, 1018],
    "Laos": [1944, 1043],
    "Mongolia": [1946, 973],
    "Philippines": [1992, 1071],
    "Sri Lanka": [1897, 1071],
    "Switzerland": [2511, 973],
    "Vietnam": [1955, 1062]

    }

# FUNCTIONS
# --------------------------------------------------------------------------------------------------------------------------------------------------

#Make dist_x +ve to turn right and -ve to turn left. Make dist_y +ve to look up and -ve to look down.
def drag(x, y, dist_x, dist_y, time):
    
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x-dist_x, y+dist_y, duration=time)
    pyautogui.mouseUp(button='left')

#Finds the currently open tab in Google Chrome.
def find_window():
    
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    google = [(hwnd, title) for hwnd, title in winlist if 'google' in title.lower()]
    #just grab the hwnd for first window matching google
    google = google[0]
    find_window.hwnd = google[0]

#Takes a screenshot and saves it to the "program_images_directory" variable directory with the name "screenshot_" followed by the "idetifier" parameter value. 
#The x1, y1, x2, and y2 parameters allow the image to be cropped.
def screenshot(identifier, x1=trim_x_1, y1=trim_y_1, x2=trim_x_2, y2=trim_y_2):
    win32gui.SetForegroundWindow(find_window.hwnd) #uses find_window.hwnd instead of just hwnd because hwnd isn't in the scope of this function
    bbox = win32gui.GetWindowRect(find_window.hwnd)
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img.save("{}screenshot_{}.png".format(program_images_directory, identifier))  

#Looks for sun in input image, and returns whether a sun was found and the (x, y) location of the sun and the sun's contour area.
def find_sun(image_directory, image_display_identifier, lower_limit, upper_limit):
    
    #Loads an image into the variable "image" with colour
    image = cv2.imread(str(image_directory), cv2.IMREAD_COLOR)

    #thresh = cv2.inRange(image, (254,254,254), (255,255,255))
    
    #image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    #thresh = cv2.inRange(image_hsv, (0,0,254), (120,1,255))

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    thresh = cv2.inRange(image_lab, lower_limit, upper_limit)

    #thresh_bgr = cv2.inRange(image, (254,254,254), (255,255,255))
    
    #image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    #thresh_hsv = cv2.inRange(image_hsv, (0,0,254), (120,1,255))

    #image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #thresh_lab = cv2.inRange(image_lab, (200,126,126), (255,128,128))
    #thresh = cv2.bitwise_and(thresh_lab,thresh_lab,mask = thresh_bgr)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    i=0
    best_match=2
    best_match_index=0
    best_match_cX=0
    best_match_cY=0
    area=1
    best_area=min_size_of_sun
    cX=0
    cY=0
    sun_found = False

    #Look for sun in image
    while(i<len(contours)): 
        area = cv2.contourArea(contours[i])
  
        if  area>best_area:
            image_contours = cv2.drawContours(image, contours, i, (0,0,255), 2)
            best_area=area
            best_match_index=i
            sun_found=True

            #find centroid of sun
            M = cv2.moments(contours[i])
            if M["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
                best_match_cX = int(M["m10"] / M["m00"]) + trim_x_1
                best_match_cY = int(M["m01"] / M["m00"]) + trim_y_1
            
        i=i+1

    
    if len(contours)>0: #if contours were found in the image
        #Puts a green circle to approximate where the sun is (display purposes only)
        (x,y),radius = cv2.minEnclosingCircle(contours[best_match_index])
        center = (int(x),int(y))
        radius = int(radius)
        image_circle_approx = cv2.circle(image,center,radius,(0,255,0),2)
        #image_contours = cv2.drawContours(image, contours, -1, (0,0,255), 2) #for debugging

        #For debugging
        #print("Countour Area of best match for {} is {}\n".format(image_display_identifier, cv2.contourArea(contours[best_match_index])))

        #Display images
        #cv2.imshow('thresh_{}'.format(image_display_identifier),thresh)
        #cv2.imshow('circle_{}'.format(image_display_identifier),image_circle_approx)
        #cv2.imwrite("{}thresh_sun_{}.png".format(program_images_directory, image_display_identifier), thresh)
        #cv2.imwrite("{}circle_sun_{}.png".format(program_images_directory, image_display_identifier), image_circle_approx)

    return sun_found, best_match_cX, best_match_cY, best_area

#Returns angle of compass for an input image.
def compass(image_directory):
    
    compass_cX=45
    compass_cY=45

    image = cv2.imread(str(image_directory), cv2.IMREAD_COLOR)
    
    compass_roi = image[int((774/1438)*default_height):int((864/1438)*default_height),int((21/2558)*default_width):int((111/2558)*default_width)] #[774:864,21:111]
    compass_hsv = cv2.cvtColor(compass_roi, cv2.COLOR_BGR2HSV) 
    compass_thresh=cv2.inRange(compass_hsv, (0,0,230), (0,0,255))

    compass_contours, compass_hierarchy = cv2.findContours(compass_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    i=0
    threshold_area=300
    filtered_contours = []
    #filters out any contours in the ROI that happen to be the same colour as the red arrow of the compass, but have a much smaller area than the red arrow on the compass
    while(i<len(compass_contours)):
        if cv2.contourArea(compass_contours[i])>threshold_area:
            filtered_contours.append(compass_contours[i])
        i=i+1
    
    ellipse = cv2.fitEllipse(filtered_contours[0])

    x, y = ellipse[0]

    if x<compass_cX:
        angle=360-(ellipse[2]+90)
    else:
        angle=360-(ellipse[2]-90)

    if angle>180:
        angle=angle-180
    elif angle<180:
        angle=angle+180

    print("Estimated angle of compass is {} degrees (before mask) \n".format(int(round(angle, 0))))

    #if the estimated angle is close to either 90 or 270 degrees (within 5 degrees), then it is not reliable and thus a 
    #different approach must be used to verify the angle
    if (85<angle and angle<95) or (265<angle and angle<275):
        hemisphere="Unknown"
        if (85<angle and angle<95):
            #check to see if white arrow is pointing directly down (within 5 degrees)
            polygons = np.array([ 
                [(40, 70), (50, 70), (45, 83)] 
                ])  
            mask = np.zeros_like(compass_thresh) 
            cv2.fillPoly(mask, polygons, (255, 255, 255)) 

            masked_image = cv2.bitwise_and(compass_thresh, mask) 
            mask_contours, mask_hierarchy = cv2.findContours(masked_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

            i=0
            total_area=0
            mask_threshold_area = 10
            while(i<len(mask_contours)):
                total_area=total_area+cv2.contourArea(mask_contours[i])
                i=i+1
            if total_area>=mask_threshold_area: #if true, then hemisphere is Southern and original angle reading was correct
                hemisphere="South"
            else: #in this case, the angle reading was likely wrong according to the mask, but needs to be confirmed
                polygons = np.array([ 
                [(40, 20), (50, 20), (45, 7)] 
                ])  

                mask = np.zeros_like(compass_thresh) 
                cv2.fillPoly(mask, polygons, (255, 255, 255)) 

                masked_image = cv2.bitwise_and(compass_thresh, mask) 
                mask_contours, mask_hierarchy = cv2.findContours(masked_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

                i=0
                total_area=0
                mask_threshold_area = 10
                while(i<len(mask_contours)):
                    total_area=total_area+cv2.contourArea(mask_contours[i])
                    i=i+1
                if total_area>=mask_threshold_area: 
                    hemisphere="North"
                else: 
                    print("Mask is unsure what hemisphere the compass indicates. Going to assume original guess was correct \n")

        if (265<angle and angle<275):
        #check to see if white arrow is pointing directly up (within 5 degrees)

            polygons = np.array([ 
                [(40, 20), (50, 20), (45, 7)] 
                ])  

            mask = np.zeros_like(compass_thresh) 
            cv2.fillPoly(mask, polygons, (255, 255, 255)) 

            masked_image = cv2.bitwise_and(compass_thresh, mask) 
            mask_contours, mask_hierarchy = cv2.findContours(masked_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

            i=0
            total_area=0
            mask_threshold_area = 10
            while(i<len(mask_contours)):
                total_area=total_area+cv2.contourArea(mask_contours[i])
                i=i+1
            if total_area>=mask_threshold_area: #if true, then hemisphere is Southern and original angle reading was correct
                hemisphere="North"
            else: #in this case, the angle reading was likely wrong according to the mask, but needs to be confirmed
                polygons = np.array([ 
                [(40, 70), (50, 70), (45, 83)] 
                ])  
                mask = np.zeros_like(compass_thresh) 
                cv2.fillPoly(mask, polygons, (255, 255, 255)) 

                masked_image = cv2.bitwise_and(compass_thresh, mask) 
                mask_contours, mask_hierarchy = cv2.findContours(masked_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

                i=0
                total_area=0
                mask_threshold_area = 10
                while(i<len(mask_contours)):
                    total_area=total_area+cv2.contourArea(mask_contours[i])
                    i=i+1
                if total_area>=mask_threshold_area:
                    hemisphere="South"
                else:
                    print("Mask is unsure what hemisphere the compass indicates. Going to assume original guess was correct \n")
    
        if hemisphere=="North":
            angle=270
        elif hemisphere=="South":
            angle=90

    return angle

#Centers sun in sky.
def center_sun_sky(sky_iterations, sun_cX, sun_cY, image_directory, lower_limit, upper_limit):
    
    #partition file name to get number of rotations backwards
    directory_no_extension = image_directory.partition(".png")[0]
    rotations=int(directory_no_extension.partition("sky")[2])
    rotations_backwards=sky_iterations-rotations
    error=False
    print("Centering to sun in sky...\n")

    i=0
    while(i<rotations_backwards):
        drag(default_width-turn_start_x, turn_start_y, -turn_dist, 0, turn_time)
        i=i+1

    n=0
    deviation=(10/2558)*default_width #10
    if(((default_width/2)+deviation)<sun_cX or ((default_width/2)-deviation)>sun_cX):
        while(((default_width/2)+deviation)<sun_cX or ((default_width/2)-deviation)>sun_cX):
            #print("#{}: sun_cX: {}  sun_cY: {} \n".format(n, sun_cX, sun_cY))
            drag(sun_cX, sun_cY, (sun_cX)-(default_width/2), (((trim_y_2-trim_y_1)/2)+trim_y_1)-(sun_cY), 0.4)
            screenshot(identifier="center_sun{}".format(n))
            center_sun_image_directory="{}screenshot_center_sun{}.png".format(program_images_directory, n)
            sun_found, sun_cX, sun_cY, area = find_sun(center_sun_image_directory, "centering_sky{}".format(n), lower_limit, upper_limit)
            
            #screenshot(identifier="center_sun_mark{}".format(n), x1=0, y1=0, x2=default_width, y2=default_height)
            #test_image = cv2.imread("{}screenshot_center_sun_mark{}.png".format(program_images_directory, n), cv2.IMREAD_COLOR)
            #cv2.circle(test_image,(int(sun_cX),int(sun_cY)), 3, (0,0,255), -1)
            #cv2.line(test_image,(int(default_width/2),int(0)),(int(default_width/2),int(default_height)),(0,255,0),1)
            #cv2.line(test_image,(int((default_width/2)+deviation),int(0)),(int((default_width/2)+deviation),int(default_height)),(0,255,0),1)
            #cv2.line(test_image,(int((default_width/2)-deviation),int(0)),(int((default_width/2)-deviation),int(default_height)),(0,255,0),1)
            #cv2.imwrite("{}center_sun_marks{}.png".format(program_images_directory, n), test_image)
            n=n+1
            if not sun_found:
                print("Error, sun not found after attempting to center. \n")
                error=True
                break
            if n>8:
                print("Stopped centering because iterations is greater than 8. \n")
                break
    else:
        print("Sun already centered...\n")
        screenshot(identifier="center_sun".format(n))
    return error

#Centers sun from ground.
def center_sun_ground(sky_iterations, ground_iterations, sun_cX, sun_cY, image_directory, lower_limit, upper_limit):
    
    print("Centering sun from ground...\n")
    directory_no_extension = image_directory.partition(".png")[0]
    rotations=int(directory_no_extension.partition("_")[2])
    rotations_backwards=iterations-rotations

    i=0
    while(i<sky_iterations):
        drag(default_width-turn_start_x, turn_start_y, -turn_dist, 0, turn_time)
        i=i+1

    #look down
    time.sleep(0.05)
    drag(look_up_start_x, ((trim_y_1+((trim_y_2-trim_y_1)/2))-(look_up_start_y-((trim_y_2-trim_y_1)/2))), 0, -look_up_dist, look_up_time)

    i=0
    while(i<rotations_backwards):
        drag(1291-(turn_start_x-1291), turn_start_y, -turn_dist, 0, turn_time)
        i=i+1

    n=0
    deviation=(10/2558)*default_width #10
    if(((default_width/2)+deviation)<sun_cX or ((default_width/2)-deviation)>sun_cX):
        while(((default_width/2)+deviation)<sun_cX or ((default_width/2)-deviation)>sun_cX):
            drag(sun_cX, sun_cY+trim_y_1, sun_cX-(default_width/2), 0, 0.4)
            screenshot(identifier="center_sun{}".format(n))
            center_sun_image_directory="{}screenshot_center_sun{}.png".format(program_images_directory, n)
            sun_found, sun_cX, sun_cY, area = find_sun(center_sun_image_directory, "centering_ground{}".format(n), lower_limit, upper_limit)
            n=n+1
            if not sun_found:
                print("Error, sun not found after attempting to center. \n")
                break
            if n>8:
                print("Error, centering iterations is greater than 8. \n")
                break
    else:
        print("Sun already centered...\n")
        screenshot(identifier="center_sun".format(n))

#Given an angle, it calculates the hemisphere (if the sun were in the center of the screen for the given input angle).
def calculate_hemisphere(angle):
    
    min_angle_deviation=10

    if (180+min_angle_deviation)<angle<(360-min_angle_deviation):
        hemisphere="North"
        print("Northern Hemisphere")
    elif (0+min_angle_deviation)<angle<(180-min_angle_deviation):
        hemisphere="South"
        print("Southern Hemisphere")
    else:
        hemisphere="Unknown"
        print("Hemisphere Unknown (due to compass uncertainty)") 

    return hemisphere

#Determines the hemisphere.
def determine_hemisphere(lower_limit, upper_limit):
    
    abs_best_area=min_size_of_sun
    area=1
    n=0
    hemisphere="Unknown"
    sun_found=False
    error=False

    #Look through all pictures of sky and determine the image that most likely contains the sun 
    while(n<sky_iterations):
        image_directory = "{}screenshot_sky{}.png".format(program_images_directory, n)
        sun, cX, cY, area = find_sun(image_directory, image_display_identifier="screenshot_sky{}".format(n), lower_limit=lower_limit, upper_limit=upper_limit)

        if sun:
            sun_found=True
    
        #If there are ultiple screenshots with the sun, this will use the image with the largest sun
        if area>abs_best_area:
            abs_best_area=area
            abs_best_screenshot=image_directory
            abs_best_match_cX = cX
            abs_best_match_cY = cY
        n=n+1

    #If the sun was found in the sky, determine the hemisphere
    if sun_found:
        print("Sun detected in image \"{}\" \n".format(abs_best_screenshot.partition("{}".format(program_images_directory))[2]))
        error = center_sun_sky(sky_iterations, abs_best_match_cX, abs_best_match_cY, abs_best_screenshot, lower_limit, upper_limit)
        if not error:
            screenshot("center_sun_compass", x1=0, y1=178, x2=2558, y2=1186)
            angle = compass("{}screenshot_center_sun_compass.png".format(program_images_directory))
            hemisphere = calculate_hemisphere(angle)
        else:
            print("Hemisphere Unknown")
            hemisphere="Unknown"
        return hemisphere
    
    else:
        #Look for sun in ground pictures
        print("Sun not found, now looking at ground pictures...\n")
        n=0
        while(n<iterations):
            image_directory = "{}screenshot_{}.png".format(program_images_directory, n)
            sun, cX, cY, area = find_sun(image_directory, image_display_identifier="ground{}".format(n), lower_limit=lower_limit, upper_limit=upper_limit)
   
            if sun:
                sun_found=True

            if area>abs_best_area:
                abs_best_area=area
                abs_best_screenshot=image_directory
                abs_best_match_cX = cX
                abs_best_match_cY = cY
                dist_from_center_of_screen = math.sqrt(((1291-cX)**2)+((505-cY)**2))
            n=n+1
    
        #If the sun was found from the ground, determine the hemisphere
        if sun_found:
            print("Sun detected in image \"{}\" \n".format(abs_best_screenshot.partition("{}".format(program_images_directory))[2]))
            center_sun_ground(sky_iterations, iterations, abs_best_match_cX, abs_best_match_cY, abs_best_screenshot, lower_limit, upper_limit)
            screenshot("center_sun_compass", x1=0, y1=178, x2=2558, y2=1186)
            angle=compass("{}screenshot_center_sun_compass.png".format(program_images_directory))
            hemisphere = calculate_hemisphere(angle)
            return hemisphere
        else:
            print("Sun not found \n")
            print("Hemisphere Unknown")
            hemisphere="Unknown"
            return hemisphere
    
#Input a country, and the function will click on that country in the geoguessr map.
def select_country(country):

    x, y = country_xy[country]

    time.sleep(0.25)
    #pyautogui.moveTo(2338, 1165)
    pyautogui.moveTo(2400, 1240)#hovers over the small map
    time.sleep(0.5)

    pyautogui.moveTo(2130, 1000)#hovers over the expand map button
    time.sleep(0.5)
    pyautogui.mouseDown() #clicks the expand map button
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(0.1)

    if country=="Malta" or country=="Andorra" or country=="Singapore":
        drag(x=1840, y=1038, dist_x=-250, dist_y=0, time=0.5)
        pyautogui.moveTo(1772, 768) #hovers over the zoom-in button on the map
        time.sleep(0.5)
        pyautogui.mouseDown() #clicks the zoom-in button
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)


    pyautogui.moveTo(x, y) #hovers over the country that is supposed to be clicked
    time.sleep(1)
    pyautogui.mouseDown() #clicks the desired country
    time.sleep(0.1)
    pyautogui.mouseUp()

#Clicks the "Guess" button on Geoguessr.
def click_guess():
    pyautogui.moveTo(guess_btn_x, guess_btn_y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()

#Clicks the "Next Round" button on Geoguessr.
def click_next_round():
    next_round_btn_visible=False
    time.sleep(1)
    while next_round_btn_visible==False:
        screenshot("next_round_btn", x1=1160, y1=1110, x2=1394, y2=1130)
        next_round_btn_image = cv2.imread("{}screenshot_next_round_btn.png".format(program_images_directory), cv2.IMREAD_COLOR)
        thresh = cv2.inRange(next_round_btn_image, (9,130,86), (9,130,86))
        cv2.imwrite("{}nextround_thresh.png".format(program_images_directory), thresh)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)>0:
            area = cv2.contourArea(contours[0])
            if area == 3.0:
                next_round_btn_visible=True
                pyautogui.moveTo(nextround_btn_x, nextround_btn_y)
                time.sleep(1)
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
            else:
                next_round_btn_visible=False
                time.sleep(3)
        else:
            next_round_btn_visible=False
            time.sleep(3)

#Clicks the "Return to Start" button on Geoguessr.
def return_to_start():
    time.sleep(0.5)
    pyautogui.moveTo(return_to_start_btn_x, return_to_start_btn_y)
    time.sleep(1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(1)

#Test function (not used by program... yet).
def road_markings():
    #read in the first image taken (as this should include the road)
    image = cv2.imread("{}screenshot_0.png".format(program_images_directory), cv2.IMREAD_COLOR)
    
    #exclude everything except the ROI
    height = image.shape[0] 
    polygons = np.array([ 
        [(664, height), (1846, height), (1305, 535), (1290, 535)] 
        ])  
    mask = np.zeros_like(image) 
    cv2.fillPoly(mask, polygons, (255, 255, 255)) 

    masked_image = cv2.bitwise_and(image, mask) 
    
    #threshold to ignore stuff that isn't yellow or white
    
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    #image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HSL) 
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    thresh_white = cv2.inRange(image_lab, (130,126,130), (205,132,135))
    #thresh_white = cv2.inRange(image_hsl, (15,15,200), (20,35,255))
    #thresh_white = cv2.inRange(image_hsv, (15,15,200), (20,35,255))

    #image_YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb) 
    #thresh_yellow = cv2.inRange(image_YCrCb, (145,146,100), (165,156,110))

    #thresh_pavement = cv2.inRange(image_hsv, (0,0,254), (120,1,255))

    #image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #thresh = cv2.inRange(image_lab, (200,126,126), (255,128,128))

    #thresh_bgr = cv2.inRange(image, (254,254,254), (255,255,255))

    #canny_image = cv2.Canny(image,100,200) #(image to be analyzed, min thresh val, max thresh val)
    #lines = cv2.HoughLinesP(canny_image,2,np.pi/180,500) #(image to be analyzed, rho accuracy (pixels), theta accuracy (radians), min length of line)

    #display Hough Transform lines
    #for line in lines:
        #x1, y1, x2, y2 = line[0]
        #cv2.line(image, (x1, y1), (x2, y2), (0,0,255), 2)

    #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    retval = cv2.imwrite("{}screenshot_roi.png".format(program_images_directory), masked_image) 
    #cv2.imshow('canny', canny_image)
    cv2.imshow('roi', masked_image)
    #cv2.imshow('hough transform', image)
    #cv2.imshow('thresh_yellow', thresh_yellow)
    cv2.imshow('thresh_white', thresh_white)

#Test function (not used by program... yet).
def taiwan():
    img = cv2.imread("{}screenshot_0.png".format(program_images_directory), 0)
    img2 = img.copy()
    template = cv2.imread("{}taiwan pattern.png".format(program_images_directory),0)
    w, h = template.shape[::-1]
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()

#Test function (not used by program... yet).
def taiwan_test():

    img_rgb = cv2.imread("{}screenshot_0.png".format(program_images_directory)) 

    # Convert to grayscale 
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
   
    # Read the template 
    template = cv2.imread("{}taiwan pattern.png".format(program_images_directory),0) 
   
    # Store width and height of template in w and h 
    w, h = template.shape[::-1] 
    found = None
  
    for scale in np.linspace(0.2, 1.0, 20)[::-1]: 
  
        # resize the image according to the scale, and keep track 
        # of the ratio of the resizing 
        resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * scale)) 
        r = img_gray.shape[1] / float(resized.shape[1]) 
   
        # if the resized image is smaller than the template, then break 
        # from the loop 
        # detect edges in the resized, grayscale image and apply template  
        # matching to find the template in the image 
        edged = cv2.Canny(resized, 50, 200) 
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED) 
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result) 
        # if we have found a new maximum correlation value, then update 
        # the found variable 
        if found is None or maxVal > found[0]: 
            if resized.shape[0] < h or resized.shape[1] < w: 
                    break
            found = (maxVal, maxLoc, r) 
   
    # unpack the found varaible and compute the (x, y) coordinates 
    # of the bounding box based on the resized ratio 
    (_, maxLoc, r) = found 
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r)) 
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r)) 
  
    # draw a bounding box around the detected result and display the image 
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2) 
    cv2.imshow("Image", image) 

#Test function (not used by program... yet).
def detect_objects():
    execution_path = os.getcwd()

    #Avg run time: RetinaNet=35 seconds, YOLO=7 seconds, TinyYOLO=6 seconds
    #Bounding boxes are much much better with Retina

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet() #Model Type Options: RetinaNet, YOLOv3, TinyYOLOv3
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5")) #Model Path Options: resnet50_coco_best_v2.1.0.h5, yolo.h5, yolo-tiny.h5

    detector.loadModel()

    print("MODEL LOADED")
    start = time.time()

    custom_objects = detector.CustomObjects(car=True, motorcycle=True, truck=True, person=True, bus=True, stop_sign=True, dog=True, sheep=True)

    detections, objects_path = detector.detectObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path , "screenshot_0.png"), output_image_path=os.path.join(execution_path , "imagenew.png"), minimum_percentage_probability=60,  extract_detected_objects=True)

    for eachObject, eachObjectPath in zip(detections, objects_path):
        print(eachObject["name"] , " : " , eachObject["percentage_probability"], " : ", eachObject["box_points"] )
        print("Object's image saved in " + eachObjectPath)
        print("--------------------------------")

    end = time.time()
    print(end - start)

#Determine Camera Generation and use screenshots from beginning of program to determine if Gen 1 (camera should not already be looking down).
def detect_camera_gen():

    cam_gen="Unknown"

    #Check for Gen 1
    i=0
    gen_1_threshold = 40
    total_blur=0
    avg_blur=0
    while (i<iterations):
        img_rgb = cv2.imread("{}screenshot_{}.png".format(program_images_directory, i)) 
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        blur=cv2.Laplacian(img_gray, cv2.CV_64F).var()
        #print("Blur #{}: {} \n".format(i, blur))
        total_blur=total_blur+blur
        i=i+1

    avg_blur=total_blur/iterations
    print("Blurriness (lower num = more blurry): {} \n".format(avg_blur))
    if avg_blur<gen_1_threshold:
        cam_gen="Gen 1"
        print("Cam Gen: {} \n".format(cam_gen))
        return cam_gen, avg_blur
    
    #Check for Gen 2
    gen_2_threshold = 33 #should be approx 29 to 33?
    i=0
    total_blur=0

    drag(x=(default_width/2), y=1373, dist_x=0, dist_y=-1360, time=1.5) #Look down

    while(i<4):
        pyautogui.moveTo(1290, 138) #get mouse out of the way of screenshot
        screenshot(identifier="gen_2_check_{}".format(i), x1=311, y1=288, x2=2318, y2=1379)
        img_looking_down = cv2.imread("{}screenshot_gen_2_check_{}.png".format(program_images_directory, i)) 
        blur=cv2.Laplacian(img_looking_down, cv2.CV_64F).var()
        total_blur=total_blur+blur
        print("Ground Blur: {}".format(blur))
        drag(x=2220, y=480, dist_x=1404, dist_y=0, time=1)
        i=i+1

    avg_blur=total_blur/4
    print("Average Blur: {} \n".format(avg_blur))

    if avg_blur>=gen_2_threshold:
        cam_gen="Gen 3 or 4"
        print("Cam Gen: {} \n".format(cam_gen))
        return cam_gen, avg_blur

    if avg_blur<gen_2_threshold:
        cam_gen="Gen 2"
        print("Cam Gen: {} \n".format(cam_gen))
        return cam_gen, avg_blur

    return cam_gen, avg_blur

#Makes the in-game map as small as possible.
def set_map():
    #hover over map, expand it, minimize it, and then it should be reset in 2 seconds
    time.sleep(0.25)
    pyautogui.moveTo(2400, 1240)#hovers over the small map
    time.sleep(0.5)

    pyautogui.moveTo(2130, 1000)#hovers over the expand map button
    time.sleep(0.5)
    pyautogui.mouseDown() #clicks the expand map button
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(0.1)

    pyautogui.moveTo(1814, 712)#hovers over the minimize map button
    time.sleep(0.5)
    pyautogui.mouseDown() #clicks the minimize map button
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(1.5)

#Attempts to straighten the geocar (assuming already looking downwards). Returns whether it was able to striaghten, or whether it was unable to straighten.
def straighten_geocar():

    compass_radius=47.5 #max is 47.5
    compass_cX = 65.5 #65.5
    compass_cY = 996.5 #966.5

    reliable=False

    screenshot(identifier="straight_geocar", x1=1124, y1=614, x2=1436, y2=932)

    image = cv2.imread("{}screenshot_straight_geocar.png".format(program_images_directory), cv2.IMREAD_COLOR)

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    thresh = cv2.inRange(image_lab, (255,128,128), (255,128,128))

    cv2.imwrite("{}arrows_thresh.png".format(program_images_directory), thresh)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    i=0
    threshold_area=2600
    filtered_contours = []
    
    if len(contours)>0:
        while(i<len(contours)):
            if cv2.contourArea(contours[i])>threshold_area:
                filtered_contours.append(contours[i])
                #print(cv2.contourArea(contours[i]))
            i=i+1
    else:
        print("Geocar straightening reliability is False. No arrows found. \n")
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight
    
    #Check if there is more than two arrows or only one arrow based on total area of filtered contours
    i=0
    total_area=0
    while(i<len(filtered_contours)):
        total_area=total_area+cv2.contourArea(filtered_contours[i])
        i=i+1
    
    total_threshold_area=5600
    if total_area>total_threshold_area or total_area<(threshold_area*2):
        print("Geocar straightening reliability is False. Either more than two arrows or only one arrow. \n")
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight

    #Find the centroid of arrow number 0
    M_0 = cv2.moments(filtered_contours[0])
    if M_0["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
        arrow_cX_0 = int(M_0["m10"] / M_0["m00"])
        arrow_cY_0 = int(M_0["m01"] / M_0["m00"])
    
    #Find the centroid of arrow number 1
    M_1 = cv2.moments(filtered_contours[1])
    if M_1["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
        arrow_cX_1 = int(M_1["m10"] / M_1["m00"])
        arrow_cY_1 = int(M_1["m01"] / M_1["m00"])
    
    
    #Draw a line connecting the two centroids and save the resulting image 
    cv2.line(image,(arrow_cX_0,arrow_cY_0),(arrow_cX_1,arrow_cY_1),(0,255,0),1)
    cv2.imwrite("{}arrows_with_line.png".format(program_images_directory), image)

    #Determine the orientation of the arrows based on the location of their centroids
    if arrow_cY_1 > arrow_cY_0:
        if arrow_cX_1 > arrow_cX_0:
            #(cX_1, cY_1) is in quadrant "C"
            angle = (math.atan((arrow_cX_1-arrow_cX_0)/(arrow_cY_1-arrow_cY_0)))*(180/math.pi)
            #print("Quadrant \"C\" \n")
            #print("Arrows angle: {} \n".format(angle))
            target_compass_angle = 90-angle
            if 0<=target_compass_angle<=90:
                x_target = ((math.cos(math.radians(target_compass_angle)))*compass_radius)+compass_cX
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
                #print("x_target: {}  y_target: {} \n".format(x_target, y_target))
                angle=math.degrees(math.atan((abs(compass_cY-y_target))/(abs(compass_cX-x_target))))
                #print("target angle: {} \n".format(angle))
                x_target=round(x_target, 0)
                y_target=round(y_target, 0)
                angle=math.degrees(math.atan((abs(compass_cY-(int(y_target))))/(abs(compass_cX-(int(x_target))))))
                #print("actual angle of compass from calculations: {} \n".format(angle))
            elif 90<target_compass_angle<=180:
                target_compass_angle=180-target_compass_angle
                x_target = compass_cX-((math.cos(math.radians(target_compass_angle)))*compass_radius)
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
            
            pyautogui.moveTo(x_target, y_target)
            x, y = pyautogui.position()
            #print("X: {}  Y: {} \n".format(x, y))
            time.sleep(0.25)
            pyautogui.mouseDown() 
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)

        elif arrow_cX_1 < arrow_cX_0:
            #(cX_1, cY_1) is in quadrant "T"
            angle = (math.atan((arrow_cX_0-arrow_cX_1)/(arrow_cY_1-arrow_cY_0)))*(180/math.pi)
            #print("Quadrant \"T\" \n")
            #print("Arrows angle: {} \n".format(angle))
            target_compass_angle = 90+angle
            if 0<=target_compass_angle<=90:
                x_target = ((math.cos(math.radians(target_compass_angle)))*compass_radius)+compass_cX
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
                
            elif 90<target_compass_angle<=180:
                target_compass_angle=180-target_compass_angle
                x_target = compass_cX-((math.cos(math.radians(target_compass_angle)))*compass_radius)
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
                #print("x_target: {}  y_target: {} \n".format(x_target, y_target))
                angle=math.degrees(math.atan((abs(compass_cY-y_target))/(abs(compass_cX-x_target))))
                #print("target angle: {} \n".format(angle))
                x_target=round(x_target, 0)
                y_target=round(y_target, 0)
                angle=math.degrees(math.atan((abs(compass_cY-(int(y_target))))/(abs(compass_cX-(int(x_target))))))
                #print("actual angle of compass from calculations: {} \n".format(angle))
            
            pyautogui.moveTo(x_target, y_target)
            x, y = pyautogui.position()
            #print("X: {}  Y: {} \n".format(x, y))
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)

        elif arrow_cX_1 == arrow_cX_0:
            #already straight
            #print("Arrows already straight \n")
            reliable=True
            x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
            return reliable, x_compass_straight, y_compass_straight
    elif arrow_cY_1 < arrow_cY_0: 
        if arrow_cX_1 > arrow_cX_0:
            #(cX_1, cY_1) is in quadrant "A"
            angle = (math.atan((arrow_cX_1-arrow_cX_0)/(arrow_cY_0-arrow_cY_1)))*(180/math.pi)
            #print("Quadrant \"A\" \n")
            #print("Arrows angle: {} \n".format(angle))
            target_compass_angle = 90+angle
            if 0<=target_compass_angle<=90:
                x_target = ((math.cos(math.radians(target_compass_angle)))*compass_radius)+compass_cX
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
            elif 90<target_compass_angle<=180:
                target_compass_angle=180-target_compass_angle
                x_target = compass_cX-((math.cos(math.radians(target_compass_angle)))*compass_radius)
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
                #print("x_target: {}  y_target: {} \n".format(x_target, y_target))
                angle=math.degrees(math.atan((abs(compass_cY-y_target))/(abs(compass_cX-x_target))))
                x_target=round(x_target, 0)
                y_target=round(y_target, 0)
                #print("target angle: {} \n".format(angle))
                angle=math.degrees(math.atan((abs(compass_cY-(int(y_target))))/(abs(compass_cX-(int(x_target))))))
                #print("actual angle of compass from calculations: {} \n".format(angle))
            
            pyautogui.moveTo(x_target, y_target)
            x, y = pyautogui.position()
            #print("X: {}  Y: {} \n".format(x, y))
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)

        elif arrow_cX_1 < arrow_cX_0:
            #(cX_1, cY_1) is in quadrant "S"
            angle = (math.atan((arrow_cX_0-arrow_cX_1)/(arrow_cY_0-arrow_cY_1)))*(180/math.pi)
            #print("Quadrant \"S\" \n")
            #print("Arrows angle: {} \n".format(angle))
            target_compass_angle = 90-angle
            if 0<=target_compass_angle<=90:
                x_target = ((math.cos(math.radians(target_compass_angle)))*compass_radius)+compass_cX
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
                #print("x_target: {}  y_target: {} \n".format(x_target, y_target))
                angle=math.degrees(math.atan((abs(compass_cY-y_target))/(abs(compass_cX-x_target))))
                #print("target angle: {} \n".format(angle)) 
                x_target=round(x_target, 0)
                y_target=round(y_target, 0)
                angle=math.degrees(math.atan((abs(compass_cY-(int(y_target))))/(abs(compass_cX-(int(x_target))))))
                #print("actual angle of compass from calculations: {} \n".format(angle))
            elif 90<target_compass_angle<=180:
                target_compass_angle=180-target_compass_angle
                x_target = compass_cX-((math.cos(math.radians(target_compass_angle)))*compass_radius)
                y_target = compass_cY-((math.sin(math.radians(target_compass_angle)))*compass_radius)
            
            pyautogui.moveTo(x_target, y_target)
            x, y = pyautogui.position()
            #print("X: {}  Y: {} \n".format(x, y))
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)

        elif arrow_cX_1 == arrow_cX_0:
            #already straight
            #print("Arrows already straight \n")
            reliable=True
            x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
            return reliable, x_compass_straight, y_compass_straight
    elif arrow_cY_1 == arrow_cY_0:
        #must turn 90 degrees (angle is 0)
        print("Y-coordinate of arrow centroid's are equal, thus turning 90 degrees... \n")
        drag(x=2220, y=480, dist_x=1404, dist_y=0, time=1)
    else:
        print("Geocar straightening reliability is False. Unsure what went wrong. \n")
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight
    
    #Check if the arrows are straight enough to consider reliable
    screenshot(identifier="straightened_geocar")
    straight_image = cv2.imread("{}screenshot_straightened_geocar.png".format(program_images_directory), cv2.IMREAD_COLOR)
    polygons_1 = np.array([[(1159, 367), (1116, 416), (1100, 399), (1159, 335), (1218, 399), (1202, 416)]])
    polygons_2 = np.array([[(1159, 607), (1116, 558), (1100, 575), (1159, 639), (1218, 575), (1202, 558)]])
    mask = np.zeros_like(straight_image) 
    cv2.fillPoly(mask, polygons_1, (255, 255, 255)) 
    cv2.fillPoly(mask, polygons_2, (255, 255, 255)) 
    masked_image = cv2.bitwise_and(straight_image, mask)
    #cv2.imwrite("{}masked_straight_arrows.png".format(program_images_directory), masked_image)

    image_lab = cv2.cvtColor(masked_image, cv2.COLOR_BGR2LAB)
    thresh = cv2.inRange(image_lab, (255,128,128), (255,128,128))
    #cv2.imwrite("{}straight_arrows_thresh.png".format(program_images_directory), thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=2:
        print("Geocar straightening reliability is False. Arrows are not straight enough to consider reliable. \n")
        #Return to original position when looking down
        pyautogui.moveTo(compass_cX, compass_cY-compass_radius)
        time.sleep(0.25)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight

    i=0
    num_straight_arrows=0
    threshold_area = 1700 #min expected size of an arrow after straightening (if the arrow is straight)
    if len(contours)>0:
        while(i<len(contours)):
            contour_area = cv2.contourArea(contours[i])
            #print("Contour area of arrow after straightening: {} \n".format(contour_area))
            if contour_area>=threshold_area:
                num_straight_arrows=num_straight_arrows+1
            i=i+1
    else:
        print("Geocar straightening reliability is False. No arrows found after straightening. \n")
        #Return to original position when looking down
        pyautogui.moveTo(compass_cX, compass_cY-compass_radius)
        time.sleep(0.25)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight

   #If number of straight arrows is equal to 2, then it is reliable. Otherwise it is not reliable.
    if num_straight_arrows==2:
        reliable=True
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight
    else:
        print("Geocar straightening reliability is False. At least one arrow isn't straight enough. \n")
        #Return to original position when looking down
        pyautogui.moveTo(compass_cX, compass_cY-compass_radius)
        time.sleep(0.25)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
        reliable=False
        x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
        return reliable, x_compass_straight, y_compass_straight

    reliable=False
    x_compass_straight, y_compass_straight = pyautogui.position() #get current orientation of compass
    return reliable, x_compass_straight, y_compass_straight

#Determines if the country is Japan using a neat trick regarding the size of the arrows in Google Streetview (Note: Should already be looking down before calling this function).
def determine_if_japan(blur, geocar_straight_is_reliable):

    japan_blur="Unknown"
    japan_arrow_threshold_area=45000
    min_arrow_threshold_area=10000
    japan_threshold_blur = 70

    if blur<=0:
        japan_blur="Unknown"
        return japan_blur

    time.sleep(0.1)
    pyautogui.moveTo(1284, 470) #random location on geoguessr game-screen
    time.sleep(0.5)
    pyautogui.moveTo(default_width/2, 778) #puts cursor near middle of screen so large arrow is visible
    time.sleep(2)
    screenshot("large_arrow")

    image = cv2.imread("{}screenshot_large_arrow.png".format(program_images_directory), cv2.IMREAD_COLOR)
    image_copy=image.copy()

    #polygons = np.array([[(981, 666), (981, 491), (1163, 295), (1345, 491), (1345, 666), (1163, 491)]])
    circle_mask = np.zeros_like(image) 
    cv2.circle(circle_mask, (1280-int(trim_x_1), 800-int(trim_y_1)), 245, (255, 255, 255), thickness=-1)
    image = cv2.bitwise_and(image, circle_mask)

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    thresh = cv2.inRange(image_lab, (80,127,124), (131,130,133))
    cv2.imwrite("{}thresh_arrow.png".format(program_images_directory), thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    i=0
    filtered_contours = []
    #print("Circle contours length: {} \n".format(len(contours)))
    
    if len(contours)>0:
        while(i<len(contours)):
            if cv2.contourArea(contours[i])>min_arrow_threshold_area:
                filtered_contours.append(contours[i])
            i=i+1
    else:
        japan_blur="Unknown"
        return japan_blur

    #print("Circle filtered_contours length: {} \n".format(len(filtered_contours)))

    if len(filtered_contours)==1:
        contour_area = cv2.contourArea(filtered_contours[0])
        #print("Circle contour area: {} \n".format(contour_area))
        if (contour_area>=japan_arrow_threshold_area) and (blur<=japan_threshold_blur):
            japan_blur="True"
        else:
            japan_blur="False"
    elif len(filtered_contours)>1:
        i=0
        while i<len(filtered_contours):
            if  (cv2.contourArea(filtered_contours[i])>=japan_arrow_threshold_area) and (blur<=japan_threshold_blur):
                japan_blur="True" #technically not true, but very likely 
            else:
                japan_blur="False"
    else:
        japan_blur="Unknown" #technically it could still be Japan, but just very unlikely if len(filtered_contours)==0. 
    
    #Save an image of all the filtered contours
    image_contours = cv2.drawContours(image_copy, filtered_contours, -1, (255, 0, 0), 2)
    cv2.circle(image_contours, (1280-int(trim_x_1), 800-int(trim_y_1)), 245, (0, 255, 0), thickness=1)   
    cv2.imwrite("{}image_contours.png".format(program_images_directory), image_contours)

    return japan_blur

#Given input text, this program will determine what language it is.
def language_identification(text):

    print("Commencing Language Identification... \n")

    #Filter out special characters
    text=text.translate({ord(i):None for i in '!@#$£%^—&©€*()_+=~`<>,.?/:;\"\'{[}]\|'})

    #Filter out numbers
    text = ''.join(i for i in text if not i.isdigit())

    #Remove the word "Google" (to ignore water marks)
    text=text.replace('Google', '')

    #Gets rid of spaces to the left
    text = text.lstrip()

    #Gets rid of spaces to the right
    text = text.rstrip()

    #Replaces multiple spaces with single spaces
    text = ' '.join(text.split())

    print("Reformated Text: {} \n".format(text))

    textblob_lang = ""

    #if the text has more than 3 characters (not including whitespace), determine what language it is
    if ((len(text))-(text.count(" ")))>=3:
        b = TextBlob(text)
        textblob_lang=b.detect_language()
        print("FastText: {} \n".format(model.predict(text, k=20)))
        print("TextBlob Language: {} \n".format(textblob_lang))
    else: 
        language="Unknown"
    
    fasttext_top_lang = model.predict(text, k=20)[0][0]
    fasttext_top_lang = fasttext_top_lang.replace('__label__', '')

    if fasttext_top_lang==textblob_lang:
        if fasttext_top_lang=="yi":
            language="iw"
        else:
            language = textblob_lang
    elif fasttext_top_lang=="he" and textblob_lang=="iw":
        #Language is hebrew
        language="iw"
    else:
        language="Unknown"

    #maybe should return language but also the confidence level of tesseract associated with the text
    return language

#Used by the determine_language function to determine the basic bounding box for detected text in an image.
def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < min_conf:
                continue
            
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            
            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            p1 = (-sin * h + endX, -cos * h +endY)
            p3 = (-cos * w + endX, sin * w +endY)
            center = (0.5*(p1[0]+p3[0]), 0.5*(p1[1]+p3[1]))
            
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((center, (w,h), -1*angle * 180.0 / math.pi))
            confidences.append(float(scoresData[x]))
    
    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)

#Rotates an input image around a specified point by an angle (given in degrees) counter-clockwise.
def rotate_image(image, angle, image_center=None):
  #accepts angle in degrees and rotates CCW
  if image_center is None:
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

#Rotates a point around another point by an angle (given in degrees) clockwise.
def rotate_point(pointX, pointY, originX, originY, angle):
    #rotates CW and accepts degrees for angle (which it then converts to radians)
    angle=angle*(math.pi/180.0)
    x = originX + ((math.cos(angle)*(pointX-originX))-(math.sin(angle)*(pointY-originY))) 
    y = originY + ((math.sin(angle)*(pointX-originX))+(math.cos(angle)*(pointY-originY)))
    return x, y

def determine_language(filename):
    #Important: The EAST text requires that your input image dimensions be multiples of 32, so if you choose to adjust your width and height  values, make sure they are multiples of 32!
    
    rotated=False
    error=False
    min_conf=0.5
    min_word_conf=79 #percentage
    padding = 0.01

    print("\n")
    print("Text Detection For {}".format(filename))
    print("________________________________________________________________ \n")
    
    image = cv2.imread("{}{}".format(program_images_directory, filename))
    orig = image.copy()
    not_rotated = image.copy()
    rotate = image.copy()
    temp = image.copy()
    (origH, origW) = image.shape[:2]

    width=int(int((origW/32))*32) #makes width of image as a multiple of 32 
    height=int(int((origH/32))*32) #makes height of image as a multiple of 32 

    #Set the new width and height and then determine the ratio in change for both the width and height
    (newW, newH) = (width, height)
    rW = origW / float(newW)
    rH = origH / float(newH)

    #Resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    #Define the two output layer names for the EAST detector model that we are interested in -- the first is the output probabilities and the
    #second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    #Load the pre-trained EAST text detector
    net = cv2.dnn.readNet("C:\\Users\\Andrew Callam\\Downloads\\OpenCV\\Geoguessr\\frozen_east_text_detection.pb")

    #Construct a blob from the image and then perform a forward pass of the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    #Decode the predictions, then  apply non-maxima suppression to suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = rects

    #Initialize the list of results
    results = []

    #Loop over the bounding boxes
    i=0
    while(i<len(boxes)):
        vertices = cv2.boxPoints(boxes[i]) #get 4 corners of the rotated rect
        #Scale the bounding box coordinates based on the respective ratios
        for j in range(4):
                vertices[j][0] *= rW
                vertices[j][1] *= rH
        vertices = np.int0(vertices)
        cv2.drawContours(temp,[vertices],0,(255,105,180),-1)
        i=i+1

    #cv2.imshow("TEMP", temp)
    thresh = cv2.inRange(temp, (255,105,180), (255,105,180))
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    i=0
    while(i<len(contours)): 
        min_rect = cv2.minAreaRect(contours[i])
        #print("Rect. Area: {} \n".format((min_rect[1][0])*(min_rect[1][1])))
        #print("Rect. Aspect Ratio (w/h): {} \n".format((min_rect[1][0])/(min_rect[1][1])))
        box = cv2.boxPoints(min_rect)
        box = np.int0(box)
        cv2.drawContours(orig,[box],0,(0,255,0),1)
        if min_rect[2] != 0 and min_rect[2] != 90:
            #If statements check which way the rects. are roughly oriented
            if box[3][0]>box[1][0]: #if the point with the greatest y-coordinate on the rect. is further right than the point with the lowest y-coordinate on the rect. then do the following
                #Must rotate image CCW to straighten text (rotate min_rect[2] CCW)
                rotated_image=rotate_image(rotate, min_rect[2], min_rect[0])
                rot_x1, rot_y1 = rotate_point(box[1][0], box[1][1], min_rect[0][0], min_rect[0][1], -1.0*(min_rect[2])) 
                rot_x2, rot_y2 = rotate_point(box[3][0], box[3][1], min_rect[0][0], min_rect[0][1], -1.0*(min_rect[2]))
                rot_y1=int(round(rot_y1))
                rot_y2=int(round(rot_y2))
                rot_x1=int(round(rot_x1))
                rot_x2=int(round(rot_x2))

                dX = int((rot_x2 - rot_x1) * padding)
                dY = int((rot_y2 - rot_y1) * padding)

                #Apply padding to each side of the bounding box, respectively
                rot_x1 = max(0, rot_x1 - dX)
                rot_y1 = max(0, rot_y1 - dY)
                rot_x2 = min(origW, rot_x2 + (dX * 2))
                rot_y2 = min(origH, rot_y2 + (dY * 2))
            
                rotated=True
                roi = rotated_image[rot_y1:rot_y2, rot_x1:rot_x2]

                #cv2.rectangle(rotated_image,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
                #cv2.imshow("Rotated {}".format(i), roi) 
            elif box[3][0]<box[1][0]: #if the point with the greatest y-coordinate on the rect. is further left than the point with the lowest y-coordinate on the rect. then do the following
                #Must rotate image CW to striaghten text (rotate 90-min_rect[2] CW)
                rotated_image=rotate_image(rotate, (-1.0*(90-min_rect[2])), min_rect[0])
                rot_x1, rot_y1 = rotate_point(box[0][0], box[0][1], min_rect[0][0], min_rect[0][1], (90-(min_rect[2]))) 
                rot_x2, rot_y2 = rotate_point(box[2][0], box[2][1], min_rect[0][0], min_rect[0][1], (90-(min_rect[2])))
                rot_y1=int(round(rot_y1))
                rot_y2=int(round(rot_y2))
                rot_x1=int(round(rot_x1))
                rot_x2=int(round(rot_x2))
            
                dX = int((rot_x2 - rot_x1) * padding)
                dY = int((rot_y2 - rot_y1) * padding)

                #Apply padding to each side of the bounding box, respectively
                rot_x1 = max(0, rot_x1 - dX)
                rot_y1 = max(0, rot_y1 - dY)
                rot_x2 = min(origW, rot_x2 + (dX * 2))
                rot_y2 = min(origH, rot_y2 + (dY * 2))

                rotated=True
                roi = rotated_image[rot_y1:rot_y2, rot_x1:rot_x2]

                #cv2.rectangle(rotated_image,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
                #cv2.imshow("Rotated {}".format(i), roi) 
            elif box[3][0]==box[1][0]: #if the rect. is at 45 degrees
                if box[2][1]>box[0][1]: #if the point furthest right on the rect. has a greater y-coordinate than the point furthest right, then rotate the text CCW
                    rotated_image=rotate_image(rotate, min_rect[2], min_rect[0])
                    rot_x1, rot_y1 = rotate_point(box[1][0], box[1][1], min_rect[0][0], min_rect[0][1], -1.0*(min_rect[2])) 
                    rot_x2, rot_y2 = rotate_point(box[3][0], box[3][1], min_rect[0][0], min_rect[0][1], -1.0*(min_rect[2]))
                    rot_y1=int(round(rot_y1))
                    rot_y2=int(round(rot_y2))
                    rot_x1=int(round(rot_x1))
                    rot_x2=int(round(rot_x2))
                
                    dX = int((rot_x2 - rot_x1) * padding)
                    dY = int((rot_y2 - rot_y1) * padding)

                    #Apply padding to each side of the bounding box, respectively
                    rot_x1 = max(0, rot_x1 - dX)
                    rot_y1 = max(0, rot_y1 - dY)
                    rot_x2 = min(origW, rot_x2 + (dX * 2))
                    rot_y2 = min(origH, rot_y2 + (dY * 2))

                    rotated=True
                    roi = rotated_image[rot_y1:rot_y2, rot_x1:rot_x2]

                    #cv2.rectangle(rotated_image,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
                    #cv2.imshow("Rotated {}".format(i), roi) 
                elif box[2][1]<box[0][1]: #if the point furthest right on the rect. has a greater y-coordinate than the point furthest right, then rotate the text CW
                    rotated_image=rotate_image(rotate, (-1.0*(90-min_rect[2])), min_rect[0])
                    rot_x1, rot_y1 = rotate_point(box[0][0], box[0][1], min_rect[0][0], min_rect[0][1], (90-(min_rect[2]))) 
                    rot_x2, rot_y2 = rotate_point(box[2][0], box[2][1], min_rect[0][0], min_rect[0][1], (90-(min_rect[2])))
                    rot_y1=int(round(rot_y1))
                    rot_y2=int(round(rot_y2))
                    rot_x1=int(round(rot_x1))
                    rot_x2=int(round(rot_x2))
                
                    dX = int((rot_x2 - rot_x1) * padding)
                    dY = int((rot_y2 - rot_y1) * padding)

                    #Apply padding to each side of the bounding box, respectively
                    rot_x1 = max(0, rot_x1 - dX)
                    rot_y1 = max(0, rot_y1 - dY)
                    rot_x2 = min(origW, rot_x2 + (dX * 2))
                    rot_y2 = min(origH, rot_y2 + (dY * 2))

                    rotated=True
                    roi = rotated_image[rot_y1:rot_y2, rot_x1:rot_x2]

                    #cv2.rectangle(rotated_image,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
                    #cv2.imshow("Rotated {}".format(i), roi) 
            else: #the rect. is at 45 degrees and is a perfect square, probably best to ignore text like this since there is no real indication what is the best way to rotate it
                print("Error: Detected text bounding box is a perfect square at 45 degree angle, thus unable to determine which way to rotate text.")
                error=True
        elif min_rect[2] == 0: 
            rot_y1=int(round(box[1][1]))
            rot_y2=int(round(box[0][1]))
            rot_x1=int(round(box[0][0]))
            rot_x2=int(round(box[2][0]))
        
            dX = int((rot_x2 - rot_x1) * padding)
            dY = int((rot_y2 - rot_y1) * padding)

            #Apply padding to each side of the bounding box, respectively
            rot_x1 = max(0, rot_x1 - dX)
            rot_y1 = max(0, rot_y1 - dY)
            rot_x2 = min(origW, rot_x2 + (dX * 2))
            rot_y2 = min(origH, rot_y2 + (dY * 2))
        
            rotated=False
            roi = not_rotated[rot_y1:rot_y2, rot_x1:rot_x2]
            #cv2.rectangle(orig,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
            #cv2.imshow("Not Rotated {}".format(i), roi) 
        elif min_rect[2] == 90:
            rot_y1=int(round(box[0][1]))
            rot_y2=int(round(box[2][1]))
            rot_x1=int(round(box[0][0]))
            rot_x2=int(round(box[2][0]))
        
            dX = int((rot_x2 - rot_x1) * padding)
            dY = int((rot_y2 - rot_y1) * padding)

            #Apply padding to each side of the bounding box, respectively
            rot_x1 = max(0, rot_x1 - dX)
            rot_y1 = max(0, rot_y1 - dY)
            rot_x2 = min(origW, rot_x2 + (dX * 2))
            rot_y2 = min(origH, rot_y2 + (dY * 2))

            rotated=False
            roi = not_rotated[rot_y1:rot_y2, rot_x1:rot_x2]
        
            #cv2.rectangle(orig,(rot_x1, rot_y1),(rot_x2,rot_y2),(0,255,0),1)
            #cv2.imshow("Not Rotated {}".format(i), roi) 
        else:
            print("Error: Unable to determine how to rotate the detected text.")
            error=True
            
        #print("i={} \n {} \n angle: {} \n".format(i, box, min_rect[2]))       
        i=i+1

        if not error:

            #cv2.imshow("Rotated {}".format(i), roi) 

            tesseract_data = pytesseract.image_to_data(roi, config=config, output_type=Output.DICT)

            conf_tess=tesseract_data['conf']
            if int(conf_tess[0])==-1 and len(conf_tess)==1:
                padding=0.05
                #print("\n Padding Increase to 5% \n")

                dX = int((rot_x2 - rot_x1) * padding)
                dY = int((rot_y2 - rot_y1) * padding)

                #Apply padding to each side of the bounding box, respectively
                rot_x1 = max(0, rot_x1 - dX)
                rot_y1 = max(0, rot_y1 - dY)
                rot_x2 = min(origW, rot_x2 + (dX * 2))
                rot_y2 = min(origH, rot_y2 + (dY * 2))

                if rotated==True:
                    roi = rotated_image[rot_y1:rot_y2, rot_x1:rot_x2]
                if rotated == False:
                    roi = not_rotated[rot_y1:rot_y2, rot_x1:rot_x2]

                tesseract_data = pytesseract.image_to_data(roi, config=config, output_type=Output.DICT)

            padding=0.01
            rotated=False
            #Add the bounding box coordinates and OCR'd text to the list  of results
            results.append(((rot_x1, rot_y1, rot_x2, rot_y2), tesseract_data))
    
        error=False

    #Show detected text
    #cv2.imshow("Text Detection {}".format(filename), orig)
    cv2.imwrite("{}Text Detection {}".format(program_images_directory, filename), orig)

    languages=[]
    #Loop over the results
    for ((rot_x1, rot_y1, rot_x2, rot_y2), tesseract_data) in results:
        
        conf_tess=tesseract_data['conf']
        text_tess=tesseract_data['text']

        if not ((int(conf_tess[0])==-1 and len(conf_tess)==1) or (conf_tess==['-1', '-1', '-1', '-1', 95] and text_tess==['', '', '', '', ''])):

            print("OCR TEXT")
            print("_________ \n")

            #Tesseract confidence adjusted text
            i=0
            conf_text=""
            while i<len(conf_tess):
        
                word_conf=int(conf_tess[i])

                if word_conf>=min_word_conf:
                    conf_text = conf_text + text_tess[i] + " "
                i=i+1
    
            i=0
            print("conf_text: {} \n".format(conf_text))
            lang=language_identification(conf_text)
            if lang!="Unknown":
                languages.append(lang)
            print("\nLanguage Detected: {} \n".format(lang))
            print("Tesseract Data Text: \n {} \n".format(tesseract_data['text']))
            print("Tesseract Data Conf: \n {} \n".format(tesseract_data['conf']))

    return languages

#Test function (not used by program... yet).
def red_light():
    
    image_hsv = cv2.cvtColor(geocar_image, cv2.COLOR_BGR2HSV)
    red_light_polygon = np.array([[(1054, 350), (1054, 160), (1284, 160), (1284, 350)]])
    red_light_mask = np.zeros_like(image_hsv)
    cv2.fillPoly(red_light_mask, red_light_polygon, (255, 255, 255))

    red_light_masked_image = cv2.bitwise_and(image_hsv, red_light_mask)
    
    red_light_thresh = cv2.inRange(red_light_masked_image, (0,30,115), (10,90,160))

    cv2.imwrite("{}red_light_thresh_{}.png".format(program_images_directory, turn), red_light_thresh)

    red_light_contours, red_light_hierarchy = cv2.findContours(red_light_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    i=0
    min_red_light_contour_area=0
    red_light_total_area=0

    red_light_filtered_contours = []
    red_light_filtered_contours_areas = []
    red_light_contours_length=len(red_light_contours)
            
    if red_light_contours_length>0:
        while(i<red_light_contours_length):
            red_light_contour_area=cv2.contourArea(red_light_contours[i])
            if red_light_contour_area>min_red_light_contour_area:
                red_light_filtered_contours.append(red_light_contours[i])
                red_light_filtered_contours_areas.append(red_light_contour_area)
                red_light_total_area=red_light_total_area+red_light_contour_area
            i=i+1
            
    print("Red Light Contour Areas (turn #{}): {} \n".format(turn, red_light_filtered_contours_areas))

    cv2.drawContours(geocar_image, red_light_filtered_contours, -1, (0, 0, 255), 1)
    cv2.drawContours(geocar_image, aerial_polygon, -1, (255, 0, 0), 1) 
    cv2.drawContours(geocar_image, red_light_polygon, -1, (0, 0, 255), 1) 
    cv2.imwrite("{}geocar_image_{}.png".format(program_images_directory, turn), geocar_image)

    print("ADAPTIVE Long Aerial Total Area: {} \n".format(aerial_total_area))
    print("Red Light Total Area: {} \n".format(red_light_total_area))

#Determines the geocar type assuming the geocar has been straightened (if possible) and the camera is already looking down.
def determine_geocar(geocar_straight_is_reliable, x_compass_straight, y_compass_straight):
   
    geocar="Unknown" 
    compass_cX = 65.5 #65.5
    compass_cY = 996.5 #966.5
    aerial_length_1=0
    aerial_length_2=0
    long_aerial_length_min=8.5
    long_aerial_length_max = 15
    short_aerial_length_min=2
    aerial="Nothing"
    
    if geocar_straight_is_reliable:
        print("Determining Geocar type... \n")
        
        #Look up slightly
        drag(x=default_width/2, y=460, dist_x=0, dist_y=375, time=1)

        #Check for aerial and red light
        turn=1
        while turn<3:
            geocar="Nothing"
            
            screenshot(identifier="geocar_check_{}".format(turn))
            geocar_image = cv2.imread("{}screenshot_geocar_check_{}.png".format(program_images_directory, turn), cv2.IMREAD_COLOR)
            geocar_image_copy = geocar_image.copy()
            geocar_image_copy2 = geocar_image.copy()

            image_gray = cv2.cvtColor(geocar_image, cv2.COLOR_BGR2GRAY)
            image_lab = cv2.cvtColor(geocar_image, cv2.COLOR_BGR2LAB)
            image_hsv = cv2.cvtColor(geocar_image, cv2.COLOR_BGR2HSV)
            
            aerial_polygon = np.array([[(1040, 250), (1040, 30), (1220, 30), (1220, 250)]])
            #car_back_polygon = np.array([[(938, 120), (1370, 120), (1370, 230), (938, 230)]]) old
            car_back_polygon = np.array([[(938, 120), (1370, 120), (1370, 270), (938, 270)]])
            sample_roi_polygon = np.array([[(1000, 50), (1300, 50), (1300, 110), (1000, 110)]])
            blue_car_back_polygon = np.array([[(1000, 180), (1335, 180), (1335, 270), (1000, 270)]])
            blue_sample_roi_polygon = np.array([[(1000, 300), (1335, 300), (1335, 350), (1000, 350)]])
            
            blank_black_image = np.zeros_like(image_gray)
            blank_black_image_black_car = blank_black_image.copy()
            blank_black_image_white_car = blank_black_image.copy()
            blank_black_image_blue_car = blank_black_image.copy()
            aerial_mask = np.zeros_like(image_gray)  
            
            cv2.fillPoly(aerial_mask, aerial_polygon, (255, 255, 255))
            
            aerial_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
            aerial_thresh = cv2.bitwise_not(aerial_thresh)

            aerial_masked_image = cv2.bitwise_and(aerial_thresh, aerial_mask)
            
            cv2.imwrite("{}aerial_thresh_{}.png".format(program_images_directory, turn), aerial_masked_image)

            aerial_contours = cv2.findContours(aerial_masked_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            aerial_contours = aerial_contours[0] if len(aerial_contours) == 2 else aerial_contours[1]

            i=0
            aerial_total_area = 0
            min_aerial_contour_area = 10
            max_aerial_contour_area = 250
            min_aspect_ratio = 7.9 #7.9 (consider lowering to 4-4.5?)
            
            aerial_filtered_contours = []
            aerial_filtered_contours_areas = []
            aerial_contours_length=len(aerial_contours)
            
            if aerial_contours_length>0:
                while(i<aerial_contours_length):
                   _,_,w,h = cv2.boundingRect(aerial_contours[i])
                   aspect_ratio = float(h)/float(w)
                   aerial_contour_area=cv2.contourArea(aerial_contours[i])
                   if (aerial_contour_area>min_aerial_contour_area) and (aspect_ratio>min_aspect_ratio) and (aerial_contour_area<max_aerial_contour_area):
                        aerial_filtered_contours.append(aerial_contours[i])
                        aerial_filtered_contours_areas.append(cv2.contourArea(aerial_contours[i]))
                        aerial_total_area=aerial_total_area+aerial_contour_area
                        #print("Aspect Ratio: {}".format(aspect_ratio))
                   i=i+1
            
            #print("Adaptive Threshold Long Aerial Contour Areas (turn #{}): {} \n".format(turn, aerial_filtered_contours_areas))
            
            aerial_filtered_thresh = cv2.drawContours(blank_black_image, aerial_filtered_contours, -1, (255, 255, 255), 1)
            cv2.imwrite("{}aerial_filtered_thresh_{}.png".format(program_images_directory, turn), aerial_filtered_thresh)

            #If there are multiple contours after filtering, combine their centroids with a line, and treat the resulting shape as a new contour.
            i=0
            aerial_contour_centroids = []
            if len(aerial_filtered_contours)>1:
                while i<len(aerial_filtered_contours):
                    M_0 = cv2.moments(aerial_filtered_contours[i])
                    if M_0["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
                        aerial_contour_cX = int(M_0["m10"] / M_0["m00"])
                        aerial_contour_cY = int(M_0["m01"] / M_0["m00"])
                        aerial_contour_centroids.append((aerial_contour_cX, aerial_contour_cY))
                    i=i+1

                i=0
                while i<((len(aerial_contour_centroids))-1):
                    cv2.line(aerial_filtered_thresh, aerial_contour_centroids[i], aerial_contour_centroids[i+1], (255, 255, 255), 1)
                    i=i+1
            
                aerial_contours = cv2.findContours(aerial_filtered_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                aerial_contours = aerial_contours[0] if len(aerial_contours) == 2 else aerial_contours[1]

                i=0
                aerial_filtered_contours = []
                aerial_filtered_contours_areas = []
                aerial_contours_length=len(aerial_contours)
                if aerial_contours_length>0:
                    while(i<aerial_contours_length):
                       _,_,w,h = cv2.boundingRect(aerial_contours[i])
                       aspect_ratio = float(h)/float(w)
                       aerial_contour_area=cv2.contourArea(aerial_contours[i])
                       if (aerial_contour_area>min_aerial_contour_area) and (aspect_ratio>min_aspect_ratio) and (aerial_contour_area<max_aerial_contour_area):
                            aerial_filtered_contours.append(aerial_contours[i])
                            aerial_filtered_contours_areas.append(cv2.contourArea(aerial_contours[i]))
                            aerial_total_area=aerial_total_area+aerial_contour_area
                            #print("Aspect Ratio: {}".format(aspect_ratio))
                       i=i+1
            
            #Find the smallest and largest x and y values in the filtered contours (in order to calculate the length of the contour)
            hypotenuse=0
            if len(aerial_filtered_contours)>0:
                c = max(aerial_filtered_contours, key=cv2.contourArea)
                left = tuple(c[c[:, :, 0].argmin()][0])
                right = tuple(c[c[:, :, 0].argmax()][0])
                top = tuple(c[c[:, :, 1].argmin()][0])
                bottom = tuple(c[c[:, :, 1].argmax()][0])

                #Calculate hypotenuse
                hypotenuse=math.sqrt(((right[0]-left[0])^2)+((bottom[1]-top[1])^2))
                print("Aerial Hypotenuse: {} \n".format(hypotenuse))

            else:
                hypotenuse=0

            #print("Aerial pixel length: {} \n".format(hypotenuse))

            cv2.imwrite("{}aerial_filtered_thresh_line_{}.png".format(program_images_directory, turn), aerial_filtered_thresh)

            #print("ADAPTIVE Long Aerial Total Area: {} \n".format(aerial_total_area))

            #Check for white car back

            sample_roi=image_lab[50:110, 1000:1300]
            avg_color_per_row = np.average(sample_roi, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            print("Average Colour: {}".format(avg_color))
            avg_brightness_of_road=avg_color[0]

            white_car_mask = np.zeros_like(image_gray)  

            cv2.fillPoly(white_car_mask, car_back_polygon, (255, 255, 255))

            white_car_thresh=cv2.inRange(image_lab, (min(avg_brightness_of_road+15, 250), 120, 120), (min(255, avg_brightness_of_road+50), 140, 140))
            #white_car_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -15)

            white_car_masked_image = cv2.bitwise_and(white_car_thresh, white_car_mask)

            cv2.imwrite("{}white_car_thresh_{}.png".format(program_images_directory, turn), white_car_masked_image)

            white_car_contours = cv2.findContours(white_car_masked_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            white_car_contours = white_car_contours[0] if len(white_car_contours) == 2 else white_car_contours[1]

            i=0
            white_car_total_area = 0
            min_white_car_contour_area = 10000 #20000
            max_white_car_contour_area = 100000
            min_white_car_aspect_ratio = 3 #3
            
            white_car_filtered_contours = []
            white_car_filtered_contours_areas = []
            white_car_contours_length=len(white_car_contours)
            
            if white_car_contours_length>0:
                while(i<white_car_contours_length):
                   _,_,w,h = cv2.boundingRect(white_car_contours[i])
                   white_car_aspect_ratio = float(w)/float(h)
                   white_car_contour_area=cv2.contourArea(white_car_contours[i])
                   if (white_car_contour_area>min_white_car_contour_area) and (white_car_aspect_ratio>min_white_car_aspect_ratio) and (white_car_contour_area<max_white_car_contour_area):
                        white_car_filtered_contours.append(white_car_contours[i])
                        white_car_filtered_contours_areas.append(cv2.contourArea(white_car_contours[i]))
                        white_car_total_area=white_car_total_area+white_car_contour_area
                        #print("Aspect Ratio: {} \n".format(white_car_aspect_ratio))
                   i=i+1
            #print("White Car Area (turn #{}): {} \n".format(turn, white_car_filtered_contours_areas))

            white_car_filtered_thresh = cv2.drawContours(blank_black_image_white_car, white_car_filtered_contours, -1, (255, 255, 255), 1)
            cv2.imwrite("{}white_car_filtered_thresh_{}.png".format(program_images_directory, turn), white_car_filtered_thresh)

            #Check for black car back
            black_car_mask = np.zeros_like(image_gray)  

            cv2.fillPoly(black_car_mask, car_back_polygon, (255, 255, 255))

            black_car_thresh=cv2.inRange(image_lab, (max(0, avg_brightness_of_road-70), 120, 120), (max(0, avg_brightness_of_road-10), 140, 140))
            #black_car_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 29, 13)
            #black_car_thresh = cv2.bitwise_not(black_car_thresh)

            black_car_masked_image = cv2.bitwise_and(black_car_thresh, black_car_mask)

            cv2.imwrite("{}black_car_thresh_{}.png".format(program_images_directory, turn), black_car_masked_image)

            black_car_contours = cv2.findContours(black_car_masked_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            black_car_contours = black_car_contours[0] if len(black_car_contours) == 2 else black_car_contours[1]

            i=0
            black_car_total_area = 0
            min_black_car_contour_area = 10000 #20000
            max_black_car_contour_area = 100000
            min_black_car_aspect_ratio = 3 #3
            
            black_car_filtered_contours = []
            black_car_filtered_contours_areas = []
            black_car_contours_length=len(black_car_contours)
            
            if black_car_contours_length>0:
                while(i<black_car_contours_length):
                   _,_,w,h = cv2.boundingRect(black_car_contours[i])
                   black_car_aspect_ratio = float(w)/float(h)
                   black_car_contour_area=cv2.contourArea(black_car_contours[i])
                   if (black_car_contour_area>min_black_car_contour_area) and (black_car_aspect_ratio>min_black_car_aspect_ratio) and (black_car_contour_area<max_black_car_contour_area):
                        black_car_filtered_contours.append(black_car_contours[i])
                        black_car_filtered_contours_areas.append(cv2.contourArea(black_car_contours[i]))
                        black_car_total_area=black_car_total_area+black_car_contour_area
                        #print("Aspect Ratio: {} \n".format(black_car_aspect_ratio))
                   i=i+1
            #print("Black Car Area (turn #{}): {} \n".format(turn, black_car_filtered_contours_areas))

            black_car_filtered_thresh = cv2.drawContours(blank_black_image_black_car, black_car_filtered_contours, -1, (255, 255, 255), 1)
            cv2.imwrite("{}black_car_filtered_thresh_{}.png".format(program_images_directory, turn), black_car_filtered_thresh)

            white_contour_cY=0
            black_contour_cY=0
            if len(black_car_filtered_contours)>0 and len(white_car_filtered_contours)>0:
                M_0 = cv2.moments(white_car_filtered_contours[0])
                M_1 = cv2.moments(black_car_filtered_contours[0])
                if M_0["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
                    white_contour_cY = int(M_0["m01"] / M_0["m00"])

                if M_1["m00"] != 0: #to avoid dividing by zero, first make sure M["m00"] is not equal to zero
                    black_contour_cY = int(M_1["m01"] / M_1["m00"])
            
                if white_contour_cY>black_contour_cY:
                    geocar="White"
                elif white_contour_cY<black_contour_cY:
                    geocar="Black"
            elif len(black_car_filtered_contours)>0:
                geocar="Black"
            elif len(white_car_filtered_contours)>0:
                geocar="White"
            
            #Check for blue car back
            sample_roi=image_hsv[300:350, 1000:1335]
            avg_color_per_row = np.average(sample_roi, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            #print("Average Colour: {}".format(avg_color))
            avg_saturation_of_road=avg_color[1]


            blue_car_mask = np.zeros_like(image_gray)  

            cv2.fillPoly(blue_car_mask, blue_car_back_polygon, (255, 255, 255))

            #blue_car_thresh=cv2.inRange(image_hsv, (100, max(avg_saturation_of_road+25, 60), 130), (130, 255, 255))
            blue_car_thresh=cv2.inRange(image_hsv, (100, 60, 130), (130, 255, 255))

            blue_car_masked_image = cv2.bitwise_and(blue_car_thresh, blue_car_mask)

            cv2.imwrite("{}blue_car_thresh_{}.png".format(program_images_directory, turn), blue_car_masked_image)

            blue_car_contours = cv2.findContours(blue_car_masked_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            blue_car_contours = blue_car_contours[0] if len(blue_car_contours) == 2 else blue_car_contours[1]

            i=0
            blue_car_total_area = 0
            min_blue_car_contour_area = 50
            max_blue_car_contour_area = 100000
            #min_blue_car_aspect_ratio = 3 
            
            blue_car_filtered_contours = []
            blue_car_filtered_contours_areas = []
            blue_car_contours_length=len(blue_car_contours)
            
            if blue_car_contours_length>0:
                while(i<blue_car_contours_length):
                   _,_,w,h = cv2.boundingRect(blue_car_contours[i])
                   blue_car_aspect_ratio = float(w)/float(h)
                   blue_car_contour_area=cv2.contourArea(blue_car_contours[i])
                   if (blue_car_contour_area>min_blue_car_contour_area) and (blue_car_contour_area<max_blue_car_contour_area):
                        blue_car_filtered_contours.append(blue_car_contours[i])
                        blue_car_filtered_contours_areas.append(cv2.contourArea(blue_car_contours[i]))
                        blue_car_total_area=blue_car_total_area+blue_car_contour_area
                        #print("Aspect Ratio: {} \n".format(blue_car_aspect_ratio))
                   i=i+1
            
            #print("Blue Car Area (turn #{}): {} \n".format(turn, blue_car_filtered_contours_areas))

            blue_car_filtered_thresh = cv2.drawContours(blank_black_image_blue_car, blue_car_filtered_contours, -1, (255, 255, 255), 1)
            cv2.imwrite("{}blue_car_filtered_thresh_{}.png".format(program_images_directory, turn), blue_car_filtered_thresh)

            if geocar=="Nothing" and len(blue_car_filtered_contours)>0:
                geocar="Blue"
            elif (geocar=="White" or geocar=="Black") and len(blue_car_filtered_contours)>0:
                geocar="Unknown"
            
            if len(aerial_filtered_contours)>0:
                minRect = cv2.minAreaRect(aerial_filtered_contours[0])
                box = cv2.boxPoints(minRect)
                box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
                cv2.drawContours(geocar_image_copy, [box], 0, (0, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, aerial_filtered_contours, -1, (255, 0, 0), 1)
            #cv2.drawContours(geocar_image_copy, white_car_filtered_contours, -1, (0, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, black_car_filtered_contours, -1, (0, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, blue_car_filtered_contours, -1, (0, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, aerial_polygon, -1, (255, 0, 0), 1) 
            #cv2.drawContours(geocar_image_copy, car_back_polygon, -1, (0, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, sample_roi_polygon, -1, (100, 155, 100), 1) 
            #cv2.drawContours(geocar_image_copy, blue_sample_roi_polygon, -1, (255, 255, 0), 1)
            #cv2.drawContours(geocar_image_copy, blue_car_back_polygon, -1, (255, 255, 0), 1)
            cv2.imwrite("{}geocar_image_{}.png".format(program_images_directory, turn), geocar_image_copy)

            #print("Geocar (turn #{}): {}".format(turn, geocar))

            if turn==1:
                aerial_length_1=hypotenuse
                geocar_1=geocar
            if turn==2:
                aerial_length_2=hypotenuse
                geocar_2=geocar


            #Turn Around 180 degrees
            pyautogui.moveTo(compass_cX-(x_compass_straight-compass_cX), compass_cY-(y_compass_straight-compass_cY))
            time.sleep(0.25)
            pyautogui.mouseDown() 
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)

            turn=turn+1
    
        #Determine aerial type based on length
        aerial_length=max(aerial_length_1, aerial_length_2) #if two aerials were found (one on either side of the geocar), assume the longest one to be the actual aerial
        if aerial_length>=long_aerial_length_min and aerial_length<=long_aerial_length_max:
            aerial="Long"
        elif (aerial_length<long_aerial_length_min) and (aerial_length>=short_aerial_length_min):
            aerial="Short"
        else:
            aerial="Nothing"

        print("Aerial Type: {} \n".format(aerial))

        #Determine geocar type 
        if geocar_1=="Nothing" and geocar_2=="Nothing":
            geocar="Nothing"
        elif (geocar_1=="White" and geocar_2=="Nothing") or (geocar_1=="Nothing" and geocar_2=="White") or (geocar_1=="White" and geocar_2=="White"):
            geocar="White"
        elif (geocar_1=="Black" and geocar_2=="Nothing") or (geocar_1=="Nothing" and geocar_2=="Black") or (geocar_1=="Black" and geocar_2=="Black"):
            geocar="Black"
        elif (geocar_1=="Blue" and geocar_2=="Nothing") or (geocar_1=="Nothing" and geocar_2=="Blue") or (geocar_1=="Blue" and geocar_2=="Blue"):
            geocar="Blue"
        else:
            print("More than one geocar type was detected. Thus, the detection is not reliable.\n")
            geocar="Unknown"

        print("Geocar Type: {} \n".format(geocar))

    else:
        print("Geocar type is unknown since geocar straightening was determined to be unreliable \n")
        geocar="Unknown"
        aerial="Unknown"

    return geocar, aerial

#Given clues as inputs, this country calculates the probability of every country, and then returns the country with the largest probability.
def determine_country_probabilities(hemisphere, camera_gen, japan_blur, aerial, geocar, languages):
    
    print("Determining Country Probabilities... \n")
    
    #Set error rates for each clue (in percentage DECIMAL)
    if hemisphere=="North":
        #hemisphere_er="#times it guessed Northern Hemisphere but it was actually Southern Hemisphere / #times it guessed Northern Hemisphere"
        hemisphere_er=0.02
    elif hemisphere=="South":
        #hemisphere_er="#times it guessed Southern Hemisphere but it was actually Nothern Hemisphere / #times it guessed Southern Hemisphere"
        hemisphere_er=0.17
    elif hemisphere=="Unknown":
        hemisphere="North"
        #hemisphere_er="#times it guessed Unknown when it was Southern Hemisphere / #times it guessed Unknown"
        hemisphere_er=0.23077

    if camera_gen=="Gen 1":
        #camera_gen_er="#times it guessed Gen 1 but it was something else/ #times it guessed Gen 1"
        camera_gen_er=0.00033
    elif camera_gen=="Gen 2":
        #camera_gen_er="#times it guessed Gen 2 but it was something else/ #times it guessed Gen 2"
        camera_gen_er=0.06
    elif camera_gen=="Gen 3 or 4":
        #camera_gen_er="#times it guessed Gen 3 or 4 but it was something else/ #times it guessed Gen 3 or 4"
        camera_gen_er=0.04
    else:
        camera_gen_er=0.5 #for when it is "Unknown", there must be a value assigned 

    if japan_blur=="True":
        #japan_blur_er="#times it guessed it was Japan (based on arrows and blur only) but it was something else/ #times it guessed it was Japan (based on arrows and blur only)"
        japan_blur_er=0.005
    elif japan_blur=="False":
        #japan_blur_er="#times it guessed it wasn't Japan (based on arrows and blur only) but it actually was Japan/ #times it guessed it wasn't Japan (based on arrows and blur only)"
        japan_blur_er=0.025
    else:
        japan_blur_er=0.5 #for when it is "Unknown", there must be a value assigned 

    if aerial=="Long":
        #aerial_er="#times it guessed there was a LONG aerial when there wasn't a LONG aerial / #times it guessed there was a LONG aerial"
        aerial_er=0.1
    elif aerial=="Short":
        #aerial_er="#times it guessed there was a SHORT aerial when there wasn't a SHORT aerial / #times it guessed there was a SHORT aerial"
        aerial_er=0.1
    elif aerial=="Nothing":
        aerial_er=0.1
        #aerial_er="#times it guessed there wasn't an aerial when there actually was / #times it guessed there was no aerial"
    else:
        aerial_er=0.5 #for when it is "Unknown", there must be a value assigned
    
    if geocar=="Nothing":
        #geocar_er="#times it guessed there was no specific geocar when there actually was (either white, black or blue though) / #times it guessed there was no specific geocar"
        geocar_er=0.03
    elif geocar=="White":
        #geocar_er="#times it guessed there was a white geocar when it wasn't actually white / #times it guessed there was a white geocar"
        geocar_er=0.1
    elif geocar=="Black":
        #geocar_er="#times it guessed there was a black geocar when it wasn't actually black / #times it guessed there was a black geocar"
        geocar_er=0.5
    elif geocar=="Blue":
        #geocar_er="#times it guessed there was a blue geocar when it wasn't actually blue / #times it guessed there was a blue geocar" 
        geocar_er=0.4
    else:
        geocar_er=0.5 #for when it is "Unknown", there must be a value assigned

    #Probabilties of different clues occuring in different countries
    country_clue_probabilities = {
    "USA": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 3.333, "Gen 2": 6.667, "Gen 3 or 4": 93.333}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 92.6, "White": 3, "Black": 0, "Blue": 4.4}, "Language": {"en": 100}},
    "Japan": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 100, "False": 0}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "France": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 15, "Gen 3 or 4": 85}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 20, "Nothing": 75}, "Geocar": {"Nothing": 85, "White": 0, "Black": 0, "Blue": 15}, "Language": {"fr": 100}},
    "Russia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 60, "Short": 35, "Nothing": 5}, "Geocar": {"Nothing": 95, "White": 0, "Black": 0, "Blue": 5}, "Language": {"ru": 100}},
    "UK": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 15, "Gen 3 or 4": 85}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 30, "Nothing": 65}, "Geocar": {"Nothing": 80, "White": 20, "Black": 0, "Blue": 0}, "Language": {"en": 100}}, 
    "South Africa": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 80, "Gen 3 or 4": 20}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 25, "White": 75, "Black": 0, "Blue": 0}, "Language": {"en": 50, "af": 50}},
    "Canada": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 10, "Gen 3 or 4": 90}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 93, "White": 0, "Black": 0, "Blue": 7}, "Language": {"en": 80, "fr": 20}},
    "Australia": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 5, "Gen 2": 10, "Gen 3 or 4": 90}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 30, "Short": 0, "Nothing": 70}, "Geocar": {"Nothing": 93, "White": 0, "Black": 0, "Blue": 7}, "Language": {"en": 100}},
    "Brazil": {"Hemisphere": {"North": 5, "South": 95}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 60, "Nothing": 40}, "Geocar": {"Nothing": 30, "White": 60, "Black": 0, "Blue": 10}, "Language": {"pt": 100}},
    "Finland": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 20, "Gen 3 or 4": 80}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"fi": 100}},
    "Spain": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 90, "White": 0, "Black": 0, "Blue": 10}, "Language": {"es": 100}},
    "Germany": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 100, "Gen 3 or 4": 0}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"de": 100}},
    "Mexico": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 2, "Gen 2": 0, "Gen 3 or 4": 98}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 30, "Nothing": 70}, "Geocar": {"Nothing": 95, "White": 0, "Black": 0, "Blue": 5}, "Language": {"es": 100}},
    "Chile": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 10, "Short": 0, "Nothing": 90}, "Geocar": {"Nothing": 5, "White": 95, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Norway": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 75, "White": 0, "Black": 0, "Blue": 25}, "Language": {"no": 100}},
    "Argentina": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 25, "White": 0, "Black": 70, "Blue": 5}, "Language": {"es": 100}},
    "Austria": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 30, "Nothing": 65}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"de": 100}},
    "India": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}}, 
    "Singapore": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Sweden": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 5, "Gen 3 or 4": 95}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"sv": 100}},
    "Thailand": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"th": 100}},
    "Ireland": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Italy": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 10, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"it": 100}},
    "Lithuania": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 15, "Short": 70, "Nothing": 15}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"lt": 100}},
    "Netherlands": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"nl": 100}},
    "Poland": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 20, "Short": 50, "Nothing": 30}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"po": 100}},
    "South Korea": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ko": 100}},
    "Taiwan": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 80, "False": 20}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Botswana": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 5, "White": 95, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Indonesia": {"Hemisphere": {"North": 5, "South": 95}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"id": 100}},
    "Malaysia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ma": 100}},
    "Peru": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 10, "White": 60, "Black": 30, "Blue": 0}, "Language": {"es": 100}},
    "Turkey": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"tr": 100}},
    "United Arab Emirates": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 20, "White": 80, "Black": 0, "Blue": 0}, "Language": {"ar": 50, "en": 50}},
    "Bangladesh": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Belgium": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"fr": 35, "en": 32.5, "nl": 32.5}},
    "Bolivia": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 10, "White": 90, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "China": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Colombia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 50, "Nothing": 50}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Costa Rica": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Croatia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 95, "Nothing": 5}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"hr": 100}},
    "Albania": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 95, "Nothing": 5}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"sq": 100}},
    "Andorra": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 95, "Nothing": 5}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}}, 
    "Bulgaria": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 50, "Short": 50, "Nothing": 0}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"bg": 100}},
    "Cambodia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 30, "Nothing": 70}, "Geocar": {"Nothing": 85, "White": 10, "Black": 5, "Blue": 0}},
    "Czechia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 50, "Short": 50, "Nothing": 0}, "Geocar": {"Nothing": 80, "White": 0, "Black": 0, "Blue": 20}, "Language": {"cs": 100}},
    "Denmark": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 10, "Short": 50, "Nothing": 40}, "Geocar": {"Nothing": 60, "White": 0, "Black": 0, "Blue": 40}, "Language": {"da": 100}},
    "Ecuador": {"Hemisphere": {"North": 40, "South": 60}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 70, "Nothing": 0}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Egypt": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ar": 90, "en": 10}},
    "Estonia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 90, "Nothing": 5}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Eswatini": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 70, "White": 30, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Ghana": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Greece": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 20, "Short": 50, "Nothing": 30}, "Geocar": {"Nothing": 90, "White": 0, "Black": 0, "Blue": 10}}, 
    "Hungary": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 30, "Short": 35, "Nothing": 35}, "Geocar": {"Nothing": 90, "White": 0, "Black": 0, "Blue": 10}, "Language": {"hu": 100}},
    "Iceland": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 30, "Short": 0, "Nothing": 80}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"is": 100}},
    "Israel": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 30, "Short": 30, "Nothing": 60}, "Geocar": {"Nothing": 50, "White": 0, "Black": 50, "Blue": 0}, "Language": {"iw": 100}},
    "Kenya": {"Hemisphere": {"North": 50, "South": 50}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Kyrgyzstan": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Lebanon": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ar": 100}},
    "Lesotho": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 10, "White": 90, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Malta": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 50, "Nothing": 50}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 90, "mt": 10}},
    "New Zealand": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 3, "Gen 2": 3, "Gen 3 or 4": 94}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 5, "Nothing": 90}, "Geocar": {"Nothing": 95, "White": 0, "Black": 0, "Blue": 5}, "Language": {"en": 100}},
    "Portugal": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 80, "Nothing": 15}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"pt": 100}},
    "Romania": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 40, "Short": 40, "Nothing": 20}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ro": 100}},
    "Senegal": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"fr": 100}},
    "Serbia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 5, "Short": 90, "Nothing": 5}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"sr": 100}},
    "Slovakia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 40, "Short": 40, "Nothing": 20}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"sk": 100}},
    "Slovenia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 1, "Short": 89, "Nothing": 10}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"sl": 100}},
    "Tunisia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"ar": 60, "fr": 40}},
    "Uganda": {"Hemisphere": {"North": 50, "South": 50}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"en": 100}},
    "Ukraine": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 80, "Short": 10, "Nothing": 10}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"uk": 100}},
    "Dominican Republic": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Latvia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 8, "Short": 90, "Nothing": 2}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"lv": 100}},
    "Uruguay": {"Hemisphere": {"North": 0, "South": 100}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 5, "White": 0, "Black": 95, "Blue": 0}, "Language": {"es": 100}},
    "Bhutan": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 10, "White": 90, "Black": 0, "Blue": 0}},
    "Guatemala": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"es": 100}},
    "Jordan": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 5, "White": 0, "Black": 95, "Blue": 0}, "Language": {"ar": 100}},
    "Laos": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Mongolia": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Philippines": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 50, "White": 50, "Black": 0, "Blue": 0}, "Language": {"en": 80, "es": 20}},
    "Sri Lanka": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}},
    "Switzerland": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 80, "False": 20}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}, "Language": {"fr": 70, "de": 30}},
    "Vietnam": {"Hemisphere": {"North": 100, "South": 0}, "Camera Gen": {"Gen 1": 0, "Gen 2": 0, "Gen 3 or 4": 100}, "Japan Blur": {"True": 0, "False": 100}, "Aerial": {"Long": 0, "Short": 0, "Nothing": 100}, "Geocar": {"Nothing": 100, "White": 0, "Black": 0, "Blue": 0}}
    }

    #Percent probability of each country
    country_probabilities = {
    "USA": 23.57,
    "Japan": 8.09,
    "France": 7.50,
    "Russia": 4.83,
    "UK": 5.03, 
    "South Africa": 2.47,
    "Canada": 4.44,
    "Australia": 2.66,
    "Brazil": 3.35,
    "Finland": 1.97,
    "Spain": 2.07,
    "Germany": 1.38,
    "Mexico": 2.07,
    "Chile": 1.18,
    "Norway": 1.48,
    "Argentina": 1.48,
    "Austria": 0.89,
    "India": 0.89, 
    "Singapore": 1.08,
    "Sweden": 1.87,
    "Thailand": 1.28,
    "Ireland": 0.39,
    "Italy": 1.38,
    "Lithuania": 0.39,
    "Netherlands": 0.59,
    "Poland": 1.28,
    "South Korea": 0.69,
    "Taiwan": 1.18,
    "Botswana": 0.20,
    "Indonesia": 0.79,
    "Malaysia": 0.59,
    "Peru": 0.59,
    "Turkey": 0.59,
    "United Arab Emirates": 0.30,
    "Bangladesh": 0.49,
    "Belgium": 0.49,
    "Bolivia": 0.30,
    "China": 0.49,
    "Colombia": 0.20,
    "Costa Rica": 0.10,
    "Croatia": 0.30,
    "Albania": 0.10,
    "Andorra": 0.10, 
    "Bulgaria": 0.20,
    "Cambodia": 0.10,
    "Czechia": 0.49,
    "Denmark": 0.20,
    "Ecuador": 0.20,
    "Egypt": 0.10,
    "Estonia": 0.30,
    "Eswatini": 0.10,
    "Ghana": 0.20,
    "Greece": 0.30, 
    "Hungary": 0.30,
    "Iceland": 0.10,
    "Israel": 0.99,
    "Kenya": 0.10,
    "Kyrgyzstan": 0.20,
    "Lebanon": 0.10,
    "Lesotho": 0.20,
    "Malta": 0.10,
    "New Zealand": 0.79,
    "Portugal": 0.49,
    "Romania": 0.39,
    "Senegal": 0.49,
    "Serbia": 0.10,
    "Slovakia": 0.20,
    "Slovenia": 0.10,
    "Tunisia": 0.20,
    "Uganda": 0.20,
    "Ukraine": 0.30,
    "Dominican Republic": 0.20,
    "Latvia": 0.10,
    "Uruguay": 0.20,
    "Bhutan": 0.10,
    "Guatemala": 0.10,
    "Jordan": 0.10,
    "Laos": 0.10,
    "Mongolia": 0.10,
    "Philippines": 0.10,
    "Sri Lanka": 0.10,
    "Switzerland": 0.10,
    "Vietnam": 0.10
    }
    
    clues = (("Hemisphere", hemisphere, hemisphere_er), ("Camera Gen", camera_gen, camera_gen_er), ("Japan Blur", japan_blur, japan_blur_er), ("Aerial", aerial, aerial_er), ("Geocar", geocar, geocar_er))
    #clues = (("Hemisphere", hemisphere, hemisphere_er), ("Aerial", aerial, aerial_er), ("Japan Blur", japan_blur, japan_blur_er), ("Geocar", geocar, geocar_er), ("Camera Gen", camera_gen, camera_gen_er))
    countries = ("USA", "Japan", "France", "Russia", "UK", "South Africa", "Canada", "Australia", "Brazil", "Finland", 
                 "Spain", "Germany", "Mexico", "Chile", "Norway", "Argentina", "Austria", "India", "Singapore", "Sweden", 
                 "Thailand", "Ireland", "Italy", "Lithuania", "Netherlands", "Poland", "South Korea", "Taiwan", "Botswana", 
                 "Indonesia", "Malaysia", "Peru", "Turkey", "United Arab Emirates", "Bangladesh", "Belgium", "Bolivia", "China",
                 "Colombia", "Costa Rica", "Croatia", "Albania", "Andorra", "Bulgaria", "Cambodia", "Czechia", "Denmark", "Ecuador", 
                 "Egypt", "Estonia", "Eswatini", "Ghana", "Greece", "Hungary", "Iceland", "Israel", "Kenya", "Kyrgyzstan", "Lebanon", 
                 "Lesotho", "Malta", "New Zealand", "Portugal", "Romania", "Senegal", "Serbia", "Slovakia", "Slovenia", "Tunisia", "Uganda",
                 "Ukraine", "Dominican Republic", "Latvia", "Uruguay", "Bhutan", "Guatemala", "Jordan", "Laos", "Mongolia", "Philippines", "Sri Lanka", 
                 "Switzerland", "Vietnam")
    num_of_countries=len(countries)

    #Make sure probabiltiies of all countries add up to 100% (multiply the unscaled probability of each country by 100/sum of each country's unscaled probability)
    country_num=0
    total_probabilities=0
    while country_num<num_of_countries:
        total_probabilities = total_probabilities + country_probabilities[countries[country_num]]
        country_num=country_num+1
     
    if total_probabilities!=0:
        scale_factor=100/total_probabilities
    else:
        scale_factor=0
        print("There was an error calculating the most likely country. All countries appear to have 0% probability. The program will assume the most likely country if all clues are assumed invalid (USA). \n")
        highest_probability_country="USA"
        return highest_probability_country

    country_num=0
    while country_num<num_of_countries:
        country_probabilities[countries[country_num]] = scale_factor*country_probabilities[countries[country_num]]
        country_num=country_num+1

    #Calculate country probabilities for each clue for each country
    clue_num=0
    country_num=0
    num_of_clues=len(clues)

    while clue_num<num_of_clues:
        if (clue_num==0) or (not(clues[clue_num][1]=="Unknown")): #if the clue is regarding the hemisphere or the clue is not equal to "Unknown", then do the following
            country_probabilities_assumed_correct=[]
            country_probabilities_assumed_incorrect=[]
            country_num=0
            while country_num<num_of_countries:
                
                clue_probability = country_clue_probabilities[countries[country_num]][clues[clue_num][0]][clues[clue_num][1]] #let "clue_probability" be probability of the clue being equal to what was found by program (for ex, if geocar="White", take probability of geocar="White" in ___ country)
                country_probabilities_assumed_correct.append(country_probabilities[countries[country_num]]*(clue_probability/100))
                country_probabilities_assumed_incorrect.append(country_probabilities[countries[country_num]]*((100-clue_probability)/100))
                country_num=country_num+1

            #Adjust country probabilities based on error rate for particular clue
            country_num=0
            while country_num<num_of_countries:
                country_probabilities[countries[country_num]] = ((country_probabilities_assumed_correct[country_num]*(1-clues[clue_num][2])) + ((country_probabilities_assumed_incorrect[country_num])*(clues[clue_num][2])))
                country_num=country_num+1
            
            #Make sure probabiltiies of all countries add up to 100% (multiply the unscaled probability of each country by 100/sum of each country's unscaled probability)
            country_num=0
            total_probabilities=0
            while country_num<num_of_countries:
                total_probabilities = total_probabilities + country_probabilities[countries[country_num]]
                country_num=country_num+1
     
            if total_probabilities!=0:
                scale_factor=100/total_probabilities
            else:
                scale_factor=0
                print("There was an error calculating the most likely country. All countries appear to have 0% probability. The program will assume the most likely country if all clues are assumed invalid (USA). \n")
                highest_probability_country="USA"
                return highest_probability_country

            country_num=0
            while country_num<num_of_countries:
                country_probabilities[countries[country_num]] = scale_factor*country_probabilities[countries[country_num]]
                country_num=country_num+1
         
        clue_num=clue_num+1

    #Calculate country probabilities based on languages found
    num_languages_found = len(languages)
    alpha=0.2
    beta=2
    i=0
    while i<num_languages_found:
        
        #Determine error rate for language
        lang_instances=languages[i][1]
        language_er=alpha**(beta*lang_instances)

        country_num=0
        country_probabilities_assumed_correct=[]
        country_probabilities_assumed_incorrect=[]
        while country_num<num_of_countries:
            
            try:
                clue_probability = country_clue_probabilities[countries[country_num]]["Language"][languages[i][0]] #let "clue_probability" be the probability of the clue being equal to what was found by program (for ex, if geocar="White", take probability of geocar="White" in ___ country)
            except:
                #KeyError
                clue_probability = 0
            
            country_probabilities_assumed_correct.append(country_probabilities[countries[country_num]]*(clue_probability/100))
            country_probabilities_assumed_incorrect.append(country_probabilities[countries[country_num]]*((100-clue_probability)/100))
            country_num=country_num+1

        #Adjust country probabilities based on error rate for particular clue
        country_num=0
        while country_num<num_of_countries:
            country_probabilities[countries[country_num]] = (((country_probabilities_assumed_correct[country_num])*(1-language_er)) + ((country_probabilities_assumed_incorrect[country_num])*(language_er)))
            country_num=country_num+1
          
        #Make sure probabiltiies of all countries add up to 100% (multiply the unscaled probability of each country by 100/sum of each country's unscaled probability)
        country_num=0
        total_probabilities=0
        while country_num<num_of_countries:
            total_probabilities = total_probabilities + country_probabilities[countries[country_num]]
            country_num=country_num+1
     
        if total_probabilities!=0:
            scale_factor=100/total_probabilities
        else:
            scale_factor=0
            print("There was an error calculating the most likely country. All countries appear to have 0% probability. The program will assume the most likely country if all clues are assumed invalid (USA). \n")
            highest_probability_country="USA"
            return highest_probability_country

        country_num=0
        while country_num<num_of_countries:
            country_probabilities[countries[country_num]] = scale_factor*country_probabilities[countries[country_num]]
            country_num=country_num+1    

        i=i+1

    #Once all clues have been applied, sort the list of probabilities from highest to lowest probability
    sorted_country_probabilities = sorted(country_probabilities.items(), key=lambda x: x[1], reverse=True)

    #Output the top ten most probable countries (make sure to round the probabilities to 0 decimal places)
    print("\nTop 10 Most Probable Countries")
    print("__________________________________\n")
    i=0
    #dict_keys=list(sorted_country_probabilities.keys())
    #dict_values=list(sorted_country_probabilities.values())
    while(i<10):
        print("{}. {} {}%\n".format(i+1, sorted_country_probabilities[i][0], round(sorted_country_probabilities[i][1], 0)))
        i=i+1

    #Return the "0" index country from the sorted probability array
    #highest_probability_country=next(iter(sorted_country_probabilities))
    highest_probability_country=sorted_country_probabilities[0][0]

    return highest_probability_country

# TESTING AREA
# --------------------------------------------------------------------------------------------------------------------------------------------------

#find_window()
#win32gui.SetForegroundWindow(find_window.hwnd)

#hemisphere="North"
#camera_gen="Gen 3 or 4"
#japan_blur="False"
#aerial="Short"
#geocar="Nothing"
#all_languages=[[]]
#all_languages = list(itertools.chain.from_iterable(all_languages)) #converts a list of lists into just a list
#language_occurances_temp = Counter(all_languages) #converts the list to a dictionary with each key being a language detected, and each key's value being the number of times that language was detected
#language_occurances=list(language_occurances_temp.items()) #converts dictionary to a list
#print("All Languages: {} \n".format(language_occurances))
#determine_country_probabilities(hemisphere, camera_gen, japan_blur, aerial, geocar, language_occurances)

#drag(x=(default_width/2), y=1373, dist_x=0, dist_y=-1360, time=1.5) #Look down
#geocar_straight_is_reliable, x_compass_straight, y_compass_straight=straighten_geocar()
#geocar=determine_geocar(geocar_straight_is_reliable, x_compass_straight, y_compass_straight)

#time.sleep(10000)

# MAIN PROGRAM
# --------------------------------------------------------------------------------------------------------------------------------------------------

#Set screen to Geoguessr
find_window()
win32gui.SetForegroundWindow(find_window.hwnd)

#Play 5 rounds of Geoguessr
while(geo_round<2):

    print("\nRound {}".format(geo_round))
    print("________________________________________________________________ \n")

    set_map() #makes the map as small as possible
    program_images_directory="C:\\Users\\Andrew Callam\\Downloads\\OpenCV\\Geoguessr\\Program Images\\Round {}\\".format(geo_round)
    all_languages=[]

    #Take screenshots of surroundings
    i=0
    while(i<iterations):
        screenshot(identifier=i)
        all_languages.append(determine_language("screenshot_{}.png".format(i))) #determine the language of any text detected in the screenshot
        drag(x=turn_start_x, y=turn_start_y, dist_x=turn_dist, dist_y=0, time=turn_time)
        time.sleep(0.05)
        i=i+1
    
    all_languages = list(itertools.chain.from_iterable(all_languages)) #converts a list of lists into just a list
    language_occurances_temp = Counter(all_languages) #converts the list to a dictionary with each key being a language detected, and each key's value being the number of times that language was detected
    language_occurances=list(language_occurances_temp.items()) #converts dictionary to a list
    print("All Languages: {} \n".format(language_occurances))

    #Determine camera generation
    camera_gen, camera_blur = detect_camera_gen()

    #Return to original view
    return_to_start()

    #Return to position that camera was at after taking ground shots
    i=0
    while(i<iterations):
        drag(x=turn_start_x, y=turn_start_y, dist_x=turn_dist, dist_y=0, time=turn_time)
        time.sleep(0.05)
        i=i+1

    #Look up at sky
    time.sleep(0.05)
    drag(look_up_start_x, look_up_start_y, 0, look_up_dist, look_up_time)

    #Take screenshots of sky 
    i=0
    while(i<sky_iterations):
        screenshot(identifier="sky{}".format(i))
        drag(turn_start_x, turn_start_y, turn_dist, 0, turn_time)
        time.sleep(0.05)
        i=i+1
    
    #Using above screenshots, determine hemisphere
    if camera_gen=="Gen 1" or camera_gen=="Unknown":
        sun_lower_limit=np.array([200, 126, 120])
        sun_upper_limit=np.array([255, 140, 128])
    elif camera_gen=="Gen 2":
        sun_lower_limit=np.array([200, 126, 124])
        sun_upper_limit=np.array([255, 132, 128])
    elif camera_gen=="Gen 3 or 4":
        sun_lower_limit=np.array([200, 126, 126])
        sun_upper_limit=np.array([255, 128, 128])

    hemisphere=determine_hemisphere(sun_lower_limit, sun_upper_limit)

    #Return to original view
    return_to_start()

    if camera_gen!="Gen 1":
        #Look down
        drag(x=(default_width/2), y=1373, dist_x=0, dist_y=-1360, time=1.5) 

        #Straighten Geocar 
        geocar_straight_is_reliable, x_compass_straight, y_compass_straight=straighten_geocar()

        #Determine if the country is Japan
        japan_blur=determine_if_japan(camera_blur, geocar_straight_is_reliable)
        print("Is this Japan? {} \n".format(japan_blur))
    else:
        japan_blur="False"

    #Adjust camera generation variable based on whether the program suspects it is Japan or not
    if japan_blur=="True" and camera_gen=="Gen 2":
        camera_gen="Gen 3 or 4" #since Japan is basically always Gen 3 or 4
        print("Cam Gen: 3 or 4 (after checking if Japan) \n")

    #Determine Geocar type if it is not Japan and not Gen 2
    if japan_blur!="True" and camera_gen!="Gen 2" and camera_gen!="Gen 1":
        geocar, aerial = determine_geocar(geocar_straight_is_reliable, x_compass_straight, y_compass_straight)
    else:
        geocar="Unknown" #if it is suspected that the country is Japan or the camera gen is Gen 2, set the geocar to "Unknown"
        aerial="Unknown"

    #Determine probabilities of all countries based on clues found
    highest_probability_country=determine_country_probabilities(hemisphere, camera_gen, japan_blur, aerial, geocar, language_occurances)

    #Waits for the user to press "n" and then "Enter" in order to continue to the next round. 
    #This allows the user to review the outputs of the program for that round before continuing onto the next round.
    pyautogui.alert("Round finished. Type \"n\" and hit \"Enter\" to continue to the next round.")
    x = input("Press n")
    if x == "n":
        pass

    #Click the highest probability country calculated by the "determine_country_probabilities" function on the in-game map
    select_country(highest_probability_country)

    #Clicks the "Guess" button
    click_guess()
    
    click_next_round()

    #Waits 5 seconds to ensure the next round has time to load
    time.sleep(5) 
       
    geo_round=geo_round+1

cv2.waitKey(0)






