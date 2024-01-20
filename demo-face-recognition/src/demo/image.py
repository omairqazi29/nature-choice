def crop_image(img, rect):
    """An utility function to crop an image to the given rect"""
    x, y, w, h = rect
    return img[y : y + h, x : x + w]
