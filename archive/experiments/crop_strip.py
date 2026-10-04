from PIL import Image

img = Image.open("paint_toolbar.png")
# Let's crop strips along the toolbar at y=50..110
# X from 100 to 600
strip = img.crop((100, 45, 600, 115))
strip.save("toolbar_tools_strip.png")
print("Saved toolbar_tools_strip.png, size:", strip.size)
