# Introduction
PixelartGen is a tool developed using PySide6 toolkit and OpenCV library for creating pixelart from image.

Just drag and drop an image and you are ready to apply few interesting effects using simple and intuitive GUI.

# Key Features
- Adjust pixelation factor and image scaling
- Change color palette using 2 different methods: Adaptive or Custom (from file)
- Play around with brightness, contrast and saturation levels
- Add an outline for cartoon-ish look
- Smooth out imperfactions of the image
- More coming soon!

# Presentation

Playing around with basic features on the image of a taxi:

![image](https://user-images.githubusercontent.com/87280929/213887329-80f2dc43-ecb5-492f-b01c-9e06af805ff0.png)


Quickly create stylized sprites for your pixelart game using custom palettes:

![comparison](https://user-images.githubusercontent.com/87280929/213888320-3fe984c2-37f6-4e22-9ff3-e70496ea458c.png)


Get inspiration for a character by applying effects to the image of low poly figure:

![comparison2](https://user-images.githubusercontent.com/87280929/213888217-b1f99cdd-1143-4f33-bf00-2f8b3d576ecb.png)


Select a custom color palette in Paint.net format from sites like lospec.com

![image](https://user-images.githubusercontent.com/87280929/213888847-ad8b0086-912b-4fe1-ba22-6c2f2e8d3c0d.png)

```
FF8c8fae
FF584563
FF3e2137
FF9a6348
FFd79b7d
FFf5edba
FFc0c741
FF647d34
FFe4943a
FF9d303b
FFd26471
FF70377f
FF7ec4c1
FF34859d
FF17434b
FF1f0e1c
```

GUI preview:

![image](https://user-images.githubusercontent.com/87280929/213886925-8c972f5f-ea49-420b-9225-b86c1c1eb1ed.png)


# Pixelation function

```python
def Pixelate(self, factor, resize):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        height, width = img.shape[:2]

        pixelart = cv2.resize(img, (int(width/factor), int(height/factor)), interpolation = cv2.INTER_LINEAR)

        if resize == False:
            pixelart = cv2.resize(pixelart, (width, height), interpolation=cv2.INTER_NEAREST)

        cv2.imwrite("pixelart.png", pixelart)
```
