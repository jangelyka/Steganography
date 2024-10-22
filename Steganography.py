# This program focuses on hiding a message or an image within an image; it
# also extracts a message or an image that was hidden within the image

# Author: Jangelyka Restituyo Rosario
# Author: Luis Manuel Fontán Rodríguez
# Date: May 24, 2023

def main():
    #Chooses to either encode or decode
    print("What do you wish to do?")
    print("A. Encode a message within an image.");
    print("B. Encode an image within an image.");
    print("C. Reveal a message within an image.");
    print("D. Reveal an image within an image.");
    option = input().upper()
    while (option!='A') and (option!='B') and (option!='C') and (option!='D'):
        option=input("Invalid option. What do you wish to do?\n").upper()

    if (option=='A'):
        encode_message_image()
    elif (option=='B'):
        encode_image_image()
    elif (option=='C'):
        decode_message_image()
    else:
        decode_image_image()

#This method hides a message within an image; it asks for the
#image that will hide the message and the message to be hidden
def encode_message_image():
    #Asks to input the image that will hide the message and the
    #message that will be hidden
    carrier = input("Enter the image file that will hide the message: \n")
    message = input("Enter the message: \n")

    #Opens the pixmap of the image and separates each section
    pixmap = open(carrier,"r")
    pix_map = pixmap.read()
    line = pix_map.split(None, 4)

    #Saves the image's width and height 
    width = int(line[1])
    height = int(line[2])

    #Compares the image's size with the message's size
    if(len(message) > width or len(message) > height):
        print("The message cannot be hidden within the image. Message size too big.")

    else:
        #Saves the pixmap pixels in a list
        pixels = line[4].split()
        int_pixels = [int(i) for i in pixels]

        #Converts the message into binary
        bin_message = list("".join(format(ord(i), "08b") for i in message))
        for i in range(len(bin_message)):
            bin_message[i] = int(bin_message[i])

        #Hides the message in the image
        i = 0
        while i < len(bin_message):
            int_pixels[i] -= bin_message[i]
            i+=1

        #Converts the int list into a string to be input into the file
        pix = ""
        for i in int_pixels:
            pix = pix + str(i) + " "
            i+=1
        
        #Opens a ppm file to save the image with the hidden message   
        pixels_ppm = open("Stenography Message as PPM.ppm","w")
        pixels_ppm.write("P3\n")
        pixels_ppm.write(str(width) + " " + str(height)+"\n")
        pixels_ppm.write("255\n")
        pixels_ppm.write(pix)
        pixels_ppm.close()

        print("The message has been hidden successfully.")

#This method hides an image within an image; it asks for the
#image that will hide the other image and for the image that
#will be hidden
def encode_image_image():
    #Asks to input the image that will hide the other image
    # and the image that will be hidden
    carrier = input("Enter the image file that will hide the other image: \n")
    hide = input("Enter the image file that will be hidden in the image: \n")

    #Opens the pixmap of the first image and separates each section
    pixmap1 = open(carrier,"r")
    pix_map1 = pixmap1.read()
    line1 = pix_map1.split(None, 4)

    #Opens the pixmap of the second image and separates each section
    pixmap2 = open(hide,"r")
    pix_map2 = pixmap2.read()
    line2 = pix_map2.split(None, 4)

    #Saves the images' width and height
    width1 = int(line1[1])
    height1 = int(line1[2])
    width2 = int(line2[1])
    height2 = int(line2[2])

    #Compares the images' sizes 
    if(width2 > width1 or height2 > height1):
        print("The image cannot be hidden within the image. Image size too big.")

    else:
        #Saves the pixmap pixels of the first image in a list
        pixels1 = line1[4].split()
        int_pixels1 = [int(i) for i in pixels1]

        #Saves the pixmap pixels of the second image in a list
        pixels2 = line2[4].split()
        int_pixels2 = [int(i) for i in pixels2]

        #Substracts the pixel values from the second image to the first image
        i = 0
        while i < len(int_pixels2):
            int_pixels1[i] -= int_pixels2[i]
            i+=1

        #Converts the int list into a string to be input into the file
        pix = ""
        for i in int_pixels1:
            pix = pix + str(i) + " "
            i+=1

        #Opens a ppm file to save the image with the hidden message
        pixels_ppm = open("Stenography Image as PPM.ppm","w")
        pixels_ppm.write("P3\n")
        pixels_ppm.write(str(width1) + " " + str(height1)+"\n")
        pixels_ppm.write("255\n")
        pixels_ppm.write(pix)
        pixels_ppm.close()
    
        print("The image has been hidden successfully.")

