import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Font setup
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

plt.rcParams.update({
    'font.sans-serif': ['Sarasa Mono SC', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#E5E7EB',
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'xtick.major.size': 0,
    'ytick.major.size': 0,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 200,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#FFFFFF',
})

G900, G500, G300, G200 = '#111827', '#6B7280', '#D1D5DB', '#E5E7EB'

# ─── Chart 1: 48 Approaches by Group ───
fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)

groups = ['Group A\nVacuum Conditioning\n(Stage 1)', 'Group B\nTopological Current\n(Stage 2)', 
          'Group C\nMetric Modulation\n(Stage 3)', 'Group D\nCascade\nDynamics',
          'Group E\nNumerical\nMethods', 'Group F\nValidation &\nFalsification']
colors = ['#3B82F6', '#06B6D4', '#8B5CF6', '#EF4444', '#F59E0B', '#22C55E']

approach_labels = {
    0: ['Lattice QED', 'Hyperfine resonance', 'Muon-catalyzed fusion', 'Vacuum DC offset',
        'Stochastic resonance', 'Fractal domain wall', 'Multiferroic coupling', 'Super-permeability MFT'],
    1: ['A-B current solver', '3-reservoir Carnot', 'Ballistic transport', 'Non-ohmic conductor',
        '4th current state', 'A reality test', 'Gain via alpha', 'Zero-T electron gas'],
    2: ['Scalar superluminal', 'Gradient coupling', 'Fractal impedance', 'Asymmetric anti-grav',
        'de Sitter bubble', 'Clock phase shift', 'Heart-freq coupling', 'Vacuum maser'],
    3: ['Serial cascade', 'Planetary anchor', 'Golden ratio cavity', 'Multi-scale alpha',
        'Unified field FDTD', 'Self-oscillation', 'Phase diagram', 'Biofield memory'],
    4: ['Non-Hermitian QO', 'SED coloured noise', 'Lattice Boltzmann ZPE', 'Spectral radius proxy',
        'Adaptive mesh', 'CUDA FDTD', 'Evolutionary optim', 'Polynomial chaos UQ'],
    5: ['Casimir calibration', 'A-B experiment', 'Johnson noise test', 'Muon detector sim',
        'Non-Hertzian comms', 'Consciousness-null', 'Suppression Boltz.', 'Anchor ablation'],
}

y_positions = []
y_labels = []
bar_colors = []

for i in range(6):
    for j, label in enumerate(approach_labels[i]):
        y_pos = len(groups) * 8 - (i * 8 + j) - 1
        y_positions.append(y_pos)
        y_labels.append(f'{i*8+j+1:02d}. {label}')
        bar_colors.append(colors[i])

bars = ax.barh(y_positions, [1]*48, color=bar_colors, height=0.75, 
               edgecolor='white', linewidth=0.3, zorder=3, alpha=0.85)

ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels, fontsize=8)
ax.set_xlim(0, 1.3)
ax.set_xticks([])

for i in range(6):
    y_top = (5-i) * 8 - 0.5
    y_bot = (5-i+1) * 8 - 0.5
    y_mid = (y_top + y_bot) / 2
    ax.annotate(groups[i].split('\n')[0].replace('Group ', ''), 
                xy=(1.05, y_mid), fontsize=9, fontweight='bold', 
                color=colors[i], va='center')

ax.set_title('48 Novel Approaches by Thematic Group', loc='left', fontsize=14, fontweight='bold', pad=16)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color(G300)

fig.savefig('/home/z/my-project/download/qnvm/approaches_taxonomy.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig)
print('Approaches taxonomy saved.')

# ─── Chart 2: Implementation Roadmap Timeline ───
fig2, ax = plt.subplots(figsize=(14, 5), constrained_layout=True)

phases = ['Phase 0\nFork+SED', 'Phase 1\nStage 1', 'Phase 2\nStage 2', 
          'Phase 3\nStage 3', 'Phase 4\nCascade', 'Phase 5\nGeo+Operator', 
          'Phase 6\nExperiments', 'Phase 7\nRelease']
durations = [2, 4, 4, 6, 3, 3, 4, 2]
cumulative = [0]
for d in durations:
    cumulative.append(cumulative[-1] + d)

phase_colors = ['#3B82F6', '#3B82F6', '#06B6D4', '#8B5CF6', '#EF4444', '#22C55E', '#F59E0B', '#6B7280']

for i, (phase, dur, color) in enumerate(zip(phases, durations, phase_colors)):
    ax.barh(0, dur, left=cumulative[i], height=0.5, color=color, 
            edgecolor='white', linewidth=1, zorder=3, alpha=0.85)
    mid = cumulative[i] + dur/2
    ax.text(mid, 0, phase, ha='center', va='center', fontsize=8, 
            fontweight='bold', color='white', zorder=4)

ax.set_xlim(-0.5, 29)
ax.set_ylim(-0.5, 0.8)
ax.set_yticks([])
ax.set_xlabel('Weeks')
ax.set_title('QNVM-GE Implementation Roadmap (28 weeks total)', loc='left', fontsize=14, fontweight='bold')

for w in range(0, 29, 4):
    ax.axvline(w, color=G300, linewidth=0.5, linestyle='--', zorder=1)
ax.set_xticks(range(0, 29, 4))

fig2.savefig('/home/z/my-project/download/qnvm/roadmap_timeline.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig2)
print('Roadmap timeline saved.')

# ─── Chart 3: QNVM v0.6 to QNVM-GE Mapping ───
fig3, ax = plt.subplots(figsize=(12, 5), constrained_layout=True)

v06_items = ['Entity', 'CI_B, CI_C', 'noise_sigma', 'spectral_radius', 'resurrection', 'archetypes']
ge_items  = ['Vacuum domain', 'E_vac, B_vac coherence', 'ZPE fluctuation amp.', 'Local ZPE efficiency', 'Domain recovery', 'Physics modules (S1/S2/S3)']

y_pos = np.arange(len(v06_items))
bars1 = ax.barh(y_pos - 0.2, [1]*len(v06_items), height=0.35, color='#3B82F6', 
                alpha=0.7, label='QNVM v0.6', zorder=3, edgecolor='white')
bars2 = ax.barh(y_pos + 0.2, [1]*len(ge_items), height=0.35, color='#8B5CF6', 
                alpha=0.7, label='QNVM-GE', zorder=3, edgecolor='white')

for i, (v, g) in enumerate(zip(v06_items, ge_items)):
    ax.text(0.5, i - 0.2, v, ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=4)
    ax.text(0.5, i + 0.2, g, ha='center', va='center', fontsize=8, color='white', fontweight='bold', zorder=4)
    ax.annotate('', xy=(1.05, i + 0.2), xytext=(1.05, i - 0.2),
                arrowprops=dict(arrowstyle='->', color=G500, lw=1.2))

ax.set_yticks([])
ax.set_xlim(-0.1, 1.4)
ax.set_xticks([])
ax.set_title('QNVM v0.6 \u2192 QNVM-GE Variable Mapping', loc='left', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

fig3.savefig('/home/z/my-project/download/qnvm/mapping_v06_to_ge.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig3)
print('Mapping chart saved.')

print('All QNVM charts done.')
