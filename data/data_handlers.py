from bs4 import BeautifulSoup as Soup, Tag
import lxml


def compile_chapter(section: Tag):
    title = title_tag.get_text(strip=True) if (
        title_tag := section.find('title')
    ) else ''
    rows = '\n\t'.join(
        [p.get_text(strip=True) for p in title_tag.find_next_siblings('p')]
    )
    return f'{title}\n{rows}'


def file_handler(name, n):
    if name.split(".")[-1] == "txt":
        x = open(name, mode="r", encoding='utf-8')
        string = x.read()
    else:
        with open(name, 'r', encoding='utf-8') as x:
            soup = Soup(x.read(), 'xml')
            string = "\n".join([*map(compile_chapter, soup.find_all('section'))])
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
