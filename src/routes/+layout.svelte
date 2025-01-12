<script lang="ts">
  import '../app.postcss';
  import { Button, Dropdown, DropdownItem, TabItem } from 'flowbite-svelte';
  import { page } from '$app/stores';

//   let tabs = ["home", "graph", "about"];
//   let selected = tabs[0];
  let { children } = $props();
</script>

<nav
  class="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600"
>
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
    <a class="flex items-center space-x-3 rtl:space-x-reverse">
      <span class="self-center pl-3 text-2xl font-semibold whitespace-nowrap dark:text-white"
        >Proof Wiki Visual Guide</span
      >
    </a>
    <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
      <Button outline class="float-right">Key</Button>
      <Dropdown style="background-color: rgba(0,0,0,0);">
        <DropdownItem class="cursor-default" style="background-color: #1f77b4;"
          >Theorem</DropdownItem
        >
        <DropdownItem class="cursor-default" style="background-color: #9467bd;"
          >Corollary</DropdownItem
        >
        <DropdownItem class="cursor-default " style="background-color: #ff7f0e;">Axiom</DropdownItem
        >
        <DropdownItem class="cursor-default" style="background-color: #2ca02c;">Proof</DropdownItem>
        <DropdownItem class="cursor-default" style="background-color: #8c564b;"
          >Definition</DropdownItem
        >
        <DropdownItem class="cursor-default" style="background-color: #d62728;">Misc</DropdownItem>
      </Dropdown>
    </div>
    <div
      class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1 pr-30"
      id="navbar-sticky"
    >
      <ul
        class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-24 md:text-xl rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
      >
        <li>
          <a
            href="/"
            class:active={$page.url.pathname == '/'}
            class="block py-2 px-3 text-gray-900 rounded  md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
            aria-current="page">Home</a
          >
        </li>
        <li>
          <a
            href="/graph"
            class:active={$page.url.pathname == '/graph'}
            class="block py-2 px-3 text-gray-900 rounded  md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
            >Graph</a
          >
        </li>
        <li>
          <a
            href="/about"
            class:active={$page.url.pathname == '/about'}
            class="block py-2 px-3 text-gray-900 rounded  md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
            >About</a
          >
        </li>
      </ul>
    </div>
  </div>
</nav>

<div class="p-5">
  {@render children()}
</div>

<style>
    .active {
      font-weight: bold;
      color: #1d4ed8; /* Tailwind blue-700 */
      border-bottom: 2px solid #1d4ed8;
    }
  </style>
