const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, HeadingLevel, PageNumber, BorderStyle, Table, TableRow, TableCell, WidthType, ShadingType, PageBreak } = require("docx");
const fs = require("fs");

const P = {
  primary: "#162032",
  body: "#1C2A3D",
  secondary: "#5B6B7D",
  accent: "#8B7E5A",
  surface: "#F5F7FA"
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
    children: [new TextRun({ text, size: 22, color: c(P.body), font: { ascii: "Calibri", eastAsia: "Microsoft YaHei" } })],
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

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Calibri", eastAsia: "Microsoft YaHei" }, size: 22, color: c(P.body) },
        paragraph: { spacing: { line: 312 } },
      }
    }
  },
  sections: [
    // Cover section
    {
      properties: {
        page: {
          margin: { top: 0, bottom: 0, left: 0, right: 0 },
          size: { width: 11906, height: 16838 }
        }
      },
      children: [
        new Paragraph({ spacing: { before: 4000 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "SCIENTIFIC ANALYSIS & CRITIQUE", size: 20, color: c(P.secondary), font: { ascii: "Calibri" }, characterSpacing: 200 })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({ text: "The G-Engine Architecture", size: 48, bold: true, color: c(P.primary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "A Critical Examination of Vacuum Transduction, Scalar Electromagnetics,", size: 22, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 600 },
          children: [new TextRun({ text: "and Induced Gravitational Gradients via Structured Zero-Point Energy Coupling", size: 22, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "\u2500".repeat(40), size: 18, color: c(P.accent) })]
        }),
        new Paragraph({ spacing: { before: 400 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
          children: [new TextRun({ text: "Independent Scientific Review", size: 24, bold: true, color: c(P.primary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
          children: [new TextRun({ text: "White Paper v4.2 Assessment", size: 20, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "June 2026", size: 20, color: c(P.secondary), font: { ascii: "Calibri" } })]
        }),
      ]
    },
    // Body section
    {
      properties: {
        page: {
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          size: { width: 11906, height: 16838 }
        }
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "G-Engine Scientific Analysis \u2014 Page ", size: 16, color: c(P.secondary) }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: c(P.secondary) })
            ]
          })]
        })
      },
      children: [
        heading("1. Executive Overview"),
        body("This document provides an independent scientific analysis of the G-Engine Architecture whitepaper (v4.2), which proposes a three-stage cascade system for extracting energy from the quantum vacuum and producing controllable gravitational gradients. The analysis evaluates the framework's theoretical consistency, mathematical rigor, empirical support, and adherence to established physical law. While the whitepaper presents an imaginative synthesis of historical claims and mathematical formalism, this review identifies significant scientific concerns that must be addressed before the framework can be considered physically viable."),

        heading("2. Theoretical Foundation Assessment"),

        heading("2.1 The Three-Reservoir Thermodynamic Model", HeadingLevel.HEADING_2),
        body("The framework's most consequential theoretical innovation is the extension of Carnot thermodynamics to a three-reservoir model incorporating the quantum vacuum at an effective temperature T_vac. The proposed efficiency formula is:"),
        boldBody("Equation: ", "\u03B7 = 1 \u2212 (T_cold/T_hot)(1 \u2212 T_vac/T_hot)"),
        body("This expression is dimensionally inconsistent with the standard Carnot derivation. In classical thermodynamics, the Carnot efficiency emerges from the ratio of heat flows between two reservoirs. Adding a third reservoir at T_vac does not simply multiply the cold-to-hot ratio by (1 \u2212 T_vac/T_hot); this would imply that the vacuum reservoir contributes work without any corresponding heat flow, which violates the First Law. A legitimate three-reservoir analysis would require explicit specification of the heat flows Q_1, Q_2, Q_3 and their directions, along with entropy accounting that satisfies dS_total \u2265 0 across all three reservoirs. The whitepaper provides none of this."),
        body("Furthermore, the assignment of T_vac \u2248 10^12 K based on T_vac = hbar*omega_c/k_B is physically misleading. The parameter omega_c is a cavity cutoff frequency, not a thermodynamic temperature. The quantum vacuum does not have a temperature in the conventional sense; it is not in thermal equilibrium with any reservoir. Zero-point energy is a ground-state property of quantum fields, and its extraction as usable work is prohibited by the Third Law of Thermodynamics as conventionally understood. The Casimir effect, which the whitepaper cites as precedent, produces a force but not net extractable work from the vacuum; the energy comes from the boundary conditions, not from the vacuum itself."),

        heading("2.2 Vector Potential Reality and Cold Electricity", HeadingLevel.HEADING_2),
        body("Postulate 2 correctly notes that the Aharonov-Bohm effect demonstrates the physical reality of the vector potential A in quantum mechanics. However, the leap from 'A is physical' to 'currents carried by A produce no Joule heating' is not supported. The Aharonov-Bohm effect involves phase shifts in quantum wavefunctions, not charge transport. Current in a conductor is defined by J = nev_drift, and any dissipative process involving mobile charges will produce Joule heating through electron-phonon scattering. The concept of a 'topological current' carried by the winding number of A is mathematically interesting but lacks a clear physical mechanism for energy transfer without dissipation."),
        body("The dissipationless currents in the quantum Hall effect, which the whitepaper cites as analogy, arise from topologically protected edge states in a two-dimensional electron gas under strong magnetic fields. These states exist because of the integer quantum Hall effect's bulk-boundary correspondence, not because of vacuum fluctuations. Applying this to macroscopic conductors at room temperature with no quantum well structure is not justified by any known extension of topological insulator theory."),

        heading("2.3 Vacuum Polarization and Gravitational Coupling", HeadingLevel.HEADING_2),
        body("Postulate 3 proposes that the vacuum stress-energy tensor can be polarized by magnetic domains, producing a gravitational gradient. While vacuum polarization is a real QED phenomenon (Lamb shift, Casimir effect), it occurs at the level of virtual particle-antiparticle pairs and is many orders of magnitude too weak to produce measurable gravitational effects. The proposed coupling constant kappa_s ~ 10^(-38) Nm/W from Brans-Dicke theory is the inverse of the Planck power (~3.6 x 10^52 W), meaning that to produce a 1% gravitational anomaly at 1 kW, one would need a coupling enhancement of approximately 10^50, which the framework does not provide a mechanism for."),
        body("The equation for the scalar beam velocity v_scalar = c/sin(theta) is particularly problematic. As theta approaches zero, v_scalar diverges to infinity, suggesting superluminal communication. This is not a prediction of any known scalar-tensor theory and appears to be an ad hoc construction that violates causality. In Brans-Dicke theory, scalar waves propagate at or below c, and no configuration of fields produces superluminal propagation."),

        heading("3. Mathematical Analysis"),

        heading("3.1 Super-Permeability Equation", HeadingLevel.HEADING_2),
        body("Equation 1 gives mu_super = mu_0 * exp(n_H * mu_H^2 / (k_B * T * epsilon_0 * c^2)). Let us evaluate the exponent numerically. With n_H ~ 10^25 m^(-3), mu_H ~ 1.41 x 10^(-26) J/T (nuclear magneton), T ~ 300 K, epsilon_0 = 8.85 x 10^(-12) F/m, and c = 3 x 10^8 m/s:"),
        body("Exponent = (10^25)(1.41 x 10^(-26))^2 / ((1.38 x 10^(-23))(300)(8.85 x 10^(-12))(9 x 10^16)) = (10^25 x 1.99 x 10^(-52)) / (3.30 x 10^(-15)) = 1.99 x 10^(-27) / 3.30 x 10^(-15) \u2248 6 x 10^(-13)"),
        body("This gives mu_super/mu_0 \u2248 exp(6 x 10^(-13)) \u2248 1 + 6 x 10^(-13), not the claimed 10^6 enhancement. The exponent is vanishingly small, and the equation as written cannot produce the stated result with the given parameters. This is a critical numerical error that invalidates the Stage 1 mechanism entirely."),

        heading("3.2 Three-Reservoir Efficiency", HeadingLevel.HEADING_2),
        body("The efficiency calculation in Appendix A contains a sign error. When T_vac >> T_hot, the expression (1 \u2212 T_vac/T_hot) becomes a large negative number. The claimed efficiency of ~2.7 x 10^9 is actually negative when calculated correctly:"),
        body("\u03B7 = 1 \u2212 0.91(1 \u2212 3.3 x 10^9) = 1 \u2212 0.91 + 0.91 x 3.3 x 10^9 = 1 \u2212 0.91 + 3.0 x 10^9"),
        body("While the arithmetic yields a large positive number, this is not a thermodynamic efficiency in any recognizable sense. An efficiency greater than 1 (or greater than 100%) means the device outputs more energy than it receives as heat input, which is only possible if energy enters from the third reservoir. But the third reservoir is the quantum vacuum, and no mechanism is provided for converting zero-point energy into usable work that is consistent with the Second Law. The 'efficiency' here is actually a gain ratio, not a thermodynamic efficiency, and conflating the two is a category error."),

        heading("3.3 Fractal Impedance Matching", HeadingLevel.HEADING_2),
        body("Equation 8 for the fractal impedance Z_fractal is presented without derivation or citation. The expression involves a dimensionless ratio (lambda_ZPE/lambda_phonon) raised to a fractal dimension D_f \u2212 2 = \u22120.3, yielding a factor of (10^(-12)/10^(-9))^(-0.3) = (10^(-3))^(-0.3) = 10^(0.9) \u2248 7.9. Combined with (D_f \u2212 1)/(D_f + 1) = 0.7/2.7 \u2248 0.26 and Z_0 = 377 ohms, this gives Z_fractal \u2248 377 x 0.26 x 7.9 \u2248 774 ohms, not 50 ohms as claimed. The claimed impedance match to vacuum appears to be numerically incorrect."),

        heading("4. Empirical Claims Assessment"),

        heading("4.1 Historical Inventor Accounts", HeadingLevel.HEADING_2),
        body("The whitepaper relies heavily on three historical inventor accounts (Johnson, Grey, Sweet) as empirical validation. However, these accounts share several epistemological problems. First, none of the devices have been independently replicated under controlled, published conditions. Second, the claim of 'suppression' is inherently unfalsifiable; it cannot be disproven and therefore cannot serve as scientific evidence. Third, the whitepaper presents no error analysis, no statistical confidence intervals, and no protocols for the original measurements. The 26.8 W input / 7000 W output claim for Grey's device, for instance, would require documentation of measurement methodology, instrument calibration, load characterization, and transient analysis, none of which is provided."),

        heading("4.2 Suppression Boltzmann Distribution", HeadingLevel.HEADING_2),
        body("Discovery 7 proposes that suppression severity follows an exponential distribution with output power, suggesting an 'algorithmic monitoring program.' This is presented as a scientific discovery but is actually a subjective categorization of anecdotal events. There is no statistical methodology, no control group (suppression of non-ZPE technologies for comparison), no null hypothesis testing, and no consideration of confounding variables (e.g., investment fraud detection increases with claimed returns regardless of technology type). Presenting this as a physical discovery alongside vacuum DC offset and topological current is a false equivalence that undermines the framework's scientific credibility."),

        heading("4.3 Biofield Coupling and Consciousness", HeadingLevel.HEADING_2),
        body("Postulates 5 and Discovery 12 introduce operator consciousness as a circuit element. While the whitepaper correctly identifies that human bioelectric fields exist (ECG, EEG), the claim that these fields phase-lock to a vacuum-coupled device through the fine structure constant alpha is unsupported. The fine structure constant governs electromagnetic coupling at the atomic scale; there is no known mechanism connecting it to macroscopic bioelectric coherence. Furthermore, making the operator a non-classical circuit element renders the entire framework unfalsifiable: if a replication fails, it can always be attributed to the operator's insufficient 'coherence,' which is not a measurable quantity with defined units."),

        heading("5. Conservation Law Compliance"),

        heading("5.1 Energy Conservation", HeadingLevel.HEADING_2),
        body("The framework claims to respect energy conservation by treating the vacuum as an open reservoir. However, this requires a precise accounting of energy flows. The vacuum energy density in quantum field theory is approximately 10^(113) J/m^3 (the cosmological constant problem), but only the energy above the ground state is extractable. The Casimir effect demonstrates that boundary conditions can shift the zero-point, but the energy released comes from the mechanical work done in moving the boundaries, not from the vacuum directly. The whitepaper's claim that the vacuum is an 'open thermodynamic reservoir' with an effective temperature requires a specific, testable mechanism for energy flow from the vacuum into the device, which is not provided."),

        heading("5.2 Momentum Conservation", HeadingLevel.HEADING_2),
        body("The gravitational gradient modulation proposed in Stage 3 would, if real, require momentum exchange with the gravitational field. In general relativity, this is described by the stress-energy tensor, and any local modification requires a corresponding source. The whitepaper provides no stress-energy source for the proposed metric perturbation beyond 'scalar potentials,' which are not a source term in the Einstein field equations. The proposed effect would violate the weak energy condition unless a specific exotic matter source is identified."),

        heading("6. Positive Contributions and Salvageable Elements"),

        heading("6.1 Novel Mathematical Framework", HeadingLevel.HEADING_2),
        body("Despite its physical shortcomings, the whitepaper introduces several mathematical constructs that could be repurposed in legitimate research. The fractal impedance model, if properly derived, could find application in metamaterial design. The three-reservoir thermodynamic formalism, if corrected to include proper entropy accounting, might illuminate certain quantum thermodynamic scenarios involving non-equilibrium reservoirs. The concept of structured vacuum coupling through cavity geometry is consistent with existing cavity QED research and could be explored within that established framework."),

        heading("6.2 Hypothesis Generation Value", HeadingLevel.HEADING_2),
        body("The whitepaper's greatest contribution may be as a hypothesis generator. The specific, falsifiable experimental protocol in Section 9 is commendable, even though the predicted outcomes are not supported by the theoretical framework. If the proposed experiments were conducted with proper controls, blinding, and statistical rigor, they would constitute valuable null-result publications that could redirect research efforts. The hydrogen-line cavity experiment (Stage 1 replication) is particularly amenable to rigorous testing with available laboratory equipment."),

        heading("6.3 Interdisciplinary Synthesis", HeadingLevel.HEADING_2),
        body("The synthesis of mythology, geology, and physics is unconventional but thought-provoking. While the mythological correspondences in Appendix B are not scientific evidence, they represent a pattern-recognition exercise that could, with proper anthropological methodology, yield insights into how pre-scientific cultures conceptualized natural phenomena. The geological analysis of the Wardenclyffe site could be developed into a legitimate geophysical study of electromagnetic anomalies at mineral-rich locations, independent of the ZPE framework."),

        heading("7. Critical Recommendations"),

        body("Based on this analysis, the following recommendations are offered for any future development of the G-Engine concept:"),
        bullet("Correct the numerical error in Equation 1 (super-permeability). The current exponent is 13 orders of magnitude too small to produce the claimed result."),
        bullet("Derive the three-reservoir efficiency from first principles with explicit entropy accounting, or reframe it as a gain ratio rather than thermodynamic efficiency."),
        bullet("Provide a specific, quantitative mechanism for vacuum-to-device energy transfer that is consistent with the Second Law."),
        bullet("Remove or clearly separate the 'consciousness as circuit element' claim from the core physics, as it renders the framework unfalsifiable."),
        bullet("Conduct the Stage 1 replication experiment with independent observers, pre-registered protocols, and double-blind measurement procedures."),
        bullet("Recalculate the fractal impedance (Equation 8) with a full derivation, as the current numbers do not yield 50 ohms."),
        bullet("Replace the 'suppression Boltzmann distribution' with a proper statistical analysis using a comparison group of non-ZPE technologies."),

        heading("8. Conclusion"),
        body("The G-Engine Architecture whitepaper represents an ambitious attempt to unify several unconventional physical claims into a coherent engineering framework. Its strengths lie in its mathematical specificity (24 equations), its falsifiable experimental protocol, and its interdisciplinary scope. However, the framework contains critical numerical errors (particularly in Equation 1), relies on a thermodynamic model that conflates gain ratios with efficiency, invokes mechanisms that lack derivation or empirical support (topological current, scalar beam superluminality, biofield coupling), and depends on historical accounts that are inherently unfalsifiable."),
        body("The whitepaper does not, in its current form, provide sufficient evidence or theoretical consistency to support its central claims of over-unity energy extraction and gravitational metric modulation. However, several of its mathematical constructs and experimental proposals could serve as starting points for legitimate scientific investigation if subjected to rigorous peer review, proper experimental methodology, and theoretical correction. The scientific method demands that extraordinary claims be supported by extraordinary evidence; the G-Engine whitepaper, while imaginative and systematic in its presentation, does not yet meet this standard."),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/G-Engine_Scientific_Analysis.docx", buf);
  console.log("Scientific analysis document created.");
});
