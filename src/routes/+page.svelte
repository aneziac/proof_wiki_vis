<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { math, display } from 'mathlifier';

  onMount(() => {
    d3.select('body').selectAll('svg').remove();
  });

  const eq1 = `|\\text{Orb}(x)| = |G : \\text{Stab}(x)| = \\frac{|G|}{|\\text{Stab}(x)|}`;
  const eq2 = `f(a) = \\frac{1}{2 \\pi i} \\oint_\\gamma \\frac{f(z)}{z - a} dz`

//   `\\begin{align*}
//             \\sigma_{uu}
//                 &= \\Gamma_{11}^1\\sigma_u+\\Gamma_{11}^2\\sigma_v+L\\textbf N \\\\
//             \\sigma_{uv}
//                 &= \\Gamma_{12}^1\\sigma_u+\\Gamma_{12}^2\\sigma_v+M\\textbf N \\\\
//             \\sigma_{vv}
//                 &= \\Gamma_{22}^1\\sigma_u+\\Gamma_{22}^2\\sigma_v+N\\textbf N \\\\
//             \\end{align*}`;
  const eq3 = `\\begin{align*}
            \\Gamma_{11}^1
                &= \\frac{GE_u - 2FF_u + FE_v}{2(EG - F^2)} \\quad
            &\\Gamma_{11}^2
                &= \\frac{2EF_u - EE_v - FE_u}{2(EG - F^2)} \\\\
            \\Gamma_{12}^1
                &= \\frac{GE_v - FG_u}{2(EG - F^2)} \\quad
            &\\Gamma_{12}^2
                &= \\frac{EG_u - FE_v}{2(EG - F^2)} \\\\
            \\Gamma_{22}^1
                &= \\frac{2GF_v - GG_u - FG_v}{2(EG - F^2)} \\quad
            &\\Gamma_{22}^2
                &= \\frac{EG_v - 2FF_v + FG_u}{2(EG - F^2)}.
            \\end{align*}`;
  const eq4 = `\\oint_{\\partial \\Sigma} \\mathbf{B} \\cdot \\mathrm{d}\\boldsymbol{\\ell} = \\mu_0 \\left(\\iint_{\\Sigma} \\mathbf{J} \\cdot \\mathrm{d}\\mathbf{S} + \\varepsilon_0 \\frac{\\mathrm{d}}{\\mathrm{d}t} \\iint_{\\Sigma} \\mathbf{E} \\cdot \\mathrm{d}\\mathbf{S} \\right)`;
  const eq5 = `\\mathbb F_2[a]/a^{n+1} = H^*\\left(\\mathbb{RP}^n; \\mathbb{F}_2\\right) \\leftarrow H^*\\left(\\mathbb{RP}^{n-1}; \\mathbb F_2\\right) = \\mathbb F_2[b]/b^{n}`;
  const eq6 = `\\mathfrak{g} \\supseteq [\\mathfrak{g},\\mathfrak{g}] \\supseteq [[\\mathfrak{g},\\mathfrak{g}],\\mathfrak{g}] \\supseteq [[[\\mathfrak{g},\\mathfrak{g}],\\mathfrak{g}],\\mathfrak{g}] \\supseteq \\cdots`;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
  <div class="pt-20 pb-20">
    <h1 class="h1">
      <span style="color: #EB4F27; font-weight: 900;">Proof Wiki</span> Visual Guide
    </h1>
  </div>
</div>

<div class="grid-container">
  <a href="https://en.wikipedia.org/wiki/Group_action#Orbit-stabilizer_theorem">
    <div class="grid-item">
      <h2 class="title">Orbit-Stabilizer Theorem</h2>
      <div class="pt-10 orbit-stabilizer">
        {@html display(eq1)}
      </div>
    </div>
  </a>
  <a href="https://en.wikipedia.org/wiki/Cauchy%27s_integral_formula">
    <div class="grid-item">
      <h2 class="title">Cauchy's Integral Formula</h2>
      <div class="pt-10 christoffel-1">
        {@html display(eq2)}
      </div>
    </div>
  </a>
  <a href="https://en.wikipedia.org/wiki/Christoffel_symbols">
    <div class="grid-item">
      <h2 class="title">Christoffel Symbols</h2>
      <div class="pt-10 christoffel-2">
        {@html display(eq3)}
      </div>
    </div>
  </a>
  <a href="https://en.wikipedia.org/wiki/Amp%C3%A8re%27s_circuital_law">
    <div class="grid-item">
      <h2 class="title">Ampère-Maxwell Law</h2>
      <div class="pt-10 maxwell-eq">
        {@html display(eq4)}
      </div>
    </div>
  </a>
  <a href="https://en.wikipedia.org/wiki/Borsuk%E2%80%93Ulam_theorem">
    <div class="grid-item">
      <h2 class="title">Borsuk-Ulam Theorem</h2>
      <div class="pt-10 borsuk-ulam">
        {@html display(eq5)}
      </div>
    </div>
  </a>
  <a href="https://en.wikipedia.org/wiki/Lie_group">
    <div class="grid-item">
      <h2 class="title">Lie Groups</h2>
      <div class="pt-10 lie-groups">
        {@html display(eq6)}
      </div>
    </div>
  </a>
</div>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* Two equal columns */
    gap: 25px; /* Space between the items */
  }

  .grid-item {
    display: flex; /* Flexbox for centering content */
    flex-direction: column; /* Stack title and content vertically */
    justify-content: center; /* Horizontal centering */
    align-items: center; /* Vertical centering */
    padding: 10px; /* Optional padding */
    text-align: center; /* Center align text inside the item */
  }

  .title {
    /* margin-bottom: 5px; Space between title and content */
    font-size: 1.5rem; /* Adjust font size for titles */
    font-weight: bold; /* Make titles bold */
    color: #fff; /* Change title color */
  }
</style>
