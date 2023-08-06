#!/bin/env python3

'''Copyright 2023 Free World Certified - all rights reserved.

This illustrates how to use PIL to generate QRcode images.

'''

from PIL import Image, ImageDraw, ImageFont #Save and display the image
import qrcode

def make(url, fname):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # the most
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="darkblue", back_color="white")

    logo = Image.open('FreeWorldCertified-logo.png')
 
    # taking base width
    basewidth = 100
 
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), resample=Image.BICUBIC) #Image.ANTIALIAS)
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos)
    img.save(fname)
    
make('https://freeworldcertified.org/', 'fwc-qrcode.png')
