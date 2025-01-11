<script lang="ts">
import { onMount } from 'svelte';
import * as d3 from 'd3';

// let svg: d3.Selection<SVGSVGElement, unknown, HTMLElement, any>; // Keep a reference to the SVG
let container: HTMLDivElement | null = null; // Reference to the container div

onMount(() => {
    d3.select('body').selectAll("svg").remove();

    if (!container) return;

    // Data for the bar chart
    const data = [30, 86, 168, 281, 303, 365];

    // Dimensions
    const width = 500;
    const height = 300;
    const barWidth = width / data.length;

    // Create SVG container
    const svg = d3
        .select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Create bars
    svg
        .selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", (_, i) => i * barWidth)
        .attr("y", (d) => height - d)
        .attr("width", barWidth - 2)
        .attr("height", (d) => d)
        .attr("fill", "steelblue");

    // Add labels
    svg
        .selectAll("text")
        .data(data)
        .enter()
        .append("text")
        .attr("x", (_, i) => i * barWidth + barWidth / 2)
        .attr("y", (d) => height - d - 5)
        .attr("text-anchor", "middle")
        .text((d) => d.toString())
        .attr("fill", "black");
});

// Clean up the SVG when the component is destroyed
// NOt working for some reason
// onDestroy(() => {
//     console.log(d3.select(container).selectAll("svg").remove())
//     // console.log(d3.select('body').data)

//     console.log('destroyed')

//     if (container) {
//         d3.select(container).selectAll("svg").remove();
//     }
// });
</script>

<div bind:this={container}></div>
