<script lang="ts">
    import '../app.postcss'
    import { ButtonGroup, Button, Dropdown, DropdownItem } from 'flowbite-svelte';

    let { children } = $props();
</script>

<ButtonGroup class="w-full flex justify-between">
    <div class="flex">
        <Button outline href="/">Home</Button>
        <Button outline href="/graph">Graph</Button>
        <Button outline href="/about">About</Button>
    </div>
    <div class="flex">
        <Button outline class="float-right">Key</Button>
        <Dropdown style="background-color: rgba(0,0,0,0);">
          <DropdownItem class="cursor-default" style="background-color: #1f77b4;">Theorem</DropdownItem>
          <DropdownItem class="cursor-default" style="background-color: #9467bd;">Corollary</DropdownItem>
          <DropdownItem class="cursor-default " style="background-color: #ff7f0e;">Axiom</DropdownItem>
          <DropdownItem class="cursor-default" style="background-color: #2ca02c;">Proof</DropdownItem>
          <DropdownItem class="cursor-default" style="background-color: #8c564b;">Definition</DropdownItem>
          <DropdownItem class="cursor-default" style="background-color: #d62728;">Misc</DropdownItem>
        </Dropdown>
    </div>
</ButtonGroup>

<div class="p-5">
    {@render children()}
</div>
