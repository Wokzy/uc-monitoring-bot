from PIL import Image
import requests
import base64
import io


def prevImage(filename):

    img = Image.open(filename)

    width, height = img.size

    M = max(width, height)

    width_300 = int(300 * width / M)
    height_300 = int(300 * height / M)

    new_img = img.resize((width_300, height_300))

    in_mem_file = io.BytesIO()
    new_img.save(in_mem_file, format="PNG")
    img_file_size = in_mem_file.tell()
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    width_40 = int(300 * width / M)
    height_40 = int(300 * height / M)

    new_img_2 = img.resize((width_40, height_40))

    in_mem_file_2 = io.BytesIO()
    new_img_2.save(in_mem_file_2, format="PNG")
    img_file_size_2 = in_mem_file_2.tell()
    in_mem_file_2.seek(0)
    img_bytes_2 = in_mem_file_2.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes_2)

    return base64_encoded_result_bytes.decode(), img_file_size_2, img_bytes, img_file_size, width_300, height_300, width_40, height_40,\
           width, height
