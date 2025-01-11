<script>
    import { math, display } from 'mathlifier';
    let n = 2;
    $: xN = `x^{${n}}`;
  </script>

  <div>
    Inline math (static): {@html math('A = \\pi r^2')}
  </div>
  <div>
    Inline math (dynamic): {@html math(xN)}
  </div>
  <div>
    Display math: {@html display(xN)}
  </div>
  <button on:click={() => n++}>Reactivity: increase exponent</button>
