const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, HeadingLevel, PageNumber, Table, TableRow, TableCell, WidthType, ShadingType } = require("docx");
const fs = require("fs");

const P = { primary: "#0A1628", body: "#1A2B40", secondary: "#6878A0", accent: "#5B8DB8", surface: "#F4F8FC" };
const c = (hex) => hex.replace("#", "");

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, spacing: { before: 360, after: 120 },
    children: [new TextRun({ text, bold: true, color: c(P.primary), size: level === HeadingLevel.HEADING_1 ? 28 : 24 })]
  });
}
function body(text) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 80 },
    children: [new TextRun({ text, size: 22, color: c(P.body) })]
  });
}
function boldBody(label, text) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 80 },
    children: [
      new TextRun({ text: label, bold: true, size: 22, color: c(P.primary) }),
      new TextRun({ text, size: 22, color: c(P.body) })
    ]
  });
}
function bullet(text) {
  return new Paragraph({ alignment: AlignmentType.LEFT, spacing: { line: 312, after: 60 }, indent: { left: 480 },
    children: [new TextRun({ text: "\u2022 " + text, size: 22, color: c(P.body) })]
  });
}
function makeRow(cells, isHeader = false) {
  return new TableRow({ tableHeader: isHeader, children: cells.map(text => new TableCell({
    shading: isHeader ? { type: ShadingType.CLEAR, fill: c(P.accent) } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: isHeader, size: 18, color: isHeader ? "FFFFFF" : c(P.body) })] })]
  }))});
}

