const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, HeadingLevel, PageNumber, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType } = require("docx");
const fs = require("fs");

const P = {
  primary: "#0A1628",
  body: "#1A2B40",
  secondary: "#6878A0",
  accent: "#5B8DB8",
  surface: "#F4F8FC"
};
const c = (hex) => hex.replace("#", "");

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({
    heading: level,
    spacing: { before: level === HeadingLevel.HEADING_1 ? 360 : 240, after: 120 },
    children: [new TextRun({ text, bold: true, color: c(P.primary), font: { ascii: "Calibri", eastAsia: "SimHei" }, size: level === HeadingLevel.HEADING_1 ? 28 : 24 })]
  });
}

function body(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 80 },
    children: [new TextRun({ text, size: 22, color: c(P.body), font: { ascii: "Calibri" } })],
  });
}

function boldBody(label, text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 80 },
    children: [
      new TextRun({ text: label, bold: true, size: 22, color: c(P.primary), font: { ascii: "Calibri" } }),
      new TextRun({ text, size: 22, color: c(P.body), font: { ascii: "Calibri" } })
    ],
  });
}

function bullet(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 312, after: 60 },
    indent: { left: 480 },
    children: [new TextRun({ text: "\u2022 " + text, size: 22, color: c(P.body), font: { ascii: "Calibri" } })],
  });
}

