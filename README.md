# QNVM-GE

**Quantum Virtual Machine — G-Engine Edition**  
**v0.2-prep / White Paper v5.0 — Falsification Edition**

A simulation bench for claims that should have been killed by arithmetic  
and were not, until someone opened the exponential.

The v0.1 snapshot shipped a three-stage vacuum-to-gravity cascade,  
forty-eight stubs, and a whitepaper that called itself triple-audited.  
The same snapshot computed \(\mu_r \approx 1.0000000000001474\),  
left every stage dark, and wrote `cascade_cop = 0` to disk.

That JSON is not an embarrassment. It is the product.

```
v4.2 said:     μ_super / μ_0  ~  10^6
the algebra:   exp(6e-13)     ~  1
the scaffold:  1.0000000000001474
the ledger:    cascade_cop = 0
```

This repository now treats those four lines as canon.  
Everything else is a test that has not yet been run.

---

## What this is

Two engines, one roof, a locked door between them.

| Engine | What it actually is | What it is not |
| --- | --- | --- |
| **QNVM v0.6** | A coherence-ecology simulator. Entities, collapse, resurrection debt, archetypes, a spatial field. | Maxwell. QED. A vacuum battery. |
| **QNVM-GE scaffold** | A staged physics skin with ablation bits, a falsification hook, and a known-physics default. | Proof that Johnson, Grey, or Sweet built a working cascade. |

The G-Engine *claim* was:

```
Stage 1  Johnson magnetron     →  vacuum conditioning
Stage 2  Grey cold-current     →  topological extraction
Stage 3  Sweet VTA             →  metric modulation
```

The G-Engine *contract* after White Paper v5.0 is:

```
Stage 1  cavity + lattice      →  measure the line, do not invent μ_r
Stage 2  gauge-fixed current   →  log ∫ J·E, do not define heat as zero
Stage 3  gravitational readout →  source T_00, do not hard-code −1.8 %/kWh
         Falsification engine  →  fail the build when the old numbers return
```

Read the corrected paper before the v4.2 TeX.  
v4.2 is an artifact under audit. v5.0 is the spec.

