// export interface Node {
//     id: string,
//     group: string,
//     radius: number,
//     citing_patents_count: number
// }

interface Node {
    resultType: string,
    name: string,
    id: string, // url
    understood: boolean,
}

interface Link {
    source: string,
    target: string,
}

export interface Graph {
    nodes: Node[]
    links: Link[]
}
