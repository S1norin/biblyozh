from bs4 import BeautifulSoup as Soup, Tag
import lxml

def compile_chapter(section: Tag):
    title = title_tag.get_text(strip=True) if (
        title_tag := section.find('title')
    ) else ''
    rows = '\n'.join(
        [p.get_text(strip=True) for p in title_tag.find_next_siblings('p')]
    )
    return f'{title}\n{rows}'

def file_handler(name, n):
    images = []
    if name.split(".")[-1] == "txt":
        x = open(name, mode="r")
        string = x.read()
    elif name.split(".")[-1] == "fb2":
        with open(name, 'r', encoding='utf-8') as x:
            soup = Soup(x.read(), 'lxml')
            string = "\n".join([*map(compile_chapter, soup.find_all('section'))])
    x.close()
    string = string.split()
    result = [""]
    count = 0
    for i in string:
        count += len(i)
        result[-1] = result[-1] + " " + i
        if count >= n:
            count = 0
            result.append("")
    return result

print(file_handler("test_files/test_file_3.fb2", 50))