- Paper: [`documents/G-Engine_White_Paper_v5.0_Falsification_Edition.pdf`](documents/G-Engine_White_Paper_v5.0_Falsification_Edition.pdf)
- Markdown: [`documents/G-Engine_White_Paper_v5.0.md`](documents/G-Engine_White_Paper_v5.0.md)
- Repo of origin: [github.com/TaoishTechy/g-engine](https://github.com/TaoishTechy/g-engine)

---

## The sentence that governs the code

No solver may emit an anomalous claim until the known-physics gates pass.  
No equation may enter a solver until it is homogeneous and numerically evaluated.  
No merge may restore a withdrawn number.

CI-shaped rules, even before CI exists:

| Gate | Fail the job if |
| --- | --- |
| Permeability | `mu_r > 1.01` under published \(n_H\), \(T\), \(\mu_H\) |
| Labels | a field named `eta` is written greater than \(1\) |
| Gravity | `mass_reduction = -0.018 * kW` is hardcoded |
| Heat | `temp_rise = 0` is hardcoded while \(P_\mathrm{real} > 0\) |
| Coupling | `cascade_cop > 1` while \(\xi = 0\) |
| Operator | a failed run is explained by “incoherent operator” after the fact |

The v0.1 dry-run already satisfies the known-physics profile.  
Keep it green.

---

## Quick start

### Prerequisites

- Python 3.10+
- NumPy
- SciPy (optional; QNVM v0.6 convolutions)
- Matplotlib (optional; runtime plots)

### Coherence ecology (the working engine)

```bash
cd src/
python qnvm_v0_6.py --generations 200 --init-pop 100 --plot
```

### Physics skin (the thing under test)

```bash
cd src/

# Stage 1 only — expect μ_r ≈ 1, conditioned = false
python QNVM_GE_scaffold.py --stage 1 --generations 100 --seed 42

# Full cascade + falsification hook
python QNVM_GE_scaffold.py --cascade --falsify --output results/

# Ten-step fixture; compare against qnvm/test_results.json
python QNVM_GE_scaffold.py --cascade --verbose --generations 10
```

A “successful” physics run, today, looks like this:

```json
"super_permeability": 1.0000000000001474,
"conditioned": false,
"cascade_cop": 0.0,
"total_output_W": 0.0
```

If your fork prints \(10^6\) or COP \(261\) without a new derivation  
and a passing Casimir gate, the fork is wrong.

### Diagrams and documents

```bash
cd g-engine/ && python device_comparison.py && python capture_diagrams.py
cd ../qnvm/ && python approaches_taxonomy.py && python capture_qnvm.py

# Historical generators (v4.2 / blueprint era)
cd g-engine/ && bun run generate_analysis.js && bun run generate_summary.js
cd ../qnvm/  && bun run generate_qnvm_docs.js
```

---

## What was withdrawn

v4.2 is kept in the tree so the error remains inspectable.  
It is not the live theory.

| Object | v4.2 claim | Status |
| --- | --- | --- |
| Super-permeability | \(\mu_r \sim 10^6\) | **Withdrawn.** Exponent \(\sim 6\times 10^{-13}\). Dry-run \(\mu_r \approx 1\). |
| Three-reservoir “efficiency” | \(261\) in the body, \(2.7\times 10^9\) in the appendix | **Withdrawn as \(\eta\).** COP and \(\eta\) are different symbols. |
| Fractal impedance | \(50\,\Omega\) | **Withdrawn.** Same formula yields \(\approx 774\,\Omega\). |
| Scalar speed | \(v = c/\sin\theta_{\mathrm{Bearden}}\) | **Deleted.** Diverges. Courant lock at \(c\). |
| Anti-gravity gradient | \(\nabla\Phi_g \propto \nabla\cdot P_{\mathrm{vac}}\), \(-1.8\,\%/\mathrm{kWh}\) | **Deleted.** Rank error. No hardcoded mass drop. |
| Unconstrained \(\xi\) | “G-Engine regime” | **Default \(\xi = 0\).** Excursions must be labelled. |
| Consciousness as circuit | operator is the device | **Rejected as postulate.** Operator is switchable noise. |
| Suppression Boltzmann | physics of ridicule | **Removed from physics.** |
| Blank auditor lines | “no contradictions remain” | **Not evidence.** |

Two audit corrections, so we do not inherit counter-errors:

1. Equation 1 is dimensionally homogeneous when rewritten \(\mu_0 n \mu_H^2 / k_B T\). The failure is *magnitude*, not units.
2. The Bohr magneton makes \(\chi\) larger, not smaller, and still \(\chi \ll 1\).

---

## Five postulates (v5.0)

| ID | Postulate | Bound |
| --- | --- | --- |
| P1 | The vacuum is a ground-state field, not a heat bath. | \(\hbar\omega_c/k_B\) is an energy scale. It is not \(T_{\mathrm{vac}}\). |
| P2 | The vector potential is physical in quantum mechanics. | Phase \(e\Phi_B/\hbar\). Not a dissipationless shop-motor bus. |
| P3 | Gravity couples to the stress-energy tensor. | \(P_{\mathrm{vac}}\) is not a source. Monitor the weak energy condition. |
| P4 | \(\alpha\) is the QED coupling. | It does not glue Schumann, 1.42 GHz, heart rate, and Compton into one law. |
| P5 | Operators are electromagnetic and thermal noise. | Switchable. Pre-registered. No post-hoc “incoherence.” |

---

## Live equations

Not the README table from v0.1. That table quoted *different formulae* than the TeX.  
One sequence, evaluated.

**Lattice susceptibility** (replaces the \(10^6\) exponential)

\[
\chi \sim \frac{\mu_0 n_H \mu_H^2}{k_B T}, \qquad \mu_r = 1+\chi
\]

At \(0.1\,\mathrm{atm}\), \(300\,\mathrm{K}\), proton moment: \(\chi \sim 10^{-9}\)–\(10^{-10}\).

**Ledgers** (replaces “efficiency \(\approx 261\)”)

\[
\Delta E_{\mathrm{dev}}+\Delta E_{\mathrm{env}}+\Delta E_{\mathrm{field}}=0
\qquad
\Delta S_{\mathrm{dev}}+\Delta S_{\mathrm{env}}+\Delta S_{\mathrm{field}}\ge 0
\]

\[
\mathrm{COP}\equiv P_{\mathrm{real,out}}/P_{\mathrm{real,in}}
\qquad
\eta \equiv W/Q_{\mathrm{in}} \le 1
\]

**Gravity** (replaces the rank-mixed gradient)

\[
\nabla^2\Phi = 4\pi G\,\rho_{\mathrm{eff}}, \qquad \rho_{\mathrm{eff}}=T_{00}/c^2
\]

**Waves** (replaces \(c/\sin\theta\))

\[
v_{\mathrm{group}}\le c \quad\text{in vacuum}, \qquad c\,\Delta t/\Delta x < 1
\]

**Field equation** (replaces free \(\xi\))

\[
G_{\mu\nu}=\frac{8\pi G}{c^4}\bigl(T^{\mathrm{matter}}_{\mu\nu}+T^{\mathrm{EM}}_{\mu\nu}\bigr)
\qquad (\xi\equiv 0\ \mathrm{default})
\]

---

## Twenty-four approaches

The forty-eight stubs are a historical catalogue.  
The live grid is six groups of four. Each cell has a null and a reject rule.  
Full text lives in White Paper v5.0, §5.

| | Focus | Live cells |
| --- | --- | --- |
| **A** | Cavity and lattice | A1 Casimir-gated SED · A2 hyperfine, no assumed inversion · A3 effective-medium \(\mu(\omega)\) · A4 stochastic resonance as SNR |
| **B** | Gauge and current | B1 embedded Aharonov–Bohm · B2 gauge-fixed Maxwell · B3 topology only with a Hamiltonian · B4 dissipation ledger \(\int J\cdot E\) |
| **C** | Gravitational readout | C1 linearized GEM + WEC · C2 gravimeter forecast · C3 preferred-frame cost · C4 phase vs group velocity |
| **D** | Metrology | D1 three-account ledger · D2 `cop`/`eta` label lock · D3 real vs apparent power · D4 thermal protocol |
| **E** | Numerics | E1 FDTD locked to \(c\) · E2 polynomial-chaos UQ from day zero · E3 spectral cavity modes · E4 ablation bitmask |
| **F** | Publication gates | F1 Casimir unit test · F2 Johnson–Nyquist floor · F3 operator-off, hashed analysis · F4 known-physics CI |

v0.2 implements **A1, A3, B1, B4, D1, D2, F1, F2, F4**.  
Not a 28-week Einstein solver. Not CUDA at \(v>c\). Not Majorana in a shoebox.

Retired from the old grid and not coming back without a derivation:  
negative-viscosity lattice Boltzmann, PT-symmetry as a fuel tap,  
superluminal FDTD, muon-catalyzed fusion with the neutron channel deleted,  
suppression-Boltzmann “physics,” consciousness-as-element.

---

## Architecture

```
                    ┌─ operator = 0 (default)
                    │
 Geophysics ──▶ VacuumField ──▶ Stage 1 ──▶ Stage 2 ──▶ Stage 3
   (off)         SED + Casimir    cavity        gauge         T_00 readout
                      │             μ_r ≈ 1      ∫J·E           Δg ~ 0
                      └─────────────┴────────────┴──────────────┘
                                         │
                                 FalsificationEngine
                                 Casimir · Nyquist · η≤1
                                 μ_r gate · ξ = 0 COP gate
```

Each stage exposes `.step(prev) -> state`.  
The falsification engine runs after every generation and is allowed  
to halt the job. Decorative thresholds that the stub cannot miss  
are not falsification.

QNVM v0.6 mapping is an analogy, and the analogy stops at the door:

| Ecology | Physics skin |
| --- | --- |
| Entity | A computational domain, not a vacuum mode |
| `CI_B`, `CI_C` | Coherence scores, not \(E_{\mathrm{vac}}, B_{\mathrm{vac}}\) |
| `noise_sigma` | An agent parameter, not a ZPE amplitude |
| Resurrection | An ecology rule, not domain reheating |
| Archetypes | Roles in a population, not Maxwell modules |

Rename nothing into a field equation.

---

## Configuration

```python
@dataclass
class QNVMGEConfig:
    generations: int = 200
    seed: int = 42
    grid_size: int = 64
    sed_bandwidth: float = 1e12          # Hz
    hydrogen_pressure_atm: float = 0.1
    cavity_freq_ghz: float = 2.45
    cavity_Q: int = 10000
    magnetic_field_T: float = 0.3
    bias_voltage_kV: float = 25.0
    xi_coupling: float = 0.0             # known-physics default
    operator_enabled: bool = False
    geo_enabled: bool = False
    # vacuum_temp_eff is an energy-scale knob, not T of a Gibbs bath
```

Override from the command line. `--help` lists the rest.  
`xi_coupling` defaults to zero. Turning it on is a labelled excursion,  
not “entering the G-Engine regime.”

---

## Repository layout

```
.
├── README.md
├── VERSION.md
├── LICENSE                              Open Falsification License v1.0
│
├── g-engine/                            v4.2 assets (historical)
│   ├── g_engine.tex / g_engine.pdf
│   ├── cascade_architecture.png
│   ├── device_comparison.png
│   ├── three_reservoir.png
│   ├── suppression_curve.png            historical figure; not physics
│   ├── discoveries_mindmap.png
│   ├── *.html, *.py, generate_*.js
│
├── qnvm/                                blueprint + fixture
│   ├── qnvm_blueprint.tex / .pdf        48-stub catalogue (historical)
│   ├── approaches_taxonomy.png
│   ├── qnvm_architecture_dataflow.png
│   ├── mapping_v06_to_ge.png
│   ├── roadmap_timeline.png             28-week plan is not live scope
│   ├── test_results.json                known-physics fixture
│
├── documents/
│   ├── G-Engine_White_Paper_v5.0_Falsification_Edition.pdf
│   ├── G-Engine_White_Paper_v5.0.md
│   ├── G-Engine_White_Paper.pdf         v4.2, under audit
│   ├── G-Engine_Scientific_Analysis.docx
│   ├── G-Engine_Executive_Summary.docx
│   ├── QNVM_Blueprint.pdf / .docx
│   ├── QNVM_Scientific_Analysis.docx
│   └── QNVM_Executive_Summary.docx
│
└── src/
    ├── qnvm_v0_6.py                     coherence ecology
    └── QNVM_GE_scaffold.py              physics skin (stubs + fixture)
```

---

## Roadmap

### v0.1 — `zero-point` (shipped)

- [x] v4.2 whitepaper and QNVM 48-approach blueprint
- [x] Independent analyses that already named the 13-order error
- [x] QNVM v0.6 ecology engine
- [x] Scaffold stubs and a 10-generation dry-run
- [x] Dry-run reports \(\mu_r \approx 1\), stages off, COP \(= 0\)

### v0.2 — `ledger` (next; this is the work)

- [x] White Paper v5.0: withdrawn claims, 24 approaches, null-first protocol
- [ ] A1 Casimir gate as a unit test
- [ ] A3 effective-medium \(\mu(\omega)\); ban the \(10^6\) exponential in code
- [ ] B1 Aharonov–Bohm phase against \(e\Phi_B/\hbar\)
- [ ] B4 dissipation ledger
- [ ] D1 / D2 energy–entropy accounts and `eta` label lock
- [ ] F1 / F2 / F4 Casimir, Nyquist, known-physics CI
- [ ] Build fails on `mu_r > 1.01` or `cascade_cop > 1` at \(\xi = 0\)

### later, if the gates hold

- **v0.3 `gauge`** — B2 full Maxwell in a chosen gauge; no heatless-kilowatt shortcut
- **v0.4 `readout`** — C1–C2 gravimeter forecast from \(T_{00}\) only
- **v0.5 `ablation`** — E4 bitmask runs; D3 real-vs-apparent power reconstruction
- **v0.6 `uq`** — E2 polynomial chaos on \(n_H, Q, B, V\)
- **v1.0 `verdict`** — F3 operator-off unblinding; supported / refuted / inconclusive

There is no milestone named “self-oscillation achieved.”  
Self-oscillation after input removal is an anomaly threshold, not a deliverable.

---

## Contributing

This project runs on an **open falsification** model.  
Useful work, in descending order of rarity:

1. A null with a closed ledger.
2. An equation audit that includes the numerical evaluation.
3. An ablation that removes a module and watches the claim vanish.
4. A competing ordinary explanation (VA vs W, contact potential, gauge artifact).
5. A bug fix in the ecology engine or the boundary conditions.

Not useful:

- Restoring \(10^6\), \(261\), \(50\,\Omega\), or \(-1.8\,\%/\mathrm{kWh}\) without a new derivation.
- Adding an operator term that can absorb any failure.
- Treating QNVM resurrection logs as vacuum recovery.
- A 28-week Gantt chart for software that does not yet conserve energy.

Every claim travels with a reject rule. See [LICENSE](./LICENSE).

---

## Citation

```bibtex
@software{qnvm_ge_v50,
  title   = {QNVM-GE: Quantum Virtual Machine for G-Engine Falsification},
  author  = {Advanced Propulsion Physics Laboratory},
  version = {0.2-prep},
  date    = {2026-09-06},
  note    = {White Paper v5.0. 24 approaches. Known-physics default. Fixture COP = 0.}
}

@techreport{gengine_wp_v50,
  title       = {The G-Engine Architecture v5.0:
                 Corrected Framework for Vacuum-Coupling Hypotheses
                 under Explicit Falsification},
  institution = {Advanced Propulsion Physics Laboratory},
  year        = {2026},
  month       = sep
}
```

v0.1 (`zero-point`, 2026-06-12) remains citable as the snapshot that  
contained both the error and the dry-run that exposed it.

---

## Disclaimer

This repository evaluates extraordinary claims about vacuum extraction  
and gravitational modulation. The evaluation is the point.

White Paper v4.2 does not establish those claims.  
White Paper v5.0 withdraws the formulae that were doing the establishing.  
The scaffold is a bench. A bench that prints COP \(= 0\) under the published  
parameters is working.

Do not raise capital on `test_results.json`.  
Do not tell a laboratory that Stage 1 is “conditioned” while \(\mu_r-1\)  
sits at \(10^{-13}\).  
Do not cite an ecology simulator as cavity QED.

---

## License

**Open Falsification License (OFL) v1.0** — see [LICENSE](./LICENSE).

The license is the joke taken seriously:  
if the equation dies in public, the equation stays dead.
