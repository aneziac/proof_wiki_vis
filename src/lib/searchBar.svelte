<script lang="ts">
  import { Search, Button, Dropdown, DropdownItem } from 'flowbite-svelte';
  import { onMount } from 'svelte';
  import { SearchOutline, ChevronDownOutline } from 'flowbite-svelte-icons';
  import Fuse from 'fuse.js'

  // let { data } = $props();

  let showSearch = false; // State to track search bar visibility
  let searchQuery = ''; // State to bind the search input

  let results = []; // Search results

  const data = [
    { name: 'Apple', category: 'Fruit' },
    { name: 'Banana', category: 'Fruit' },
    { name: 'Carrot', category: 'Vegetable' },
    { name: 'Dragonfruit', category: 'Fruit' },
    { name: 'Eggplant', category: 'Vegetable' },
    { name: 'Fig', category: 'Fruit' },
  ];

  // Fuse.js configuration
  const fuse = new Fuse(data, {
    keys: ['name', 'category'], // Fields to search in
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

  $: searchQuery, (() => {
    results = searchQuery ? fuse.search(searchQuery).map(result => result.item) : [];
  })()
</script>

<!-- {#if showSearch}
  <form class="flex">
    <div class="relative">
      <Button class="rounded-e-none whitespace-nowrap border border-e-0 border-primary-700">
        {selectCategory}
        <ChevronDownOutline class="w-2.5 h-2.5 ms-2.5" />
      </Button>
      <Dropdown classContainer="w-40">
        {#each items as { label }}
          <DropdownItem
            on:click={() => {
              selectCategory = label;
            }}
            class={selectCategory === label ? 'underline' : ''}
          >
            {label}
          </DropdownItem>
        {/each}
      </Dropdown>
    </div>
    <Search
      autofocus
      size="md"
      class="rounded-none py-2.5"
      placeholder="Search..."
      bind:value={searchQuery}
    />
    <Button class="!p-2.5 rounded-s-none">
      <SearchOutline class="w-6 h-6" />
    </Button>
  </form>
{/if} -->


{#if showSearch}
  <div class="fixed top-0 left-0 w-full h-full bg-gray-900 bg-opacity-75 flex items-center justify-center">
    <div class="bg-white p-4 rounded shadow-lg w-1/2">
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
          {#each results as result}
            <li class="p-2 bg-gray-100 rounded shadow-sm">
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