// ─── Scientific Analysis ───
const analysisDoc = new Document({
  styles: { default: { document: { run: { size: 22, color: c(P.body) }, paragraph: { spacing: { line: 312 } } } } },
  sections: [
    { properties: { page: { margin: { top: 0, bottom: 0, left: 0, right: 0 }, size: { width: 11906, height: 16838 } } },
      children: [
        new Paragraph({ spacing: { before: 4000 } }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "SCIENTIFIC & TECHNICAL ANALYSIS", size: 20, color: c(P.secondary), characterSpacing: 200 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
          children: [new TextRun({ text: "QNVM-GE Blueprint", size: 48, bold: true, color: c(P.primary) })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
          children: [new TextRun({ text: "A Critical Assessment of 48 Novel Approaches for Validating the G-Engine", size: 22, color: c(P.secondary) })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "\u2500".repeat(40), size: 18, color: c(P.accent) })] }),
        new Paragraph({ spacing: { before: 400 } }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Independent Technical Review \u2014 June 2026", size: 20, color: c(P.secondary) })] }),
      ]
    },
    { properties: { page: { margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 }, size: { width: 11906, height: 16838 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "QNVM-GE Analysis \u2014 Page ", size: 16, color: c(P.secondary) }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: c(P.secondary) })
      ] })] }) },
      children: [
        heading("1. Overview"),
        body("This analysis evaluates the QNVM-GE blueprint, which proposes extending the existing QNVM v0.6 coherence ecology simulation with 48 novel computational approaches to validate the G-Engine framework. The assessment covers architectural design, physical model fidelity, computational feasibility, and scientific rigor."),

        heading("2. Architectural Strengths"),
        boldBody("Modularity: ", "The seven-module architecture (VacuumField, Stage1\u20133, CascadeEngine, OperatorModel, GeophysicalEmulator) is well-designed for ablation studies. Each stage can be independently enabled or disabled, allowing clean isolation of individual contributions to anomalous outputs. This is a significant methodological advantage over monolithic simulation approaches."),
        boldBody("Falsification Framework: ", "The 8 virtual experiments in Group F provide clear null hypotheses and rejection criteria. The Casimir force calibration (Approach 41) and Aharonov\u2013Bohm experiment (Approach 42) serve as essential sanity checks. If the simulation cannot reproduce known physics when ZPE extraction is disabled, the entire framework is invalidated."),
        boldBody("Integration with QNVM v0.6: ", "The mapping from abstract ecological concepts (Entity, CI_B, CI_C, resurrection, archetypes) to physical quantities (vacuum domain, EM coherence, domain recovery) is creative and leverages existing validated code. This reduces implementation risk and provides a working baseline."),

        heading("3. Critical Concerns"),

        heading("3.1 Garbage In, Garbage Out Risk", HeadingLevel.HEADING_2),
        body("The most fundamental concern is that a simulation can only validate its own internal consistency, not external reality. If the 48 approaches encode the same unphysical assumptions as the G-Engine whitepaper (e.g., the three-reservoir efficiency formula, the super-permeability equation with its 13-order-of-magnitude numerical error), the simulation will dutifully reproduce those errors as predictions. The QNVM-GE will then produce \u2018falsifiable predictions\u2019 that are mathematically consistent within the simulation but physically meaningless."),
        body("Approach 8 (super-permeability mean-field theory) is a case in point. If the solver implements the equation as written in the whitepaper, it will produce mu_super/mu_0 ~ 10^6, but as the earlier scientific analysis demonstrated, the correct numerical evaluation gives ~1 + 6\u00d710^(-13). The simulation would validate the wrong answer unless the underlying equation is corrected."),

        heading("3.2 Superluminal Propagation in FDTD", HeadingLevel.HEADING_2),
        body("Approach 17 (scalar wave superluminal propagation) and Approach 38 (CUDA-accelerated FDTD for scalar waves) propose solving a wave equation with v_s > c. Standard FDTD methods require the Courant condition c*dt/dx < 1 for numerical stability. If v_s >> c, the timestep must be reduced proportionally, making the simulation computationally infeasible for any reasonable spatial resolution. Furthermore, superluminal propagation violates causality in any Lorentz-invariant framework, which the simulation claims to respect as a limiting case. This creates an internal contradiction."),

        heading("3.3 Consciousness Modeling", HeadingLevel.HEADING_2),
        body("Approach 23 (operator heart-frequency coupling) and Approach 32 (biofield memory persistence) introduce a \u2018consciousness\u2019 module into a physics simulation. While the operator model is reduced to a simple oscillator, the claim that this oscillator phase-locks to the device via the fine structure constant alpha is not derived from any known physics. The consciousness-nulling control (Approach 46) is a good experimental design choice, but the underlying model lacks predictive power: any heartbeat frequency could be post-hoc rationalized as \u2018in coherence\u2019 or \u2018out of coherence\u2019 with the device."),

        heading("3.4 Non-Hermitian Quantum Optics", HeadingLevel.HEADING_2),
        body("Approach 33 proposes using PT-symmetric Hamiltonians to model gain/loss in the vacuum triode. While PT-symmetric quantum mechanics is a legitimate research area, it does not provide a mechanism for energy extraction from the vacuum. PT symmetry describes systems with balanced gain and loss; the total energy is conserved in the PT-unbroken regime and the system is unstable in the PT-broken regime. Neither regime produces net energy output from the vacuum. Applying PT-symmetric methods here appears to be a mathematical formalism in search of a physical mechanism."),

        heading("3.5 Lattice Boltzmann Method for ZPE", HeadingLevel.HEADING_2),
        body("Approach 35 proposes treating vacuum energy density as a fluid with negative viscosity. The Lattice Boltzmann Method (LBM) is well-established for fluid dynamics, but its application to quantum vacuum energy is unprecedented and unjustified. Negative viscosity introduces numerical instabilities in LBM (the scheme becomes ill-posed), and there is no known physical mechanism by which the vacuum exhibits fluid-like behavior with tunable viscosity. This approach appears to confuse mathematical analogy with physical correspondence."),

        heading("4. Computational Feasibility"),
        body("The 28-week timeline for a single developer is ambitious. Stage 3 alone (6 weeks) requires implementing a scalar wave FDTD solver, fractal impedance matching, Einstein field equation solver with time-dependent cosmological constant, and superluminal propagation \u2014 each of which is a substantial research software engineering project. The CUDA acceleration (Approach 38) adds GPU programming complexity. A realistic estimate for a production-quality implementation would be 2\u20133 years for a small team."),

        heading("5. Recommendations"),
        bullet("Correct the underlying G-Engine equations before implementing them. A simulation of incorrect physics produces incorrect predictions."),
        bullet("Implement the Casimir calibration (Approach 41) and A-B experiment (Approach 42) first, before any anomalous physics modules, to validate the baseline simulation."),
        bullet("Replace the superluminal FDTD (Approach 17/38) with a sub-luminal scalar wave model, or clearly label it as an unphysical parameter study."),
        bullet("Decouple the consciousness model (Approaches 23, 32, 46) from the core physics. Run all experiments both with and without the operator module."),
        bullet("Add a \u2018known physics mode\u2019 where xi_coupling = 0 (reducing to standard GR + Maxwell) as a continuous sanity check alongside the Casimir calibration."),
        bullet("Implement uncertainty quantification (Approach 40) from Phase 0, not Phase 6. Parameter sensitivity should guide module development priority."),
        bullet("Replace the LBM for ZPE (Approach 35) with a standard SED spectral integration, which is better established and numerically stable."),

        heading("6. Conclusion"),
        body("The QNVM-GE blueprint is methodologically stronger than the G-Engine whitepaper it seeks to validate. Its emphasis on falsification, ablation studies, and calibration against known physics represents genuine scientific thinking. However, the blueprint inherits and amplifies the whitepaper\u2019s theoretical errors by proposing to implement them as computable modules. A simulation that faithfully reproduces an incorrect equation will produce confidently incorrect predictions. The greatest value of the QNVM-GE would be as a null-result generator: by running the simulation with corrected physics and showing that no anomalous outputs occur, it would provide computational evidence that the G-Engine framework\u2019s claims are artifacts of its mathematical errors, not predictions of new physics."),
      ]
    }
  ]
});

