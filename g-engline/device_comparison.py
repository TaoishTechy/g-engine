import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# Font setup
fm = matplotlib.font_manager.fontManager
fm.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
fm.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

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
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.titlepad': 16,
    'legend.frameon': False,
    'legend.fontsize': 10,
    'figure.dpi': 200,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#FFFFFF',
    'savefig.pad_inches': 0.3,
})

G900, G700, G500, G400, G300, G200, G100, G50 = \
    '#111837', '#374151', '#6B7280', '#9CA3AF', '#D1D5DB', '#E5E7EB', '#F3F4F6', '#F9FAFB'
C_BLUE = '#3B82F6'
C_CYAN = '#06B6D4'
C_PURPLE = '#8B5CF6'

# ─── Chart 1: Device Comparison - Log-scale bar chart ───
fig, axes = plt.subplots(1, 3, figsize=(16, 6), constrained_layout=True)

devices = ['Johnson\nMagnetron', 'Grey\nCold Current', 'Sweet\nVTA']
colors = ['#3B82F6', '#06B6D4', '#8B5CF6']

# Input Power (W) - log scale
input_power = [0.1, 26.8, 0.0003]
bars1 = axes[0].bar(devices, input_power, color=colors, width=0.55, edgecolor='white', linewidth=0.5, zorder=3)
axes[0].set_yscale('log')
axes[0].set_title('Input Power (W)', loc='left', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Watts (log scale)')
for bar, val in zip(bars1, input_power):
    label = f'{val:.4f}' if val < 0.01 else f'{val:.1f}'
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.5,
                label, ha='center', va='bottom', fontsize=9, color=G700)
axes[0].spines['left'].set_visible(True)
axes[0].spines['left'].set_color(G200)
axes[0].yaxis.grid(True, alpha=0.08, color=G300)
axes[0].set_axisbelow(True)

# Output Power (W)
output_power = [500, 7000, 24000]
bars2 = axes[1].bar(devices, output_power, color=colors, width=0.55, edgecolor='white', linewidth=0.5, zorder=3)
axes[1].set_title('Output Power (W)', loc='left', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Watts')
for bar, val in zip(bars2, output_power):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 400,
                f'{val:,}', ha='center', va='bottom', fontsize=9, color=G700, fontweight='bold')
axes[1].set_ylim(0, max(output_power) * 1.2)
axes[1].spines['left'].set_visible(True)
axes[1].spines['left'].set_color(G200)
axes[1].yaxis.grid(True, alpha=0.08, color=G300)
axes[1].set_axisbelow(True)

# Power Gain (output/input)
gains = [5000, 261, 80000000]
bars3 = axes[2].bar(devices, gains, color=colors, width=0.55, edgecolor='white', linewidth=0.5, zorder=3)
axes[2].set_yscale('log')
axes[2].set_title('Power Gain (Output/Input)', loc='left', fontsize=13, fontweight='bold')
axes[2].set_ylabel('Gain Ratio (log scale)')
for bar, val in zip(bars3, gains):
    label = f'{val/1e6:.0f}M' if val >= 1e6 else f'{val:,}'
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.5,
                label, ha='center', va='bottom', fontsize=9, color=G700, fontweight='bold')
axes[2].spines['left'].set_visible(True)
axes[2].spines['left'].set_color(G200)
axes[2].yaxis.grid(True, alpha=0.08, color=G300)
axes[2].set_axisbelow(True)

fig.suptitle('G-Engine Device Comparison', fontsize=18, fontweight='bold', y=1.02)
fig.savefig('/home/z/my-project/download/g-engine/device_comparison.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig)
print('Device comparison chart saved.')

# ─── Chart 2: Three-Reservoir Thermodynamics ───
fig2, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

temperatures = {'T_cold (273 K)': 273, 'T_hot (300 K)': 300, 'T_vac (~10^12 K)': 1e12}
labels_t = list(temperatures.keys())
values_t = list(temperatures.values())

bars_t = ax.bar(labels_t, values_t, color=[G200, C_CYAN, C_PURPLE], width=0.5, 
                edgecolor='white', linewidth=0.5, zorder=3)
ax.set_yscale('log')
ax.set_title('Three-Reservoir Temperature Hierarchy', loc='left', fontsize=14, fontweight='bold')
ax.set_ylabel('Temperature (K, log scale)')
for bar, val in zip(bars_t, values_t):
    label = f'{val:.0f}' if val < 1e4 else f'{val:.0e}'
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 2,
            label, ha='center', va='bottom', fontsize=10, color=G700, fontweight='bold')
ax.spines['left'].set_visible(True)
ax.spines['left'].set_color(G200)
ax.yaxis.grid(True, alpha=0.08, color=G300)
ax.set_axisbelow(True)

ax.annotate('Theoretical max efficiency\n' + r'$\eta \approx 2.7 \times 10^9$',
            xy=(2, 1e12), xytext=(1.3, 1e9),
            fontsize=10, color=C_PURPLE, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=C_PURPLE, lw=1.5))

fig2.savefig('/home/z/my-project/download/g-engine/three_reservoir.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig2)
print('Three-reservoir chart saved.')

# ─── Chart 3: Suppression Boltzmann Distribution ───
fig3, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

power_levels = [50, 1000, 10000, 100000]
labels_s = ['<100 W\n(Ridicule)', '1 kW\n(Patent Denial)', '10 kW\n(Harassment)', '>100 kW\n(Lethal Response)']

x_fine = np.linspace(0, 120000, 300)
y_fine = np.exp(x_fine / 20000)

ax.plot(x_fine, y_fine, color='#CC3311', linewidth=2.5, zorder=3)
ax.fill_between(x_fine, 0, y_fine, alpha=0.06, color='#CC3311')

for pl, lb in zip(power_levels, labels_s):
    y_val = np.exp(pl / 20000)
    ax.scatter([pl], [y_val], s=80, color='#CC3311', zorder=5, edgecolors='white', linewidth=1.5)
    ax.annotate(lb, xy=(pl, y_val), xytext=(pl, y_val * 3),
                fontsize=9, color=G700, ha='center',
                arrowprops=dict(arrowstyle='->', color=G400, lw=0.8))

ax.set_yscale('log')
ax.set_title('Suppression Severity vs. Output Power', loc='left', fontsize=14, fontweight='bold')
ax.set_xlabel('Output Power (W)')
ax.set_ylabel('Suppression Level (arb. units, log)')
ax.spines['left'].set_visible(True)
ax.spines['left'].set_color(G200)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color(G200)
ax.xaxis.grid(True, alpha=0.05, color=G300)
ax.yaxis.grid(True, alpha=0.05, color=G300)
ax.set_axisbelow(True)

fig3.savefig('/home/z/my-project/download/g-engine/suppression_curve.png', dpi=200, facecolor='white', bbox_inches='tight')
plt.close(fig3)
print('Suppression curve saved.')

print('All matplotlib charts done.')
