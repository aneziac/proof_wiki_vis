import requests
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass, asdict
import re
import json

@dataclass
class PageNode:
    resultType:     str
    name:           str
    url:            str
    understood:     bool

@dataclass
class PageLink:
    source: str
    target: str

@dataclass
class HTMLChunk:
    identifier: str
    content:    str
    parser:     bs

urls_indexed = set()
DOMAIN = "https://proofwiki.org"
VALID_IDS = [
    "Theorem",
    "Definition",
    "Corollary",
    "Proposition",
    "Proof"
]
VALID_IDS_REGEX = '^(' + '|'.join(
    re.escape(pattern.replace("*", ".*")) for pattern in VALID_IDS
) + ')'

INVALID_TYPES = [
    "Definition",
    "Special",
    "Category",
    "Mathematician",
    "Talks",
    "Talk",
    "ProofWiki",
    "Symbols",
    "Template",
    "Book",
    "Help",
    "Main_Page",
    "File"
]




def ParsePage(url : str) -> None:
    print(f"----------------- started processing {url} -----------------")
    response    = requests.get(url)
    data        = bs(response.content, 'html.parser')
    chunks      = GetChunks(data)
    depChunks   = []

    pageType, pageName = GetHeader(data)
    if pageType == "":
        if len(chunks) > 0:
            pageType = chunks[0].identifier
        else:
            pageType = "Misc"

    for chunk in chunks:
        deps = GetDependencies(chunk.parser)

        unique_deps = []
        for dep in deps:
            if dep not in unique_deps:
                unique_deps.append(dep)

        unique_deps = [DOMAIN + dep for dep in unique_deps]
        depChunks.append(unique_deps)

    # DEBUG
    print(pageType, pageName)
    if len(depChunks) > 0:
        for dep in depChunks[0]:
            print(dep)


    # WRITE NODE
    pageNode = PageNode(
        resultType      = pageType,
        name            = pageName,
        url             = url,
        understood      = False,
    )
    write_to_json(asdict(pageNode), "page_nodes.json")
    urls_indexed.add(url)

    for deps in depChunks:
        for dep in deps:
            if dep not in urls_indexed:
                pageLink = PageLink(
                    source = url,
                    target = dep
                )
                write_to_json(asdict(pageLink), "page_links.json")
                ParsePage(dep)

    print(f"----------------- stopped processing {url} -----------------")


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

        match = re.match(VALID_IDS_REGEX, chunk.identifier)
        if match:
            chunk.identifier = match.group(0)
            chunks.append(chunk)

    return chunks



def GenChunk(html : bs) -> HTMLChunk:
    header = html.find('h2')
    span = header.find('span') if header else None

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
    anchors = html.find_all('a', href=True)

    hrefs = [
        a['href'] for a in anchors
        if a['href'].startswith('/wiki/') 
        and not any(a['href'].startswith(f'/wiki/{unwanted}') for unwanted in INVALID_TYPES)
        and a['href'].count('/') < 3
        and '#' not in a['href']
    ]

    return hrefs



def GetHeader(html : bs) -> tuple[str, str]:
    header = html.find('h1')

    span_type = header.find('span', class_="mw-page-title-namespace") if header else None
    span_name = header.find('span', class_="mw-page-title-main") if header else None

    pageType = ""
    pageName = ""

    if span_type:
        pageType = span_type.get_text()

    if span_name:
        pageName = span_name.get_text()

    return pageType, pageName



def write_to_json(data, filename):
    with open(filename, 'a') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write(',\n')
        # f.write('\n')


ParsePage("https://proofwiki.org/wiki/Chinese_Remainder_Theorem")
