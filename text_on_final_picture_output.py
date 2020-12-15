from PIL import Image, ImageDraw, ImageFont, ImageFilter

img = Image.open("./images/marge_all.png")

brand1_name = ImageDraw.Draw(img)

font2 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 24, encoding="unic")

brand1_name.text((120, 1440),"Company wise Work Hour %(Monthly)" , (229,193,105), font=font2)
brand1_name.text((730, 1440), "Category wise Work Hour %(Monthly)", (229,193,105), font=font2)

img.save('./images/send_this_photo.png')