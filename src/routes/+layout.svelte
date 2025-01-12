<script lang="ts">
    import '../app.postcss'
    import { ButtonGroup, Button } from 'flowbite-svelte';

    let { children } = $props();
</script>

<ButtonGroup class="w-full flex jutify-evenly">
    <Button outline href="/">Home</Button>
    <Button outline href="/graph">Graph</Button>
    <Button outline href="/about">About</Button>
</ButtonGroup>

{@render children()}
