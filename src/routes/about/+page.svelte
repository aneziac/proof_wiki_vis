
<script lang="ts">
import { onMount } from 'svelte';
import * as d3 from 'd3';

onMount(() => {
    d3.select('body').selectAll("svg").remove();
})
</script>

<div class="container h-full mx-auto flex justify-center items-center">
    <div class="pt-20">
        <h1 class="h1">About</h1>
        <br />
        <h2>
            This project was created for SB Hacks 2025 by Jesse Cobb, Nate Annau, and Shane Tobin.
            <br /><br />
            Repository Link: <a href=https://github.com/aneziac/proof_wiki_vis class="text-blue-500">https://github.com/aneziac/proof_wiki_vis</a>
        </h2>
    </div>
</div>
