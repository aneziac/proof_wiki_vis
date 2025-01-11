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

url_to_node = {}
DOMAIN = "https://proofwiki.org"


def ParsePage(url : str) -> None:
    response    = requests.get(url)
    data        = bs(response.content, 'html.parser')
    chunks      = GetChunks(data)
    depChunks   = []

    for chunk in chunks:
        deps = GetDependencies(chunk)
        deps = [DOMAIN + dep for dep in deps]
        depChunks.append(deps)

    pageName, pageType = GetMeta(chunks[0])

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


def GetChunks(html : bs) -> list[bs]:
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

        chunks.append(chunk)

    html_content = ''.join(chunks[0])
    html_parser = bs(html_content, 'html.parser')
    print((html_parser))


    return []

def GetDependencies(chunk : bs) -> list[str]:
    return []

def GetMeta(statement : bs) -> tuple[str, str]:
    return "", ""

ParsePage("https://proofwiki.org/wiki/Chinese_Remainder_Theorem")