#This method reveals the message that was hiden in an image
def decode_message_image():
    #Asks to input the image that with the hidden message and the
    #original image
    stegoimage = input("Enter the image file that contains the hidden message: \n")
    carrier = input("Enter the original image: \n")

    #Opens the pixmap of the first image and separates each section
    pixmap1 = open(stegoimage,"r")
    pix_map1 = pixmap1.read()
    line1 = pix_map1.split(None, 4)
    pixels1 = line1[4].split()
    int_pixels1 = [int(i) for i in pixels1]

    #Opens the pixmap of the second image and separates each section
    pixmap2 = open(carrier,"r")
    pix_map2 = pixmap2.read()
    line2 = pix_map2.split(None, 4)
    pixels2 = line2[4].split()
    int_pixels2 = [int(i) for i in pixels2]

    #Substracts the pixels from the first image to the second image
    for i in range(len(int_pixels1)):
        int_pixels2[i] -= int_pixels1[i]

    #Groups the elements of the int_pixels2 list into groups of 8 to work with
    #bytes and decode the encoded message
    int_pixels2 = [int_pixels2[i:i+8] for i in range(0, len(int_pixels2), 8)]
    pixels2_list = []
    for i in range(len(int_pixels2)):
      pixels2_list.insert(i, my_bin_2_dec(int_pixels2[i]))
      i+=1

    for i in range(len(pixels2_list)):
      pixels2_list[i] = chr(pixels2_list[i])

    deciphered = ""
    for i in pixels2_list:
       deciphered += i

    #Success message
    print("This is the message that was hidden: \n" + deciphered)
    
#This method reveals the image that was hidden inside an image
def decode_image_image():
    #Asks to input the image that with the hidden message and the
    #original image
    stegoimage = input("Enter the image file that contains the hidden image: \n")
    carrier = input("Enter the original image: \n")

    #Opens the pixmap of the first image and separates each section
    pixmap1 = open(stegoimage,"r")
    pix_map1 = pixmap1.read()
    line1 = pix_map1.split(None, 4)

    #Saves the image's width and height
    width1 = int(line1[1])
    height1 = int(line1[2])

    #Opens the pixmap of the second image and separates each section
    pixmap2 = open(carrier,"r")
    pix_map2 = pixmap2.read()
    line2 = pix_map2.split(None, 4)

    #Saves the pixmap pixels of the first image in a list
    pixels1 = line1[4].split()
    int_pixels1 = [int(i) for i in pixels1]

    #Saves the pixmap pixels of the second image in a list
    pixels2 = line2[4].split()
    int_pixels2 = [int(i) for i in pixels2]

    #Substracts the pixels from the first image to the second image
    for i in range(len(int_pixels1)):
        int_pixels2[i] -= int_pixels1[i]

    #Converts the int list into a string to be input into the file
    pix = ""
    for i in int_pixels2:
        pix = pix + str(i) + " "
        i+=1

    #Opens a ppm file to save the image with the hidden message
    pixels_ppm = open("Stenography Hidden as PPM (image).ppm","w")
    pixels_ppm.write("P3\n")
    #pixels_ppm.write(str(width1) + ' ' + str(height1)+'\n') WRONG
    #the width and the height must be the ones from the original picture hidden
    pixels_ppm.write(str(width1) + " " + str(height1)+"\n")
    pixels_ppm.write("255\n")
    pixels_ppm.write(pix)
    pixels_ppm.close()

    print("The image has been extracted successfully.")
       
#This method converts a binary list given into an integer 
def my_bin_2_dec (b):
  exp = -1

  for i in (b):
      exp+=1
   
  d = 0
  for i in b:
      d += i * 2 ** exp
      exp-=1

  return d
    

main()



    
