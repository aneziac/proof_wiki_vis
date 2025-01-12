import { type Graph } from './graphTypes';

function buildAdjacencyList(graph: Graph): Record<string, string[]> {
    const adjacencyList: Record<string, string[]> = {};

    // Initialize adjacency list
    graph.nodes.forEach(node => {
      adjacencyList[node.id] = [];
    });

    // Populate adjacency list from edges
    graph.links.forEach(link => {
      adjacencyList[link.source].push(link.target);
      adjacencyList[link.target].push(link.source); // If undirected graph
    });

    return adjacencyList;
}

function printTree(nodeId: number, adjacencyList: Record<number, number[]>, visited: Set<number>, level: number = 0): void {
    if (visited.has(nodeId)) return; // Prevent infinite loops in cyclic graphs
    visited.add(nodeId);

    const indent = ' '.repeat(level * 2);
    console.log(`${indent}${nodeId}`);

    const neighbors = adjacencyList[nodeId];
    neighbors.forEach(neighbor => {
        printTree(neighbor, adjacencyList, visited, level + 1);
    });
}
