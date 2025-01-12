<script lang="ts">
  import { type Graph, type Node } from './graphTypes';
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import Fuse from 'fuse.js';
  import { Search, Button } from 'flowbite-svelte';

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

    data = await d3.json('/data/pages.json') as Graph;
    ($state.snapshot(data).nodes).forEach((node) => {
        fuse.add(node.name);
    })

    d3.select('body').selectAll('svg').remove();

    // Specify the dimensions of the chart.
    const width = 928;
    const height = 680;

    // Specify the color scale.
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // The force simulation mutates links and nodes, so create a copy
    // so that re-evaluating this cell produces the same result.
    const links = data.links.map((d) => ({ ...d }));
    nodes = data.nodes.map((d) => ({ ...d }));

    // Create a simulation with several forces.
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        'link',
        d3.forceLink(links).id((d) => d.id)
      )
      .force('charge', d3.forceManyBody())
      .force('x', d3.forceX())
      .force('y', d3.forceY());

    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.2, 2])
      // .translateExtent([[0, 0], [width * 5, height * 5]])
      .on('zoom', (e) => {
        d3.selectAll('g').attr('transform', e.transform);
      });

    // Create the SVG container.
    const svg = d3
      .select('body')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [-width / 2, -height / 2, width, height])
      .attr('style', 'max-width: 100%; height: auto;')
      .call(zoom);

    // Add a line for each link, and a circle for each node.
    const link = svg
      .append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', (d) => Math.sqrt(d.value));

    const node = svg
      .append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 5)
      .attr('fill', (d) => color(d.group));

    node.append('title').text((d) => d.id);

    // Add a drag behavior.
    node.call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));

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
