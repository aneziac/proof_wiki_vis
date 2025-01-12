<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->

<script lang="ts">
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import { math, display } from 'mathlifier';

    onMount(() => {
        d3.select('body').selectAll("svg").remove();
    })

        const eq1 = `|\\text{Orb}(x)| = |G : \\text{Stab}(x)| = \\frac{|G|}{|\\text{Stab}(x)|}`
        const eq2 = `\\begin{align*}
            \\sigma_{uu}
                &= \\Gamma_{11}^1\\sigma_u+\\Gamma_{11}^2\\sigma_v+L\\textbf N \\\\
            \\sigma_{uv}
                &= \\Gamma_{12}^1\\sigma_u+\\Gamma_{12}^2\\sigma_v+M\\textbf N \\\\
            \\sigma_{vv}
                &= \\Gamma_{22}^1\\sigma_u+\\Gamma_{22}^2\\sigma_v+N\\textbf N \\\\
            \\end{align*}`;
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
    <div class="space-y-5">
        <h1 class="h1">Let's get cracking bones!</h1>
    </div>
</div>

<div class="pt-10">
    {@html display(eq1)}
</div><div class="pt-10">
    {@html display(eq2)}
</div><div class="pt-10">
    {@html display(eq3)}
</div><div class="pt-10">
    {@html display(eq4)}
</div><div class="pt-10">
    {@html display(eq5)}
</div><div class="pt-10">
    {@html display(eq6)}
</div>