function makeRow(cells, isHeader = false) {
  return new TableRow({
    tableHeader: isHeader,
    children: cells.map(text => new TableCell({
      shading: isHeader ? { type: ShadingType.CLEAR, fill: c(P.accent) } : undefined,
      margins: { top: 60, bottom: 60, left: 120, right: 120 },
      children: [new Paragraph({
        children: [new TextRun({ text, bold: isHeader, size: 20, color: isHeader ? "FFFFFF" : c(P.body), font: { ascii: "Calibri" } })]
      })]
    }))
  });
}

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Calibri" }, size: 22, color: c(P.body) },
        paragraph: { spacing: { line: 312 } },
      }
    }
  },
  sections: [
    // Cover
    {
      properties: {
        page: { margin: { top: 0, bottom: 0, left: 0, right: 0 }, size: { width: 11906, height: 16838 } }
      },
      children: [
        new Paragraph({ spacing: { before: 4000 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "EXECUTIVE SUMMARY", size: 20, color: c(P.secondary), font: { ascii: "Calibri" }, characterSpacing: 200 })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 300 },
          children: [new TextRun({ text: "The G-Engine Architecture", size: 48, bold: true, color: c(P.primary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "A Unified Framework for Vacuum Transduction,", size: 22, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 600 },
          children: [new TextRun({ text: "Scalar Electromagnetics, and Induced Gravitational Gradients", size: 22, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "\u2500".repeat(40), size: 18, color: c(P.accent) })]
        }),
        new Paragraph({ spacing: { before: 400 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
          children: [new TextRun({ text: "Based on White Paper v4.2", size: 22, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "June 2026", size: 20, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
      ]
    },
    // Body
    {
      properties: {
        page: { margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 }, size: { width: 11906, height: 16838 } }
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "G-Engine Executive Summary \u2014 Page ", size: 16, color: c(P.secondary) }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: c(P.secondary) })
            ]
          })]
        })
      },
      children: [
        heading("1. Framework Overview"),
        body("The G-Engine Architecture proposes a three-stage cascade system that extracts energy from the quantum vacuum (zero-point field) and, in its complete configuration, produces controllable gravitational gradients. The framework synthesizes historical data from three inventors\u2014Johnson (1970s magnetron motor), Grey (1970s cold current motor), and Sweet (1980s vacuum triode amplifier)\u2014with geological analysis of the Lang Island/Wardenclyffe site and mythological encoding from global traditions. The whitepaper presents 24 novel equations, 12 previously undocumented physical discoveries, and a falsifiable experimental protocol."),

        heading("2. The Three-Stage Cascade"),

        heading("Stage 1: Vacuum Conditioning (Johnson Magnetron)", HeadingLevel.HEADING_2),
        boldBody("Function: ", "Conditions the local vacuum via magnetic lattice super-permeability using hydrogen atoms intercalated between magnet domains. The hydrogen hyperfine transition (1.42 GHz, 21 cm line) resonates with the cavity's fundamental mode."),
        boldBody("Key Result: ", "Produces a super-permeable magnetic environment with mu_super/mu_0 ~ 10^6, enabling the vacuum to be 'prepared' for energy extraction in subsequent stages."),
        boldBody("Signatures: ", "1.42 GHz emission at 10^6x ambient; muon flux without neutrons; persistent current decay time > 10^5 years."),

        heading("Stage 2: Topological Current Extraction (Grey Motor)", HeadingLevel.HEADING_2),
        boldBody("Function: ", "Extracts 'cold electricity'\u2014topological (non-ohmic) current carried by the vector potential A rather than electron drift. This current produces no Joule heating."),
        boldBody("Key Result: ", "Three-reservoir thermodynamic efficiency yields eta_Grey ~ 261, matching Grey's reported 26.8 W input / 7,000 W output with zero heat signature."),
        boldBody("Signatures: ", "Zero temperature rise at output leads; Aharonov-Bohm interference pattern; gain factor > 200."),

        heading("Stage 3: Gravitational Metric Modulation (Sweet VTA)", HeadingLevel.HEADING_2),
        boldBody("Function: ", "Converts conditioned vacuum and topological current into a scalar beam that modulates the local gravitational potential. Barium ferrite magnet domain walls self-organize into a fractal antenna (D_f ~ 1.7)."),
        boldBody("Key Result: ", "For P_scalar = 24 kW, weight reduction Delta_m/m ~ -1.8% per kWh. Impedance-matched to vacuum at ~50 ohms."),
        boldBody("Signatures: ", "Weight reduction of test mass; non-Hertzian signal propagation; operator-dependent output power."),

        heading("3. Key Equations Summary"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            makeRow(["Equation", "Description", "Key Result"], true),
            makeRow(["Super-permeability", "mu_super = mu_0 * exp(n_H*mu_H^2 / k_B*T*eps_0*c^2)", "mu_super/mu_0 ~ 10^6"]),
            makeRow(["Three-reservoir efficiency", "eta = 1 - (T_c/T_h)(1 - T_vac/T_h)", "eta ~ 261 (Grey)"]),
            makeRow(["Anti-gravity gradient", "Grad(Phi_g) = -(kappa_s/c^2) * Grad . P_vac", "Delta_m/m ~ -1.8%/kWh"]),
            makeRow(["Fractal impedance", "Z_f = Z_0 * (D_f-1)/(D_f+1) * (lambda_ZPE/lambda_ph)^{D_f-2}", "Z ~ 50 ohms"]),
            makeRow(["Unified field equation", "Nabla^2(Psi_G) - (1/v_G^2)*d^2(Psi_G)/dt^2 = -(4*pi*G/c^4)*(T + T_ZPE*xi)*Psi_EM", "G-Engine regime"]),
          ]
        }),

        heading("4. Twelve Novel Discoveries"),
        bullet("Vacuum DC Offset: Nonzero DC potential at broken spatial symmetry (magnetic domain boundaries)."),
        bullet("Topological Current (Fourth State): Current carried by the winding number of A, not by electron motion."),
        bullet("Stochastic Resonance Conditioning: Sweet's conditioning tunes the SNR to the stochastic resonance peak."),
        bullet("Hydrogen Line as Universal Grid Frequency: 1.42 GHz is the frequency at which vacuum fluctuations phase-lock globally."),
        bullet("Scale Invariance via alpha: The fine structure constant (1/137) is the vacuum's attenuation factor."),
        bullet("Operator Biofield Memory: Device output persists ~3 minutes after shutdown; matches quantum memory formula."),
        bullet("Suppression Boltzmann Distribution: Suppression severity scales exponentially with output power."),
        bullet("Planetary Anchor Necessity: Devices require specific geographic nodes (Lang Island, Giza) for telluric grid coupling."),
        bullet("Golden Ratio Cavity Optimization: Aspect ratio phi:1:1/phi maximizes reactive energy fraction at 55.3%."),
        bullet("Muon-Catalyzed Fusion Without Neutrons: Cold fusion via muon catalysis with cavity field energy absorption."),
        bullet("Asymmetric Anti-Gravity: Weight reduction only when scalar beam is directed downward (local de Sitter event)."),
        bullet("Consciousness as Circuit Element: VTA output correlates with operator heart frequency via alpha."),

        heading("5. Experimental Protocol"),
        boldBody("Stage 1 Test: ", "Build hydrogen-filled magnetron cavity (f = 2.45 GHz, Q > 10^4, B = 0.3 T). Measure 1.42 GHz harmonic emission, persistent current decay, and muon flux."),
        boldBody("Stage 2 Test: ", "Construct topological current extractor (toroidal coil, pulsed DC bias). Verify zero thermal rise (< 0.1 K at 1 kW), A-B interference, and gain > 200."),
        boldBody("Stage 3 Test: ", "Build conditioned barium ferrite VTA (20:12:7 cm box, 72-hour AC+DC conditioning). Measure weight change (gravimeter at 10^(-9) g resolution), clock phase shift over 200 miles, and operator ECG correlation."),
        boldBody("Cascade Test: ", "Operate all stages in series. Expected: 0.3 mW + 25 kV input, 24 kW + 1.8% weight reduction output, self-oscillating after conditioning."),

        heading("6. Fundamental Postulates"),
        bullet("Vacuum as Open Reservoir: T_vac = hbar*omega_c/k_B >> 300 K; energy extraction thermodynamically allowed as three-reservoir process."),
        bullet("Vector Potential Reality: The Aharonov-Bohm effect confirms A is physical; 'cold electricity' is current carried by A."),
        bullet("Vacuum Polarity: Vacuum stress-energy tensor can be polarized by magnetic domains, producing gravitational gradients."),
        bullet("Scale Invariance: Coupling physics is scale-invariant via alpha = 1/137."),
        bullet("Biofield Coupling: Operator's bioelectric coherence phase-locks to the device via alpha."),

        heading("7. Mythological Encoding"),
        body("The framework identifies cross-cultural mythological correspondences to G-Engine principles: Vedic Vimana (mercury vortex = Stage 1 magnetron), Egyptian pyramid-aquifer (planetary anchor), Norse Yggdrasil nine realms (9 resonant modes of VTA), Alchemical Philosopher's Stone (conditioned magnet), Hopi Blue Star Kachina (scalar beam craft), and Tibetan Vajra (bipolar scalar output). These correspondences are presented as encoding rather than proof."),

        heading("8. Ethical Considerations"),
        body("The whitepaper raises three ethical questions: (1) Does the vacuum self-limit global ZPE extraction to prevent alpha from approaching zero, which would dissolve atomic structure? (2) If suppression represents a test, what threshold of collective coherence unlocks the technology? (3) Are scarcity, gravity, and entropy learning conditions that a species should not eliminate prematurely? The authors recommend open, international, audited replication efforts with full transparency."),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/G-Engine_Executive_Summary.docx", buf);
  console.log("Executive summary document created.");
});
