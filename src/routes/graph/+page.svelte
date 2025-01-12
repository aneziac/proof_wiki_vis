<script lang="ts">
import { type Graph, type Node } from './graphTypes';
import { onMount } from 'svelte';
import * as d3 from 'd3';
import Fuse from 'fuse.js';
import { Search, Button } from 'flowbite-svelte';

let activeNode = null;

interface OverwrittenLink {
    source: Node,
    target: Node
}

  const maxResults = 8;
  let showSearch = $state(false); // State to track search bar visibility
  let searchQuery = $state(''); // State to bind the search input

  let isHovered = false;

  // Function to toggle the visibility of the search bar when spacebar is pressed
  const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === ' ') {
      // event.preventDefault(); // Prevent the default spacebar behavior (scrolling)
      showSearch = true; // Toggle visibility of search bar
    } else if (event.key === 'Escape') {
      showSearch = false;
      searchQuery = '';
    }
  };

  let data: Graph = $state({ nodes: [], links: [] });

    // Fuse.js configuration)
    let fuse = new Fuse(['test'], {
      keys: ['name'], // Fields to search in
      threshold: 0.3, // Fuzziness level (lower is stricter)
    });

    let results = $derived.by(() => {
      return searchQuery ? fuse.search(searchQuery).map(result => result.item) : [];
    }); // Search results

  let nodes = {};

  onMount(async () => {
    document.addEventListener('keydown', handleKeydown);

    data = await d3.json('/data/new_pages.json') as Graph;
    ($state.snapshot(data).nodes).forEach((node) => {
        fuse.add(node.name);
    })

    d3.select('body').selectAll('svg').remove();

    const UNSELECT_COLOR    = "#AAA";
    const SELECT_COLOR      = "#FFF";
    const UNSELECT_OP       = 0.6;
    const SELECT_OP         = 0.9;

    // Specify the color scale.
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // The force simulation mutates links and nodes, so create a copy
    // so that re-evaluating this cell produces the same result.
    const links = data.links.map((d) => ({ ...d }));
    nodes = data.nodes.map((d) => ({ ...d }));

    // const adjacencyMap = new Map<number, Set<number>>();
    // links.forEach(link => {
    //     if (!adjacencyMap.has(link.source)) {
    //         adjacencyMap.set(link.source, new Set());
    //     }
    //     if (!adjacencyMap.has(link.target)) {
    //         adjacencyMap.set(link.target, new Set());
    //     }
    //     adjacencyMap.get(link.source)?.add(link.target);
    //     adjacencyMap.get(link.target)?.add(link.source);
    // });

    const outgoingMap = new Map<number, Set<number>>();
    const incomingMap = new Map<number, Set<number>>();
    links.forEach(link => {
        // Add to outgoing map (source -> target)
        if (!outgoingMap.has(link.source)) {
            outgoingMap.set(link.source, new Set());
        }
        outgoingMap.get(link.source)?.add(link.target);

        // Add to incoming map (target -> source)
        if (!incomingMap.has(link.target)) {
            incomingMap.set(link.target, new Set());
        }
        incomingMap.get(link.target)?.add(link.source);
    });

    const id_to_node = new Map<string, Node>();
    nodes.forEach(node => {
        id_to_node.set(node.id, node);
    })

    // Create a simulation with several forces.
    const simulation = d3.forceSimulation(nodes)
        .force("center", d3.forceCenter())
        .force("link", d3.forceLink(links).id(d => d.id).strength(2))
        .force("collide", d3.forceCollide(15).strength(1))
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());


    const updateChartSize = () => {
        const width = window.innerWidth;
        const height = window.innerHeight;

        const zoom = d3.zoom<SVGSVGElement, unknown>()
            .scaleExtent([0.2, 2])
            // .translateExtent([[0, 0], [width * 5, height * 5]])
            .on('zoom', e => {
                d3.selectAll('g')
                    .attr('transform', e.transform);
            });

        const svg = d3.select("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .call(zoom);
    };

    // Create the SVG container.
    const svg = d3.select('body')
        .append('svg')
        .append("svg:g")
        .attr("style", "width: 100%; height: 100%;")
        .attr("transform","scale(.5, .5)");

    updateChartSize();
    window.addEventListener('resize', updateChartSize);


    // Add a line for each link, and a circle for each node.
    const link = svg.append("g")
        .attr("stroke", UNSELECT_COLOR)
        .attr("stroke-opacity", UNSELECT_OP)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => 3);

    const node = svg.append("g")
        .attr("stroke", "#FFF")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 6)
        .attr("fill", d => color(d.resultType))
        .on("mouseenter", (_, hoveredNode: Node) => {

            // const adjacentNodes = new Set();
            // data.links.forEach(link => {
            //     if (link.source === hoveredNode.id) {
            //         adjacentNodes.add(link.target);
            //     } else if (link.target === hoveredNode.id) {
            //         adjacentNodes.add(link.source);
            //     }
            // });
            // const adjacentNodes = adjacencyMap.get(hoveredNode.id) || new Set<number>();
            const inAdjacents = incomingMap.get(hoveredNode.id) || new Set<number>();
            const outAdjacents = outgoingMap.get(hoveredNode.id) || new Set<number>();

            // @ts-ignore
            link.style('stroke-width', (edge: OverwrittenLink) => {
                if   (hoveredNode === edge.source
                   || hoveredNode === edge.target) {
                    return 7;
                } else {
                    return 4;
                }
            });

            // @ts-ignore
            link.style('stroke', (edge: OverwrittenLink) => {
                return edge.source === hoveredNode ||
                    edge.target === hoveredNode ? SELECT_COLOR : UNSELECT_COLOR;
            });

            // @ts-ignore
            link.style('stroke-opacity', (edge: OverwrittenLink) => {
                return edge.source === hoveredNode ||
                    edge.target === hoveredNode ? SELECT_OP : UNSELECT_OP;
            });

            node.attr('r', (otherNode: Node) => {
                return otherNode === hoveredNode ? 10 : 6;
            });

            // @ts-ignore
            node.style('fill', (otherNode: Node) => {
                let sameNode = hoveredNode === otherNode;
                let inAdjacent = inAdjacents.has(otherNode.id)
                let outAdjacent = outAdjacents.has(otherNode.id)

                if (!sameNode && !inAdjacent) {
                    if (outAdjacent) {
                        return '#FFF';
                    }
                    return '#808080';
                }
            });
        });

    node.append("title")
        .text("");  // Remove the title element to prevent the default tooltip

    // Add a drag behavior.
    node.call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));

            node.on("mouseover", function(event, d) {
    // Create a tooltip text box on hover
    d3.select('body').append("div")
        .attr("class", "tooltip")
        .attr("style", "position: absolute; background: rgba(0,0,0,0.7); color: white; padding: 5px; border-radius: 5px;")
        .html(`${d.name}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY + 10) + "px");
    });

    function formatDeps(depChunks: string[][]) {
        var formatted = "<hr/>";
        if (depChunks.length == 0) {
            formatted += "<p>No dependencies</p>";
            return formatted;
        }
        for (let i = 0; i < depChunks.length; i++) {
            const dependencies = depChunks[0];
            var header = "";
            if (i == 0) {
                header = "Statement";
            } else {
                if (depChunks.length <= 2){
                    header = "Proof";
                } else {
                    header = `Proof ${i}`;
                }
            }

            var chunk = `<h4>${header} dependencies</h4><ul>`;
            for (let j = 0; j < dependencies.length; j++) {
                const dep = dependencies[j];
                const currNode = id_to_node.get(dep);
                chunk += `<li class="list-disc"><a href="${dep}"  style="color: blue;" target="_blank">${currNode.name}</a></li>`
            }
            chunk += "</ul>";
            formatted += chunk;
        }

        return formatted;
    }

    function floatWin(event : any, d : Node) {
        // Remove any existing menu and backdrop
        d3.select('.menu-backdrop').remove();
        d3.select('.info-box').remove();

        // Create a full-screen backdrop
        d3.select('body').append("div")
            .attr("class", "menu-backdrop")
            .attr("style", `position: fixed; 
                            top: 0; left: 0; 
                            width: 100vw; height: 100vh; 
                            background: rgba(0, 0, 0, 0.5); 
                            z-index: 999;`)
            .on("click", function() {
                // Clicking the backdrop closes the menu
                d3.select('.menu-backdrop').remove();
                d3.select('.info-box').remove();
            });

        // Append the large info menu
        d3.select('body').append("div")
            .attr("class", "info-box")
            .attr("style", `position: fixed;
                            top: 50%; left: 50%;
                            transform: translate(-50%, -50%);
                            width: 60vw; height: 70vh;
                            background: rgba(255, 255, 255, 0.9); 
                            color: black;
                            padding: 50px;
                            border-radius: 10px;
                            z-index: 1000;
                            box-shadow: 0px 0px 10px rgba(0,0,0,0.3); 
                            overflow-y: auto;`)
            .html(`<h2><a href="${d.id}" target="_blank">${d.name} (${d.resultType})</a></h2>
                    ${formatDeps(d.dependencies)}
                   <button id="close-menu" style="
                            position: absolute; 
                            top: 10px; right: 20px; 
                            background: red;
                            color: white;
                            border: none;
                            padding: 5px 10px; 
                            cursor: pointer;
                            font-size: 16px;
                            border-radius: 5px;">X</button>`);

        // Add event listener to close button
        d3.select("#close-menu").on("click", function() {
            d3.select('.menu-backdrop').remove();
            d3.select('.info-box').remove();
        });
    }

    node.on("click", function(event, d) {
        floatWin(event, d);
    });



    node.on("mouseout", function() {
        // Remove the tooltip when mouse leaves
        link.style('stroke-width', 4);
        link.style('stroke', edge => {
            return "#AAA";
        });
        node.attr('r', node => {
            return 6;
        });
        node.style('fill', node => {
            return color(node.resultType);
        });

        activeNode = null;
        d3.select('.tooltip').remove();
    });


    // Set the position attributes of links and nodes each time the simulation ticks.
    simulation.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);
    });

    // Reheat the simulation when drag starts, and fix the subject position.
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    // Update the subject (dragged node) position during drag.
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    // Restore the target alpha so the simulation cools after dragging ends.
    // Unfix the subject position now that it’s no longer being dragged.
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    // When this cell is re-run, stop the previous simulation. (This doesn’t
    // really matter since the target alpha is zero and the simulation will
    // stop naturally, but it’s a good practice.)
    // invalidation.then(() => simulation.stop());

    return () => {
      document.removeEventListener('keydown', handleKeydown);
    };
  });

function handleClick(result) {
  nodes.forEach((node) => {
    if (result === node.name) {
      console.log(node.x)
    }
  })
}
</script>

{#if showSearch}
  <div class="fixed top-0 left-0 w-full h-full bg-gray-900 bg-opacity-75 flex items-center justify-center">
    <div class="bg-gray-400 p-4 rounded shadow-lg w-3/4">
      <form class="flex mb-4">
        <Search
          autofocus
          size="md"
          class="flex-grow rounded-none py-2.5"
          placeholder="Search..."
          bind:value={searchQuery}
        />
        <Button class="!p-2.5 rounded-s-none">Search</Button>
      </form>

      <!-- Search Results -->
      <ul class="space-y-2">
        {#if results.length > 0}
        {#each results.slice(0, maxResults) as result}
        <li
          class="p-2 bg-gray-500 rounded shadow-sm text-white hover:bg-gray-700 cursor-pointer"
          on:click={() => handleClick(result)}
        >
          <strong>{result}</strong>
        </li>
      {/each}
        {:else}
          <li class="text-gray-500">No results found.</li>
        {/if}
      </ul>
    </div>
  </div>
{/if}

<style>
  .hover {
    color: slategray
  }
</style>
