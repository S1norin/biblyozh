import PyPDF2


def file_handler(name, n):
    if name.split(".")[-1] == "txt":
        x = open(name, mode="r")
        string = x.read()
    elif name.split(".")[-1] == "pdf":
        x = open(name, 'rb')
        reader = PyPDF2.PdfReader(x)
        string = ""
        for i in reader.pages:
            string = string + i.extract_text()
    x.close()
    result = []
    for i in range(n, len(string), n):
        result.append(string[i - n:i])
        if len(string) - n < i:
            result.append(string[i:])
    return result