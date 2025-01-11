import requests
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass

@dataclass
class PageNode:
    resultType:     str
    name:           str
    url:            str
    understood:     bool
    dependencies:   list[list[str]]

@dataclass
class HTMLChunk:
    identifier: str
    content:    str
    parser:     bs

url_to_node = {}
DOMAIN = "https://proofwiki.org"
VALID_IDS = [
    "Theorem",
    "Proof",
    "Proof 1",
    "Proof 2"
]




def ParsePage(url : str) -> None:
    response    = requests.get(url)
    data        = bs(response.content, 'html.parser')
    chunks      = GetChunks(data)
    pageName    = chunks[0].content
    pageType    = chunks[0].identifier
    depChunks   = []

    for chunk in chunks:
        deps = GetDependencies(chunk.parser)
        deps = [DOMAIN + dep for dep in deps]
        depChunks.append(deps)

    # unique_ = []
    # for item in my_list:
    #     if item not in unique_list:
    #         unique_list.append(item)

    for dep in depChunks[1]:
        print(dep)

    pageNode = PageNode(
        resultType      = pageType,
        name            = pageName,
        url             = url,
        understood      = False,
        dependencies    = depChunks
    )

    url_to_node[url] = pageNode

    for deps in depChunks:
        for dep in deps:
            if dep not in url_to_node:
                ParsePage(dep)


def GetChunks(html : bs) -> list[HTMLChunk]:
    headings = html.find_all('h2')
    chunks = []

    for i in range(len(headings)):
        start_tag = headings[i]


        if i + 1 < len(headings):
            end_tag = headings[i + 1]
        else:
            end_tag = html.contents[-1]

        chunk = [str(start_tag)]
        for element in start_tag.find_all_next():
            if element == end_tag:
                break
            chunk.append(str(element))

        chunk = bs(''.join(chunk), 'html.parser')
        chunk = GenChunk(chunk)
        if chunk.identifier in VALID_IDS:
            chunks.append(chunk)

    for chunk in chunks:
        print("------------------------------------------------------------")
        # print(chunk.identifier, chunk.content)
        # print(chunk.parser)


    return chunks



def GenChunk(html : bs) -> HTMLChunk:
    header = html.find('h2')
    span = header.find('span')
    htmlChunk = None

    if span:
        htmlChunk = HTMLChunk(
            identifier = span.get('id'),
            content = span.get_text(),
            parser = html
        )
    else:
        htmlChunk = HTMLChunk(
            identifier = "",
            content = "",
            parser = html
        )

    return htmlChunk



def GetDependencies(html : bs) -> list[str]:
    anchors = html.find_all('a')

    hrefs = []
    for anchor in anchors:
        hrefs.append(anchor['href'])

    print(hrefs)
    return hrefs



def GetMeta(statement : bs) -> tuple[str, str]:
    return "", ""


ParsePage("https://proofwiki.org/wiki/Chinese_Remainder_Theorem")
