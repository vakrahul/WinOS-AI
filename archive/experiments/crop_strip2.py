from PIL import Image

img = Image.open("paint_toolbar.png")
strip = img.crop((350, 45, 850, 115))
strip.save("tools_actual_strip.png")
print("Saved tools_actual_strip.png, size:", strip.size)
