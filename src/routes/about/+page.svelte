<h2>About</h2>
<p>SB Hacks 2025 project</p>

<script lang="ts">
import { onMount } from 'svelte';
import * as d3 from 'd3';

onMount(() => {
    d3.select('body').selectAll("svg").remove();
})
</script>
