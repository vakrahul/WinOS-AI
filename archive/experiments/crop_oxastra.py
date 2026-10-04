from PIL import Image

img = Image.open("linkedin_email_posts.png")
# Crop OxAstra post area
crop = img.crop((400, 250, 1150, 750))
crop.save("oxastra_post_area.png")
print("Cropped OxAstra post area, size:", crop.size)
