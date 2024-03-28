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
        k = reader.getPage(0)['/Resources']['/XObject'].getObject()
        for obg in k:
            if k[obg]['/Subtipe'] == '/Image':
                size = (k[obg]['/Width'], k[obg]['/Height'])
                data = k[obg].getData()
                mode = "RGB"
                if k[obg]['/Filter'] == '/FlateDecode':
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