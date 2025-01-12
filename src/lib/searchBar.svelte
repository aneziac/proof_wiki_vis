<script lang="ts">
  import { Search, Button } from 'flowbite-svelte';
  import { onMount } from 'svelte';
  import Fuse from 'fuse.js'
  import { type Node } from '../routes/graph/graphTypes'

  export let data: Node[];
  console.log(JSON.parse(JSON.stringify(data)));

//   const rawData = Reflect.get(data, '__raw__') || data;
//   console.log(rawData);

//   console.log($state.raw(data))

  const maxResults = 8;
  let showSearch = false; // State to track search bar visibility
  let searchQuery = ''; // State to bind the search input

  let results = []; // Search results

  // Fuse.js configuration
  const fuse = new Fuse(data, {
    keys: ['name'], // Fields to search in
    threshold: 0.3, // Fuzziness level (lower is stricter)
  });

  // Function to toggle the visibility of the search bar when spacebar is pressed
  const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === ' ') {
      event.preventDefault(); // Prevent the default spacebar behavior (scrolling)
      showSearch = true; // Toggle visibility of search bar
    } else if (event.key === 'Escape') {
      showSearch = false;
      searchQuery = '';
      results = [];
    }
  };

  onMount(() => {
    document.addEventListener('keydown', handleKeydown);

    return () => {
      document.removeEventListener('keydown', handleKeydown);
    };
  });

//   let results = $derived(searchQuery, (query) => {
//     return query ? fuse.search(query).map(result => result.item) : [];
//   })

  $: searchQuery, (() => {
    results = searchQuery ? fuse.search(searchQuery).map(result => result.item) : [];
  })()
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
            <li class="p-2 bg-gray-500 rounded shadow-sm text-white">
              <strong>{result.name}</strong> - {result.category}
            </li>
          {/each}
        {:else}
          <li class="text-gray-500">No results found.</li>
        {/if}
      </ul>
    </div>
  </div>
{/if}
