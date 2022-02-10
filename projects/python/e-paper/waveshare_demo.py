import os
from waveshare_epd import epd2in7    # we use a Waveshare 2.7" e-Paper display
from PIL import Image, ImageDraw, ImageFont  # some functions from Pillow

# image directory
pic_dir = 'pic'

try:
    # initialise display
    epd_disp = epd2in7.EPD()
    epd_disp.init()
    
    # clear display : 0=black, 255=white
    epd_disp.Clear(255)
    
    # reverse widht and heigt as display is n ormally in portrait mode
    w = epd_disp.height
    h = epd_disp.width
    print('width', w)
    print('height', h)
    
    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, 'Avenir Next.ttc'), 18, index=1)
    bottom_font = ImageFont.truetype(os.path.join(pic_dir, 'Avenir Next.ttc'), 15, index=5)
    
    # define and draw background
    image = Image.new(mode='1', size=(w,h), color=255)
    draw = ImageDraw.Draw(image)
    
    # position and draw text
    draw.text((15, 0), 'Welcome to the Workshop!', font=top_font, fill=0, align='left')
    draw.text((10, 150), 'https://dronebotworkshop.com', font=bottom_font, fill=0, align='left')
    
    # get robot image
    dbwsbot = Image.open(pic_dir+'/dbws-robot.bmp')
    
    # paste image onto background
    image.paste(dbwsbot, (80, 35))
    
    # write buffer data to display
    epd_disp.display(epd_disp.getbuffer(image))
    
except IOError as e:
    print(e)
    