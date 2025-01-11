<script lang="ts">
    import '../app.postcss'

	let { children } = $props();
</script>

<nav>
	<a href="/">Home</a>
	<a href="/graph">Graph</a>
	<a href="/about">About</a>
    <a href="/mathex">Math Example</a>
</nav>

{@render children()}
