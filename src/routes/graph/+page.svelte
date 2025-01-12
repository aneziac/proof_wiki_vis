<script lang="ts">
import { type Graph } from './graphTypes';
import { onMount } from 'svelte';
import * as d3 from 'd3';

onMount(async () => {
    const data = await d3.json('/data/pages.json') as Graph;

    d3.select('body').selectAll("svg").remove();

    // Specify the dimensions of the chart.
    const width = 900;
    const height = 900;

    // Specify the color scale.
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // The force simulation mutates links and nodes, so create a copy
    // so that re-evaluating this cell produces the same result.
    const links = data.links.map(d => ({...d}));
    const nodes = data.nodes.map(d => ({...d}));

    // Create a simulation with several forces.
    const simulation = d3.forceSimulation(nodes)
        .force("center", d3.forceCenter())
        .force("link", d3.forceLink(links).id(d => d.id).strength(2))
        .force("collide", d3.forceCollide(15).strength(1))
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const zoom = d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.2, 2])
        // .translateExtent([[0, 0], [width * 5, height * 5]])
        .on('zoom', e => {
            d3.selectAll('g')
                .attr('transform', e.transform);
        });

    // Create the SVG container.
    const svg = d3.select('body')
        .append('svg')
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "width: 100%; height: 100%;")
        .call(zoom)
        .append("svg:g")
        .attr("transform","scale(.5,.5)");


    // Add a line for each link, and a circle for each node.
    const link = svg.append("g")
        .attr("stroke", "#AAA")
        .attr("stroke-opacity", 0.7)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => 3);

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 6)
        .attr("fill", d => color(d.resultType));

    node.append("title")
        .text(d => d.name);

    // Add a drag behavior.
    node.call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    // Set the position attributes of links and nodes each time the simulation ticks.
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
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

    // return svg.node();
});

// Clean up the SVG when the component is destroyed
// Not working for some reason
// onDestroy(() => {
//     console.log(d3.select(container).selectAll("svg").remove())
//     // console.log(d3.select('body').data)

//     console.log('destroyed')

//     if (container) {
//         d3.select(container).selectAll("svg").remove();
//     }
// });
</script>
