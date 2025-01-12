export interface Node {
    id: string,
    group: string,
    radius: number,
    citing_patents_count: number
}

// interface Node {
//     result_type: string,
//     name: string,
//     url: string,
//     understood: boolean,
// }

export interface Link {
    source: string,
    target: string,
    value: number
}

export interface Graph {
    nodes: Node[]
    links: Link[]
}