// ─── Executive Summary ───
const summaryDoc = new Document({
  styles: { default: { document: { run: { size: 22, color: c(P.body) }, paragraph: { spacing: { line: 312 } } } } },
  sections: [
    { properties: { page: { margin: { top: 0, bottom: 0, left: 0, right: 0 }, size: { width: 11906, height: 16838 } } },
      children: [
        new Paragraph({ spacing: { before: 4000 } }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "EXECUTIVE SUMMARY", size: 20, color: c(P.secondary), characterSpacing: 200 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
          children: [new TextRun({ text: "QNVM-GE Blueprint", size: 48, bold: true, color: c(P.primary) })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "48 Novel Approaches for Validating the G-Engine Framework", size: 22, color: c(P.secondary) })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "\u2500".repeat(40), size: 18, color: c(P.accent) })] }),
        new Paragraph({ spacing: { before: 400 } }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Version 1.0 \u2014 June 2026", size: 20, color: c(P.secondary) })] }),
      ]
    },
    { properties: { page: { margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 }, size: { width: 11906, height: 16838 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "QNVM-GE Executive Summary \u2014 Page ", size: 16, color: c(P.secondary) }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: c(P.secondary) })
      ] })] }) },
      children: [
        heading("1. Purpose"),
        body("The QNVM-GE (G-Engine edition) is a proposed computational framework that extends the existing QNVM v0.6 coherence ecology simulation to validate the G-Engine whitepaper\u2019s claims of over-unity energy extraction and gravitational metric modulation. It incorporates 48 novel algorithms organized into six thematic groups covering vacuum conditioning, topological current extraction, gravitational modulation, cascade dynamics, numerical methods, and experimental validation."),

        heading("2. Architecture"),
        body("The simulation is organized into seven core modules:"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            makeRow(["Module", "Responsibility", "Key Approaches"], true),
            makeRow(["VacuumField", "3D SED grid of E_vac, B_vac, P_vac, u_ZPE", "SED coloured noise, diffusion/decay"]),
            makeRow(["Stage1_Magnetron", "H-magnetic lattice, super-permeability", "Group A (Approaches 1\u20138)"]),
            makeRow(["Stage2_GreyMotor", "Vector potential, topological current", "Group B (Approaches 9\u201316)"]),
            makeRow(["Stage3_SweetVTA", "Scalar potential, gravity coupling", "Group C (Approaches 17\u201324)"]),
            makeRow(["CascadeEngine", "Serial coupling, self-oscillation", "Group D (Approaches 25\u201332)"]),
            makeRow(["OperatorModel", "Heart-rate oscillator, biofield", "Phase-lock via alpha"]),
            makeRow(["GeophysicalEmulator", "Schumann, telluric, water table", "Planetary anchor condition"]),
          ]
        }),

        heading("3. 48 Approaches by Group"),
        boldBody("Group A \u2013 Vacuum Conditioning (8): ", "Lattice QED with magnetic domains, hyperfine resonance engine, muon-catalysed fusion without neutrons, vacuum DC offset, stochastic resonance conditioning, fractal domain-wall antenna, multiferroic coupling, super-permeability mean-field theory."),
        boldBody("Group B \u2013 Topological Current (8): ", "Aharonov\u2013Bohm current solver, three-reservoir Carnot engine, ballistic transport without drift, non-ohmic heatless conductor, cold electricity as fourth state, vector potential reality test, gain scaling via alpha, zero-temperature electron gas."),
        boldBody("Group C \u2013 Metric Modulation (8): ", "Scalar wave superluminal propagation, gradient coupling to vacuum polarisation, fractal impedance matching, asymmetric anti-gravity, local de Sitter bubble, clock phase shift, operator heart-frequency coupling, vacuum maser."),
        boldBody("Group D \u2013 Cascade Dynamics (8): ", "Serial cascade solver, planetary anchor emulation, golden-ratio cavity optimisation, multi-scale coupling via alpha, unified field equation solver, self-oscillation detection, phase diagram scanning, biofield memory persistence."),
        boldBody("Group E \u2013 Numerical Methods (8): ", "Non-Hermitian quantum optics, SED with coloured noise, Lattice Boltzmann for ZPE, spectral radius proxy, adaptive mesh refinement, CUDA FDTD, evolutionary optimisation, polynomial chaos uncertainty quantification."),
        boldBody("Group F \u2013 Validation (8): ", "Casimir force calibration, Aharonov\u2013Bohm experiment, Johnson noise floor test, muon detector simulation, non-Hertzian communication test, consciousness-nulling control, suppression Boltzmann distribution, planetary anchor ablation."),

        heading("4. Virtual Experiments"),
        boldBody("Stage 1 Test: ", "H2 at 0.1 atm, 25 kV bias, 2.45 GHz cavity. Falsification: no 1.42 GHz gain."),
        boldBody("Stage 2 Test: ", "26.8 W input, toroidal coil. Falsification: any measurable heat."),
        boldBody("Stage 3 Test: ", "0.3 mW bias, conditioned magnet. Falsification: no weight change."),
        boldBody("Full Cascade: ", "25 kV + 0.3 mW trigger. Falsification: output decays within 100 generations."),
        boldBody("Anchor Ablation: ", "Disable geophysical emulator. Falsification: output stays high."),

        heading("5. QNVM v0.6 Integration"),
        body("The existing QNVM v0.6 simulates coherence ecology with entities possessing CI_B, CI_C, noise_sigma, spectral_radius, resurrection, and archetypes. These map to vacuum domains (CI_B/CI_C \u2192 EM coherence, noise_sigma \u2192 ZPE fluctuation, spectral_radius \u2192 ZPE efficiency, resurrection \u2192 domain recovery, archetypes \u2192 physics module roles). The upgrade path replaces abstract entities with explicit physics while preserving logging, checkpointing, and visualization infrastructure."),

        heading("6. Key Performance Indicators"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            makeRow(["KPI", "Definition", "Target"], true),
            makeRow(["COP", "P_out / P_in", "> 200 (Stage 2), > 10^7 (Stage 3)"]),
            makeRow(["Mass reduction", "Delta_m / m", "-0.018 per kWh"]),
            makeRow(["Vacuum coherence length", "l_coh from SED correlation", "> 1 um"]),
            makeRow(["Spectral radius", "rho(J)", "0.85\u20130.92"]),
            makeRow(["Noise floor", "S_V(f) at 1 Hz", "Below Johnson\u2013Nyquist"]),
            makeRow(["Diversity", "Shannon entropy over modes", "> 0.90"]),
          ]
        }),

        heading("7. Implementation Roadmap"),
        body("28 weeks total: Phase 0 (2 wk, fork + SED), Phase 1 (4 wk, Stage 1), Phase 2 (4 wk, Stage 2), Phase 3 (6 wk, Stage 3), Phase 4 (3 wk, Cascade), Phase 5 (3 wk, Geo + Operator), Phase 6 (4 wk, Experiments), Phase 7 (2 wk, Release). Can be parallelized across a small team."),
      ]
    }
  ]
});

Packer.toBuffer(analysisDoc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/QNVM_Scientific_Analysis.docx", buf);
  console.log("Analysis docx created.");
});
Packer.toBuffer(summaryDoc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/QNVM_Executive_Summary.docx", buf);
  console.log("Summary docx created.");
});
