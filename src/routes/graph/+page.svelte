<script lang="ts">
import { onMount } from 'svelte';
import * as d3 from 'd3';

// function loadData(url: RouteParams): void {
//     let major: string | undefined = undefined;
//     if (Object.keys(url).length === 2) {
//         major = url.major as string;
//     }
//     const dept = url.dept as string;

//     d3.json(`/data/website/${dept}.json`).then(f => {
//         d3.json(`/data/api/${dept}.json`).then(g => {
//             if (major) {
//                 d3.json(`/data/majors/${dept}.json`).then(h => {
//                     const majorCourses = getMajorCourses(h as MajorJSON, major!);
//                     loadGraph(dept, f as WebsiteCourseJSON, g as APICourseJSON, majorCourses);
//                 });
//             } else {
//                 loadGraph(dept, f as WebsiteCourseJSON, g as APICourseJSON);
//             }
//         });
//     });
// }

interface Node {
    id: string,
    group: string,
    radius: number,
    citing_patents_count: number
}

interface Link {
    source: string,
    target: string,
    value: number
}

onMount(async () => {
    const data = await d3.json('/data/graph.json');

    d3.select('body').selectAll("svg").remove();

    // // Data for the bar chart
    // const data = [30, 86, 168, 281, 303, 365];

    // // Dimensions
    // const width = 500;
    // const height = 300;
    // const barWidth = width / data.length;

    // // Create SVG container
    // const svg = d3
    //     .select("body")
    //     .append("svg")
    //     .attr("width", width)
    //     .attr("height", height);

    // // Create bars
    // svg
    //     .selectAll("rect")
    //     .data(data)
    //     .enter()
    //     .append("rect")
    //     .attr("x", (_, i) => i * barWidth)
    //     .attr("y", (d) => height - d)
    //     .attr("width", barWidth - 2)
    //     .attr("height", (d) => d)
    //     .attr("fill", "steelblue");

    // // Add labels
    // svg
    //     .selectAll("text")
    //     .data(data)
    //     .enter()
    //     .append("text")
    //     .attr("x", (_, i) => i * barWidth + barWidth / 2)
    //     .attr("y", (d) => height - d - 5)
    //     .attr("text-anchor", "middle")
    //     .text((d) => d.toString())
    //     .attr("fill", "black");

    // Specify the dimensions of the chart.
    const width = 928;
    const height = 680;

    // Specify the color scale.
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // The force simulation mutates links and nodes, so create a copy
    // so that re-evaluating this cell produces the same result.
    const links = data.links.map(d => ({...d}));
    const nodes = data.nodes.map(d => ({...d}));

    // Create a simulation with several forces.
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    // Create the SVG container.
    const svg = d3.select('body')
        .append('svg')
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    // Add a line for each link, and a circle for each node.
    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 5)
        .attr("fill", d => color(d.group));

    node.append("title")
        .text(d => d.id);

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

    return svg.node();
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
