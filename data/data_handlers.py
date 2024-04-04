import PyPDF2
from PIL import Image


def file_handler(name, n):
    images = []
    if name.split(".")[-1] == "txt":
        x = open(name, mode="r")
        string = x.read()
    elif name.split(".")[-1] == "pdf":
        x = open(name, 'rb')
        reader = PyPDF2.PdfReader(x)
        XObject = reader.pages[0]['/Resources']['/XObject'].getObject()
        for obg in XObject:
            if XObject[obg]['/Subtipe'] == '/Image':
                size = (XObject[obg]['/Width'], XObject[obg]['/Height'])
                data = XObject[obg].getData()
                mode = "RGB"
                if XObject[obg]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                else:
                    print("Error")
                images.append(img)
        string = ""
        for i in reader.pages:
            string = string + i.extract_text()
    x.close()
    result = []
    for i in range(n, len(string), n):
        result.append(string[i - n:i])
        if len(string) - n < i:
            result.append(string[i:])
    if len(images) > 0:
        result = (result, images)
    return result