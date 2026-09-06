#!/usr/bin/env python3
"""
QNVM v0.6 – Balanced Recovery Ecology Engine
==============================================
A falsifiable artificial-life simulation of coherence ecology with
balanced collapse, recovery, resurrection, selection, coherence repair,
archetype roles, protected triage, and state-truth accounting.

Target regime:
- healthy_population 5000–7000
- collapsed_fraction 0.02–0.10
- avg_CI_norm_healthy >= 0.55
- avg_noise_healthy 0.018–0.030
- avg_spectral_radius_proxy 0.85–0.92
- rolling death rate < 0.10
- diversity_healthy >= 0.90

Usage:
    python qnvm_v0_6.py --generations 200 --init-pop 100 --plot
    python qnvm_v0_6.py --seed-count 32 --branches 16
"""

import argparse
import csv
import json
import math
import os
import sys
import time
import pickle
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Callable
from collections import Counter
import numpy as np

# ----------------------------------------------------------------------
# Optional dependencies
# ----------------------------------------------------------------------
try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

try:
    from scipy.ndimage import convolve
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    # Simple fallback convolution (box blur) if scipy missing
    def convolve(image, kernel, mode='wrap'):
        h, w = image.shape
        kh, kw = kernel.shape
        pad_h = kh // 2
        pad_w = kw // 2
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='wrap')
        result = np.zeros_like(image)
        for i in range(h):
            for j in range(w):
                region = padded[i:i+kh, j:j+kw]
                result[i, j] = np.sum(region * kernel)
        return result

# ----------------------------------------------------------------------
# Entity States
# ----------------------------------------------------------------------
class EntityState(Enum):
    ACTIVE = "active"
    UNSTABLE = "unstable"
    COLLAPSED = "collapsed"
    DORMANT = "dormant"
    RESURRECTED = "resurrected"
    DEAD = "dead"

# ----------------------------------------------------------------------
# Equation Registry (E001–E097) – core functions (unchanged from v0.5)
# ----------------------------------------------------------------------
@dataclass
class EquationSpec:
    id: str
    name: str
    layer: str
    status: str
    inputs: List[str]
    outputs: List[str]
    bounds: Dict[str, Tuple[float, float]]
    units: Dict[str, str]
    callable: Optional[Callable] = None
    test_name: Optional[str] = None
    notes: str = ""

class EquationRegistry:
    def __init__(self):
        self.specs: Dict[str, EquationSpec] = {}
        self._register_core()
        self._register_v04()
    
    def _register_core(self):
        self.register(EquationSpec(
            id="E001", name="coherence_stabilization", layer="core", status="implemented",
            inputs=["CI_B", "CI_C", "rho"], outputs=["CI_B_new", "CI_C_new"],
            bounds={"CI_B": (0,1), "CI_C": (0,1)}, units={},
            callable=self._coherence_stabilization,
            notes="Stabilizes coherence rather than conserving"
        ))
        self.register(EquationSpec(
            id="E002", name="field_nudge", layer="core", status="implemented",
            inputs=["CI", "field_coherence"], outputs=["CI_new"],
            bounds={"CI": (0,1), "field_coherence": (0,1)}, units={},
            callable=self._field_nudge,
            notes="Nudges entity coherence toward local field value"
        ))
        self.register(EquationSpec(
            id="E003", name="soft_collapse_gate", layer="core", status="implemented",
            inputs=["noise_sigma", "spectral_radius", "sigma_crit", "rho_crit", "steepness"],
            outputs=["collapse_prob"],
            bounds={"collapse_prob": (0,1)}, units={},
            callable=self._soft_collapse_gate,
            notes="Probability of collapse with dead zone"
        ))
        self.register(EquationSpec(
            id="E004", name="resurrection_probability", layer="core", status="implemented",
            inputs=["faith", "res_coherence", "internal_noise", "debt", "scar_load", "threshold"],
            outputs=["prob"],
            bounds={"prob": (0,1)}, units={},
            callable=self._resurrection_probability,
            notes="Debt and scars reduce probability"
        ))
        self.register(EquationSpec(
            id="E005", name="recovery_probability", layer="core", status="implemented",
            inputs=["noise_sigma", "recovery_sigma", "collapse_age", "max_collapse_age"],
            outputs=["prob"],
            bounds={"prob": (0,1)}, units={},
            callable=self._recovery_probability,
            notes="Increases with low noise and long collapse age"
        ))
        # E006–E096 stubs
        for i in range(6, 97):
            self.register(EquationSpec(
                id=f"E{i:03d}", name=f"eq_{i:03d}", layer="core", status="stub",
                inputs=[], outputs=[], bounds={}, units={},
                notes="Not yet implemented"
            ))
    
    def _register_v04(self):
        self.register(EquationSpec(
            id="E097", name="true_spectral_radius", layer="core", status="implemented",
            inputs=["matrix"], outputs=["rho"],
            bounds={"rho": (0, None)}, units={},
            callable=self._true_spectral_radius,
            notes="Computes spectral radius from 2x2 Jacobian"
        ))
    
    def register(self, spec: EquationSpec):
        self.specs[spec.id] = spec
    
    def implemented_count(self) -> int:
        return sum(1 for s in self.specs.values() if s.status == "implemented")
    
    def stub_count(self) -> int:
        return sum(1 for s in self.specs.values() if s.status == "stub")
    
    def report(self) -> str:
        total = len(self.specs)
        return (f"Equation registry: {self.implemented_count()}/{total} implemented, "
                f"{self.stub_count()}/{total} stubs")
    
    # ----- Implemented equations -----
    @staticmethod
    def _coherence_stabilization(ci_b, ci_c, rho, dt=1.0):
        sigma_topo = 0.01 * max(0, rho - 0.95)
        delta = sigma_topo * dt
        return ci_b + delta*0.5, ci_c + delta*0.5
    
    @staticmethod
    def _field_nudge(ci, field_coherence):
        return ci + 0.01 * field_coherence * (1 - ci)
    
    @staticmethod
    def _soft_collapse_gate(noise_sigma, spectral_radius, sigma_crit, rho_crit, steepness=8.0):
        # Dead zone: stable if noise and rho are well below thresholds
        if noise_sigma < 0.85 * sigma_crit and spectral_radius < 0.95 * rho_crit:
            return 0.0
        a = steepness
        sigmoid = lambda x: 1 / (1 + np.exp(-a * x))
        p_noise = sigmoid(noise_sigma - sigma_crit)
        p_rho = sigmoid(spectral_radius - rho_crit)
        return min(1.0, p_noise + p_rho - p_noise * p_rho)
    
    @staticmethod
    def _resurrection_probability(faith, res_coh, internal_noise, debt, scar_load, threshold=0.5):
        base = max(0.0, min(0.4, 2.0 * (faith - threshold) * res_coh * (1 - 0.5*internal_noise)))
        penalty = np.exp(-debt/10.0) * (1 - scar_load)
        return base * penalty
    
    @staticmethod
    def _recovery_probability(noise_sigma, recovery_sigma, collapse_age, max_collapse_age):
        noise_factor = max(0, 1 - noise_sigma / max(0.01, recovery_sigma))
        age_factor = min(1, collapse_age / max(1, max_collapse_age))
        return noise_factor * age_factor
    
    @staticmethod
    def _true_spectral_radius(matrix):
        eigvals = np.linalg.eigvals(matrix)
        return float(max(abs(eigvals)))

# ----------------------------------------------------------------------
# Simulation Configuration
# ----------------------------------------------------------------------
@dataclass
class QNVMConfig:
    generations: int = 200
    init_pop: int = 100
    seed: int = 42
    carrying_capacity: int = 10_000
    sigma_crit: float = 0.048
    rho_crit: float = 1.0
    recovery_sigma: float = 0.037
    faith_threshold: float = 0.5
    spatial: bool = True
    field_size: int = 64
    use_weather_events: bool = False
    ultra_efficient: bool = False
    anti_monoculture_lambda: float = 0.3
    resurrection_debt_factor: float = 0.05
    identity_fragmentation_rate: float = 0.03
    max_collapse_age: int = 12
    min_resurrection_age: int = 3          # increased from v0.5
    soft_collapse: bool = True
    collapse_steepness: float = 8.0
    true_spectral_radius: bool = False
    target_diversity: float = 0.75
    rare_archetype_boost: float = 0.3
    mutation_rate: float = 0.04
    mutation_strength: float = 0.05
    hybrid_archetype_chance: float = 0.02
    archetype_mutation_chance: float = 0.01
    debt_decay_rate: float = 0.01
    coherence_selection_exponent: float = 1.25    # new
    min_active_survival_prob: float = 0.70       # new
    coherence_repair_rate: float = 0.004         # new
    # Archetype role flags (all True by default)
    enable_archetype_roles: bool = True
    # Multiverse
    seed_count: int = 1
    branches: int = 1
    ablation: List[str] = field(default_factory=list)
    # Output
    outdir: str = "."
    checkpoint_interval: int = 0
    log_interval: int = 1

# ----------------------------------------------------------------------
# Spatial Field (unchanged from v0.5)
# ----------------------------------------------------------------------
class SpatialField:
    def __init__(self, size: int):
        self.size = size
        self.coherence = np.ones((size, size), dtype=np.float32) * 0.5
        self.noise = np.zeros((size, size), dtype=np.float32)
        self.resource = np.ones((size, size), dtype=np.float32)
        self.memory = np.zeros((size, size), dtype=np.float32)
    
    def diffuse(self, rate=0.1):
        kernel = np.array([[0.05, 0.1, 0.05],
                           [0.1, 0.4, 0.1],
                           [0.05, 0.1, 0.05]])
        self.coherence = (1-rate)*self.coherence + rate*convolve(self.coherence, kernel, mode='wrap')
        self.noise = (1-rate)*self.noise + rate*convolve(self.noise, kernel, mode='wrap')
        self.resource = (1-rate)*self.resource + rate*convolve(self.resource, kernel, mode='wrap')
        self.memory = (1-rate)*self.memory + rate*convolve(self.memory, kernel, mode='wrap')
    
    def decay(self, rate=0.01):
        self.coherence *= (1 - rate)
        self.noise *= (1 - rate)
        self.resource *= (1 - rate)
        self.memory *= (1 - rate)
        np.clip(self.coherence, 0, 1, out=self.coherence)
        np.clip(self.noise, 0, 1, out=self.noise)
        np.clip(self.resource, 0.1, 1, out=self.resource)
    
    def deposit(self, x, y, coh_delta=0, noise_delta=0, res_delta=0, mem_delta=0):
        ix = int(x) % self.size
        iy = int(y) % self.size
        self.coherence[ix, iy] = float(np.clip(self.coherence[ix, iy] + coh_delta, 0, 1))
        self.noise[ix, iy] = float(np.clip(self.noise[ix, iy] + noise_delta, 0, 1))
        self.resource[ix, iy] = float(np.clip(self.resource[ix, iy] + res_delta, 0.1, 1))
        self.memory[ix, iy] = float(np.clip(self.memory[ix, iy] + mem_delta, 0, 1))
    
    def sample(self, x, y):
        ix = int(x) % self.size
        iy = int(y) % self.size
        return (self.coherence[ix, iy], self.noise[ix, iy],
                self.resource[ix, iy], self.memory[ix, iy])

# ----------------------------------------------------------------------
# Entity (individual) – v0.6 with same slots + archetype role support
# ----------------------------------------------------------------------
class Entity:
    __slots__ = ('id', 'archetype', 'traits', 'x', 'y', 'CI_B', 'CI_C', 'precision',
                 'boundary', 'temporal', 'spectral_radius_proxy', 'true_spectral_radius',
                 'noise_sigma', 'rank_efficiency', 'faith', 'biophoton', 'vitality',
                 'internal_noise', 'resurrection_coherence', 'resurrection_amplifier',
                 'instability_bias', 'mycelial_connectivity', 'logos_coupling',
                 'state', 'collapse_age', 'resurrect_cooldown', 'resurrected',
                 'age', 'resurrection_debt', 'resurrection_scars', 'identity_fragmentation',
                 'parent_id', 'lineage_id', 'mutation_distance')
    def __init__(self, eid: int, archetype: str, rng: np.random.Generator,
                 config: QNVMConfig, spatial: bool, parent_id: Optional[int] = None,
                 lineage_id: Optional[int] = None):
        self.id = eid
        self.archetype = archetype
        self.traits = 0
        if spatial:
            self.x = rng.uniform(0, config.field_size)
            self.y = rng.uniform(0, config.field_size)
        else:
            self.x = self.y = 0.0
        
        base_coh = {"Explorer":0.70, "Philosopher":0.90, "Creator":0.80,
                    "Scientist":0.85, "Strategist":0.75, "Empath":0.95, "Rebel":0.60}[archetype]
        base_ent = {"Explorer":0.3, "Philosopher":0.5, "Creator":0.4,
                    "Scientist":0.2, "Strategist":0.6, "Empath":0.2, "Rebel":0.8}[archetype]
        drift_bias = {"Explorer":0.20, "Philosopher":0.15, "Creator":0.18,
                      "Scientist":0.12, "Strategist":0.25, "Empath":0.10, "Rebel":0.35}[archetype]
        
        self.CI_B = np.clip(base_coh + rng.uniform(-0.1, 0.1), 0, 1)
        self.CI_C = np.clip(base_ent + rng.uniform(-0.1, 0.1), 0, 1)
        self.precision = rng.uniform(-1, 1)
        self.boundary = rng.uniform(-1, 1)
        self.temporal = rng.uniform(-1, 1)
        self.spectral_radius_proxy = rng.uniform(0.5, 0.9)
        self.true_spectral_radius = 0.0
        self.noise_sigma = rng.uniform(0.01, 0.05)
        self.rank_efficiency = rng.uniform(0.7, 0.9)
        self.faith = rng.uniform(0.3, 0.9)
        self.biophoton = 1.0 + 3.0 * rng.random()
        self.vitality = 100.0
        self.internal_noise = rng.uniform(0.0, 0.8)
        self.resurrection_coherence = 1.0
        self.resurrection_amplifier = rng.uniform(0.3, 1.0)
        self.instability_bias = drift_bias + rng.uniform(-0.05, 0.05)
        self.mycelial_connectivity = rng.uniform(0.5, 1.0)
        self.logos_coupling = rng.uniform(0.0, 0.5)
        self.state = EntityState.ACTIVE
        self.collapse_age = 0
        self.resurrect_cooldown = 0
        self.resurrected = False
        self.age = 0
        self.resurrection_debt = 0
        self.resurrection_scars = 0.0
        self.identity_fragmentation = 0.0
        self.parent_id = parent_id
        self.lineage_id = lineage_id if lineage_id is not None else eid
        self.mutation_distance = 0.0

# ----------------------------------------------------------------------
# Main Simulation – QNVM v0.6
# ----------------------------------------------------------------------
class QNVM:
    def __init__(self, config: QNVMConfig, branch_id: int = 0):
        self.config = config
        self.branch_id = branch_id
        if config.seed_count > 1:
            self.rng = np.random.default_rng(config.seed + branch_id)
        else:
            self.rng = np.random.default_rng(config.seed)
        self.registry = EquationRegistry()
        self.field = SpatialField(config.field_size) if config.spatial else None
        self.entities: List[Entity] = []
        self.generation = 0
        self.history = []
        self.phase_log = []
        self.resurrection_log = []
        self.death_log = []
        self.birth_log = []                # new
        self.archetype_counts = []
        self.archetype_lifecycle = []      # new per-generation
        self.field_history = []            # new
        self.next_id = 1
        self.lineage_counter = 1
        self._init_population()
    
    def _init_population(self):
        archetypes = ["Explorer","Philosopher","Creator","Scientist","Strategist","Empath","Rebel"]
        for _ in range(self.config.init_pop):
            arch = self.rng.choice(archetypes)
            e = Entity(self.next_id, arch, self.rng, self.config, self.config.spatial)
            self.entities.append(e)
            self.next_id += 1
            self.lineage_counter = max(self.lineage_counter, e.lineage_id + 1)
    
    # ------------------------------------------------------------------
    # Standardised logging
    # ------------------------------------------------------------------
    def log_death(self, e=None, *, eid=None, cause: str, extra: Optional[Dict[str, Any]] = None):
        row = {
            "generation": self.generation,
            "id": e.id if e is not None else eid,
            "archetype": e.archetype if e is not None else "",
            "cause": cause,
            "age": e.age if e is not None else "",
            "collapse_age": e.collapse_age if e is not None else "",
            "noise_sigma": float(e.noise_sigma) if e is not None else "",
            "spectral_radius_proxy": float(e.spectral_radius_proxy) if e is not None else "",
            "state": e.state.value if e is not None else "",
            "lineage_id": e.lineage_id if e is not None else "",
            "parent_id": e.parent_id if e is not None else "",
            "resurrection_debt": float(e.resurrection_debt) if e is not None else "",
            "resurrection_scars": float(e.resurrection_scars) if e is not None else "",
            "identity_fragmentation": float(e.identity_fragmentation) if e is not None else "",
        }
        if extra:
            row.update(extra)
        self.death_log.append(self._json_convert(row))
    
    def log_birth(self, child: Entity, parent: Entity, mutation_distance: float):
        """Log birth event for lineage tracking."""
        self.birth_log.append({
            "generation": self.generation,
            "child_id": child.id,
            "parent_id": parent.id,
            "parent_state": parent.state.value,
            "parent_archetype": parent.archetype,
            "child_archetype": child.archetype,
            "CI_B": float(child.CI_B),
            "CI_C": float(child.CI_C),
            "noise_sigma": float(child.noise_sigma),
            "mutation_distance": mutation_distance
        })
    
    # ------------------------------------------------------------------
    # Archetype role functions (field-level)
    # ------------------------------------------------------------------
    def apply_archetype_roles(self, e, field_coh, field_noise, field_res, field_mem):
        if not self.config.enable_archetype_roles:
            return
        # Empath: reduces local field noise
        if e.archetype == "Empath":
            self.field.deposit(e.x, e.y, noise_delta=-0.002)
        # Scientist: reduces local spectral radius proxy (via field memory)
        elif e.archetype == "Scientist":
            self.field.deposit(e.x, e.y, mem_delta=-0.002)  # memory as proxy for spectral damping
        # Creator: increases field coherence and memory
        elif e.archetype == "Creator":
            self.field.deposit(e.x, e.y, coh_delta=0.002, mem_delta=0.002)
        # Philosopher: boosts recovery through memory (handled in recovery)
        # Strategist: improves survival under high selection (handled in survival)
        # Explorer: moves (handled in migration)
        # Rebel: adds noise (handled below)
        if e.archetype == "Rebel":
            self.field.deposit(e.x, e.y, noise_delta=0.001)
    
    # ------------------------------------------------------------------
    # Migration for Explorer archetype
    # ------------------------------------------------------------------
    def migrate_explorer(self, e):
        if e.archetype != "Explorer" or e.state not in (EntityState.ACTIVE, EntityState.UNSTABLE):
            return
        # Move toward higher resource/coherence
        if self.field:
            # Sample current field
            fcoh, fnoise, fres, fmem = self.field.sample(e.x, e.y)
            # Try a random nearby point
            dx = self.rng.uniform(-2, 2)
            dy = self.rng.uniform(-2, 2)
            new_x = e.x + dx
            new_y = e.y + dy
            ncoh, nnoise, nres, nmem = self.field.sample(new_x, new_y)
            # Move if resource or coherence is meaningfully better
            if (nres > fres + 0.05) or (ncoh > fcoh + 0.05):
                e.x = new_x % self.config.field_size
                e.y = new_y % self.config.field_size
    
    # ------------------------------------------------------------------
    # Core dynamics (recovery, resurrection, soft collapse, etc.)
    # ------------------------------------------------------------------
    def _soft_collapse(self, e):
        prob = EquationRegistry._soft_collapse_gate(
            e.noise_sigma, e.spectral_radius_proxy,
            self.config.sigma_crit, self.config.rho_crit,
            self.config.collapse_steepness
        )
        if self.rng.random() < prob:
            e.state = EntityState.COLLAPSED
            e.collapse_age = 0
            if self.field:
                self.field.deposit(e.x, e.y, coh_delta=-0.05, noise_delta=0.1, mem_delta=0.2)
            return True
        return False
    
    def _recover(self, e):
        # Base probability from equation
        prob = EquationRegistry._recovery_probability(
            e.noise_sigma, self.config.recovery_sigma,
            e.collapse_age, self.config.max_collapse_age
        )
        # Archetype boost: Philosopher improves recovery
        if self.config.enable_archetype_roles and e.archetype == "Philosopher":
            prob *= 1.2
        # Field memory boost (if any)
        if self.field:
            _, _, _, fmem = self.field.sample(e.x, e.y)
            prob *= (1 + fmem * 0.5)
        if self.rng.random() < prob:
            e.state = EntityState.ACTIVE
            e.collapse_age = 0
            e.CI_B = np.clip(e.CI_B * 1.2, 0, 1)
            e.CI_C = np.clip(e.CI_C * 0.5, 0, 1)
            e.noise_sigma = np.clip(e.noise_sigma * 0.8, 0, 0.2)
            if self.field:
                self.field.deposit(e.x, e.y, coh_delta=0.1, noise_delta=-0.05, mem_delta=0.1)
            return True
        return False
    
    def _attempt_resurrection(self, e):
        if e.state != EntityState.COLLAPSED:
            return False
        if e.collapse_age < self.config.min_resurrection_age:
            return False
        prob = EquationRegistry._resurrection_probability(
            e.faith, e.resurrection_coherence, e.internal_noise,
            e.resurrection_debt, e.resurrection_scars, self.config.faith_threshold
        )
        # Make resurrection probability peak at collapse_age 4-6
        if 4 <= e.collapse_age <= 6:
            prob *= 1.5
        if self.rng.random() < prob:
            collapse_age_before = e.collapse_age
            e.state = EntityState.RESURRECTED
            e.resurrect_cooldown = 5
            e.resurrected = True
            e.resurrection_debt += 1
            e.resurrection_scars += 0.05
            e.identity_fragmentation += self.config.identity_fragmentation_rate
            e.CI_B = np.clip(e.CI_B * 1.2, 0, 1)
            e.CI_C = np.clip(e.CI_C * 0.5, 0, 1)
            e.internal_noise = 0.0
            e.noise_sigma = np.clip(e.noise_sigma * 0.5, 0, 0.05)
            e.collapse_age = 0
            if self.field:
                self.field.deposit(e.x, e.y, coh_delta=0.15, mem_delta=0.2)
            self.resurrection_log.append({
                "generation": self.generation,
                "id": e.id,
                "archetype": e.archetype,
                "age": e.age,
                "collapse_age": collapse_age_before,
                "debt_after": e.resurrection_debt,
                "scars_after": e.resurrection_scars,
                "faith": float(e.faith),
            })
            return True
        return False
    
    def _coherence_repair(self, e):
        """Active coherence repair for healthy entities in good fields."""
        if e.state not in (EntityState.ACTIVE, EntityState.UNSTABLE, EntityState.RESURRECTED):
            return
        if not self.field:
            return
        fcoh, fnoise, fres, fmem = self.field.sample(e.x, e.y)
        if fnoise < self.config.recovery_sigma * 0.8:  # low noise zone
            repair = self.config.coherence_repair_rate
            e.CI_B += repair * (fcoh - e.CI_B)
            e.CI_C += repair * (fmem - e.CI_C)  # memory repairs CI_C
            e.CI_B = float(np.clip(e.CI_B, 0, 1))
            e.CI_C = float(np.clip(e.CI_C, 0, 1))
    
    def _survival_probability(self, e, archetype_freq, total_active):
        # Base: coherence to exponent * (1 - noise)
        ci_norm = (e.CI_B + e.CI_C) / 2.0
        base = (ci_norm ** self.config.coherence_selection_exponent) * (1 - e.noise_sigma)
        # Anti-monoculture penalty
        penalty = 1 - self.config.anti_monoculture_lambda * (archetype_freq ** 2)
        # Rare boost
        if archetype_freq < 0.1 and self.config.rare_archetype_boost > 0:
            boost = 1 + self.config.rare_archetype_boost * (1 - archetype_freq/0.1)
        else:
            boost = 1.0
        base_prob = base * penalty * boost
        
        # State-specific modifications
        if e.state == EntityState.ACTIVE:
            prob = base_prob
            # Minimum survival protection for high-coherence, low-noise
            if ci_norm > 0.55 and e.noise_sigma < 0.025:
                prob = max(prob, self.config.min_active_survival_prob)
        elif e.state == EntityState.UNSTABLE:
            prob = base_prob * 0.8
        elif e.state == EntityState.RESURRECTED:
            fragility = 1.0 - min(0.5, e.resurrect_cooldown / 5.0)
            prob = base_prob * fragility
        elif e.state == EntityState.COLLAPSED:
            # Collapsed survival uses recovery probability as base, but with triage protection
            rec_prob = EquationRegistry._recovery_probability(
                e.noise_sigma, self.config.recovery_sigma,
                e.collapse_age, self.config.max_collapse_age
            )
            if e.collapse_age <= 2:
                # Protected triage: no selection death
                prob = 1.0
            elif e.collapse_age <= 8:
                prob = rec_prob * 0.5
            else:
                prob = rec_prob * 0.2  # steep decline after 8
        else:
            prob = base_prob * 0.5
        return np.clip(prob, 0.05, 1.0)
    
    def step(self):
        self.generation += 1
        
        # 1. Field dynamics
        if self.field:
            self.field.diffuse(0.1)
            self.field.decay(0.01)
            # Archetype field effects (applied before entity updates)
            for e in self.entities:
                if e.state not in (EntityState.DEAD, EntityState.DORMANT):
                    fcoh, fnoise, fres, fmem = self.field.sample(e.x, e.y)
                    self.apply_archetype_roles(e, fcoh, fnoise, fres, fmem)
        
        # 2. Coherence dynamics and field nudges for active/unstable/resurrected
        for e in self.entities:
            if e.state in (EntityState.ACTIVE, EntityState.UNSTABLE, EntityState.RESURRECTED):
                fcoh, fnoise, fres, fmem = self.field.sample(e.x, e.y) if self.field else (0.5, 0.0, 1.0, 0.0)
                # Field nudge
                e.CI_B = EquationRegistry._field_nudge(e.CI_B, fcoh)
                e.noise_sigma = EquationRegistry._field_nudge(e.noise_sigma, 1 - fnoise)  # invert
                e.noise_sigma = float(np.clip(e.noise_sigma, 0, 0.2))
                e.CI_B = float(np.clip(e.CI_B, 0, 1))
                # Coherence stabilization
                new_b, new_c = EquationRegistry._coherence_stabilization(e.CI_B, e.CI_C, e.spectral_radius_proxy)
                e.CI_B, e.CI_C = new_b, new_c
                e.CI_B = float(np.clip(e.CI_B, 0, 1))
                e.CI_C = float(np.clip(e.CI_C, 0, 1))
                # Spectral radius proxy
                e.spectral_radius_proxy = (e.CI_B + e.CI_C) * (1 - e.noise_sigma) + self.rng.normal(0, 0.01)
                e.spectral_radius_proxy = np.clip(e.spectral_radius_proxy, 0, 2)
                if self.config.true_spectral_radius:
                    eps = 1e-6
                    J = np.zeros((2,2))
                    J[0,0] = 1 - 0.01 * max(0, e.spectral_radius_proxy - 0.95)
                    J[0,1] = 0.5 * 0.01 * max(0, e.spectral_radius_proxy - 0.95)
                    J[1,0] = 0.5 * 0.01 * max(0, e.spectral_radius_proxy - 0.95)
                    J[1,1] = 1 - 0.01 * max(0, e.spectral_radius_proxy - 0.95)
                    e.true_spectral_radius = float(max(abs(np.linalg.eigvals(J))))
                e.precision = (e.CI_B + e.CI_C) / (1 + e.noise_sigma)
                e.precision = np.clip(e.precision, -2, 2)
                e.vitality *= 0.999 if e.faith > self.config.faith_threshold else 0.99
                e.vitality = np.clip(e.vitality, 80, 100)
                e.biophoton = 1.0 + 3.0 * e.faith * (1 - e.internal_noise)
                e.biophoton = np.clip(e.biophoton, 0, 20)
                # Active coherence repair
                self._coherence_repair(e)
                # Unstable detection
                if (e.noise_sigma > 0.85 * self.config.sigma_crit or
                    e.spectral_radius_proxy > 0.95 * self.config.rho_crit):
                    e.state = EntityState.UNSTABLE
                else:
                    if e.state == EntityState.UNSTABLE:
                        e.state = EntityState.ACTIVE
        
        # 3. Phase transitions and collapse
        enter_count = 0
        for e in self.entities:
            if e.state in (EntityState.ACTIVE, EntityState.UNSTABLE):
                if self.config.soft_collapse:
                    if self._soft_collapse(e):
                        enter_count += 1
                else:
                    if (e.noise_sigma > self.config.sigma_crit or
                        e.spectral_radius_proxy > self.config.rho_crit):
                        e.state = EntityState.COLLAPSED
                        e.collapse_age = 0
                        if self.field:
                            self.field.deposit(e.x, e.y, coh_delta=-0.05, noise_delta=0.1, mem_delta=0.2)
                        enter_count += 1
        
        # 4. Aging, recovery, resurrection, debt decay
        recover_count = 0
        resurrect_events = 0
        for e in self.entities:
            # Debt decay
            e.resurrection_debt = max(0, e.resurrection_debt - self.config.debt_decay_rate)
            if e.state == EntityState.COLLAPSED:
                e.collapse_age += 1
                if e.collapse_age <= 2:
                    # Protected triage: no recovery attempt, just wait
                    pass
                else:
                    if self._recover(e):
                        recover_count += 1
                    elif self._attempt_resurrection(e):
                        resurrect_events += 1
                    elif e.collapse_age >= self.config.max_collapse_age:
                        e.state = EntityState.DEAD
                        self.log_death(e, cause="collapse_timeout")
            elif e.state == EntityState.RESURRECTED:
                if e.resurrect_cooldown > 0:
                    e.resurrect_cooldown -= 1
                else:
                    e.state = EntityState.ACTIVE
            # Age all non-dead, non-collapsed (collapsed ages separately)
            if e.state not in (EntityState.DEAD, EntityState.COLLAPSED, EntityState.DORMANT):
                e.age += 1
                e.CI_B *= (1 - e.identity_fragmentation * 0.01)
                e.CI_C *= (1 - e.identity_fragmentation * 0.01)
                e.CI_B = float(np.clip(e.CI_B, 0, 1))
                e.CI_C = float(np.clip(e.CI_C, 0, 1))
                if e.parent_id is not None:
                    e.mutation_distance += self.rng.exponential(0.1)
        
        # 5. Migration for Explorers
        if self.config.enable_archetype_roles:
            for e in self.entities:
                if e.state not in (EntityState.DEAD, EntityState.COLLAPSED, EntityState.DORMANT):
                    self.migrate_explorer(e)
        
        # 6. Survival selection with state-aware probabilities
        all_non_dead = [e for e in self.entities if e.state != EntityState.DEAD]
        total_non_dead = len(all_non_dead)
        if total_non_dead == 0:
            # Extinction: record final metrics and stop stepping
            self._record_metrics(enter_count, recover_count, resurrect_events)
            return
        arch_counts = Counter(e.archetype for e in all_non_dead)
        survivors = []
        for e in all_non_dead:
            freq = arch_counts[e.archetype] / max(1, total_non_dead)
            prob = self._survival_probability(e, freq, total_non_dead)
            if self.rng.random() < prob:
                survivors.append(e)
            else:
                self.log_death(e, cause="selection")
        
        # 7. Reproduction – only ACTIVE, UNSTABLE, and RESURRECTED (after cooldown)
        def can_reproduce(e):
            if e.state in (EntityState.ACTIVE, EntityState.UNSTABLE):
                return True
            if e.state == EntityState.RESURRECTED and e.resurrect_cooldown == 0:
                return True
            return False
        
        repro_rate = 0.4 * max(0, 1 - len(survivors) / self.config.carrying_capacity)
        new_entities = []
        for e in survivors:
            if can_reproduce(e) and self.rng.random() < repro_rate:
                child = self._reproduce(e)
                new_entities.append(child)
        
        # 8. Fitness-weighted capacity enforcement
        self.entities = survivors + new_entities
        if len(self.entities) > self.config.carrying_capacity:
            health = [(e, (e.CI_B+e.CI_C)/2 * (e.vitality/100) / (1 + e.resurrection_debt))
                      for e in self.entities]
            health.sort(key=lambda x: x[1], reverse=True)
            self.entities = [e for e, _ in health[:self.config.carrying_capacity]]
            removed = len(health) - self.config.carrying_capacity
            for e, _ in health[self.config.carrying_capacity:]:
                self.log_death(e, cause="capacity_exceeded")
        
        # 9. Record metrics
        self._record_metrics(enter_count, recover_count, resurrect_events)
    
    def _reproduce(self, parent: Entity) -> Entity:
        r = self.rng.random()
        if r < self.config.hybrid_archetype_chance and parent.parent_id is not None:
            mates = [e for e in self.entities if e.state not in (EntityState.DEAD, EntityState.COLLAPSED)
                     and e.id != parent.id
                     and (not self.config.spatial or abs(e.x - parent.x) < 5.0)]
            if mates:
                mate = self.rng.choice(mates)
                arch = self.rng.choice([parent.archetype, mate.archetype])
            else:
                arch = parent.archetype
        elif r < self.config.hybrid_archetype_chance + self.config.archetype_mutation_chance:
            archetypes = ["Explorer","Philosopher","Creator","Scientist","Strategist","Empath","Rebel"]
            arch = self.rng.choice([a for a in archetypes if a != parent.archetype])
        else:
            arch = parent.archetype
        
        child = Entity(self.next_id, arch, self.rng, self.config,
                       self.config.spatial, parent_id=parent.id, lineage_id=parent.lineage_id)
        self.next_id += 1
        # Mutation with probability mutation_rate
        if self.rng.random() < self.config.mutation_rate:
            child.CI_B = np.clip(parent.CI_B + self.rng.normal(0, self.config.mutation_strength), 0, 1)
            child.CI_C = np.clip(parent.CI_C + self.rng.normal(0, self.config.mutation_strength), 0, 1)
            child.faith = np.clip(parent.faith + self.rng.normal(0, self.config.mutation_strength), 0, 1)
            child.noise_sigma = np.clip(parent.noise_sigma + self.rng.normal(0, self.config.mutation_strength*0.5), 0, 0.2)
        else:
            child.CI_B = parent.CI_B
            child.CI_C = parent.CI_C
            child.faith = parent.faith
            child.noise_sigma = parent.noise_sigma
        child.resurrection_debt = max(0, parent.resurrection_debt - 0.5)
        child.resurrection_scars = max(0, parent.resurrection_scars - 0.1)
        child.identity_fragmentation = max(0, parent.identity_fragmentation - 0.1)
        mutation_dist = abs(child.CI_B - parent.CI_B) + abs(child.CI_C - parent.CI_C)
        child.mutation_distance = parent.mutation_distance + mutation_dist
        if self.config.spatial:
            child.x = parent.x + self.rng.uniform(-2, 2)
            child.y = parent.y + self.rng.uniform(-2, 2)
        # Log birth
        self.log_birth(child, parent, mutation_dist)
        return child
    
    def _record_metrics(self, enter, recover, resurrect_events):
        # State counts
        active_cnt = sum(1 for e in self.entities if e.state == EntityState.ACTIVE)
        unstable_cnt = sum(1 for e in self.entities if e.state == EntityState.UNSTABLE)
        collapsed_cnt = sum(1 for e in self.entities if e.state == EntityState.COLLAPSED)
        resurrected_cnt = sum(1 for e in self.entities if e.state == EntityState.RESURRECTED)
        dormant_cnt = sum(1 for e in self.entities if e.state == EntityState.DORMANT)
        dead_this_gen = len([d for d in self.death_log if d.get("generation") == self.generation])
        
        pop_non_dead = active_cnt + unstable_cnt + collapsed_cnt + resurrected_cnt + dormant_cnt
        healthy_pop = active_cnt + unstable_cnt + resurrected_cnt
        
        # Guard against division by zero
        if pop_non_dead == 0:
            # Extinction: record zeros
            metrics = {
                "generation": self.generation,
                "population_non_dead": 0,
                "healthy_population": 0,
                "collapsed_fraction": 0.0,
                "resurrected_fraction": 0.0,
                "active_count": 0,
                "unstable_count": 0,
                "collapsed_count": 0,
                "resurrected_count": 0,
                "dormant_count": 0,
                "dead_this_gen": dead_this_gen,
                "death_rate": 0.0,
                "rolling_death_rate_10gen": 0.0,
                "avg_CI_norm_all": 0.0,
                "avg_CI_norm_healthy": 0.0,
                "avg_spectral_radius_proxy": 0.0,
                "avg_noise_sigma": 0.0,
                "avg_noise_healthy": 0.0,
                "avg_rank_efficiency": 0.0,
                "enter_transitions": enter,
                "recover_transitions": recover,
                "resurrected_this_gen": resurrect_events,
                "efficiency_violation": False,
                "diversity_shannon": 0.0,
                "diversity_normalized_all": 0.0,
                "diversity_normalized_healthy": 0.0,
                "effective_archetypes_all": 0,
                "effective_archetypes_healthy": 0,
                "avg_faith": 0.0,
                "avg_faith_healthy": 0.0,
                "avg_ctc_stability": 0.0,
                "avg_drift": 0.0,
                "total_resurrection_events": len(self.resurrection_log),
                "total_resurrection_debt": 0.0,
                "avg_resurrection_debt": 0.0,
                "median_resurrection_debt": 0.0,
                "max_resurrection_debt": 0.0,
            }
            metrics = self._json_convert(metrics)
            self.history.append(metrics)
            self.archetype_counts.append({"generation": self.generation})
            return
        
        collapsed_fraction = collapsed_cnt / pop_non_dead
        resurrected_fraction = resurrected_cnt / pop_non_dead
        
        # Averages for healthy entities
        healthy_entities = [e for e in self.entities if e.state in (EntityState.ACTIVE, EntityState.UNSTABLE, EntityState.RESURRECTED)]
        if healthy_entities:
            avg_CI_healthy = np.mean([(e.CI_B + e.CI_C)/2.0 for e in healthy_entities])
            avg_noise_healthy = np.mean([e.noise_sigma for e in healthy_entities])
            faith_healthy = np.mean([e.faith for e in healthy_entities])
            # Healthy diversity
            arch_counts_healthy = Counter(e.archetype for e in healthy_entities)
            probs_healthy = np.array([c/len(healthy_entities) for c in arch_counts_healthy.values()])
            shannon_healthy = -np.sum(probs_healthy * np.log(probs_healthy + 1e-9))
            effective_healthy = np.exp(shannon_healthy) if shannon_healthy > 0 else 1
            norm_diversity_healthy = shannon_healthy / np.log(len(arch_counts_healthy)) if len(arch_counts_healthy) > 1 else 1.0
        else:
            avg_CI_healthy = 0.0
            avg_noise_healthy = 0.0
            faith_healthy = 0.0
            norm_diversity_healthy = 0.0
            effective_healthy = 0
        
        # Debt metrics
        debts = [e.resurrection_debt for e in self.entities if e.state != EntityState.DEAD]
        avg_debt = np.mean(debts) if debts else 0.0
        median_debt = np.median(debts) if debts else 0.0
        max_debt = max(debts) if debts else 0.0
        
        # Overall averages (for backward compatibility)
        all_non_dead = [e for e in self.entities if e.state != EntityState.DEAD]
        if all_non_dead:
            ci_sum_all = np.mean([e.CI_B + e.CI_C for e in all_non_dead])
            rho_all = np.mean([e.spectral_radius_proxy for e in all_non_dead])
            sigma_all = np.mean([e.noise_sigma for e in all_non_dead])
            rank_eff_all = np.mean([e.rank_efficiency for e in all_non_dead])
            faith_all = np.mean([e.faith for e in all_non_dead])
            ci_vals_all = [e.CI_B + e.CI_C for e in all_non_dead]
            ctc_stability = 1.0 / (1.0 + np.var(ci_vals_all) * 10)
            drift_all = np.mean([e.instability_bias + 0.5*e.internal_noise for e in all_non_dead])
        else:
            ci_sum_all = rho_all = sigma_all = rank_eff_all = faith_all = ctc_stability = drift_all = 0.0
        
        # Overall diversity
        arch_counts_all = Counter(e.archetype for e in all_non_dead)
        probs_all = np.array([c/len(all_non_dead) for c in arch_counts_all.values()]) if all_non_dead else []
        shannon_all = -np.sum(probs_all * np.log(probs_all + 1e-9)) if len(probs_all) > 0 else 0
        norm_diversity_all = shannon_all / np.log(len(arch_counts_all)) if len(arch_counts_all) > 1 else 1.0
        
        # Death rate
        death_rate = dead_this_gen / max(1, healthy_pop) if healthy_pop > 0 else 0
        # Rolling death rate (simple 10-gen average)
        if not hasattr(self, '_death_rate_history'):
            self._death_rate_history = []
        self._death_rate_history.append(death_rate)
        if len(self._death_rate_history) > 10:
            self._death_rate_history.pop(0)
        rolling_death_rate = np.mean(self._death_rate_history) if self._death_rate_history else 0
        
        # Field metrics
        if self.field:
            avg_field_coherence = float(np.mean(self.field.coherence))
            avg_field_noise = float(np.mean(self.field.noise))
            avg_field_resource = float(np.mean(self.field.resource))
            avg_field_memory = float(np.mean(self.field.memory))
        else:
            avg_field_coherence = avg_field_noise = avg_field_resource = avg_field_memory = 0.0
        self.field_history.append({
            "generation": self.generation,
            "avg_field_coherence": avg_field_coherence,
            "avg_field_noise": avg_field_noise,
            "avg_field_resource": avg_field_resource,
            "avg_field_memory": avg_field_memory
        })
        
        metrics = {
            "generation": self.generation,
            "population_non_dead": pop_non_dead,
            "healthy_population": healthy_pop,
            "collapsed_fraction": collapsed_fraction,
            "resurrected_fraction": resurrected_fraction,
            "active_count": active_cnt,
            "unstable_count": unstable_cnt,
            "collapsed_count": collapsed_cnt,
            "resurrected_count": resurrected_cnt,
            "dormant_count": dormant_cnt,
            "dead_this_gen": dead_this_gen,
            "death_rate": death_rate,
            "rolling_death_rate_10gen": rolling_death_rate,
            "avg_CI_norm_all": ci_sum_all / 2.0 if all_non_dead else 0.0,
            "avg_CI_norm_healthy": avg_CI_healthy,
            "avg_spectral_radius_proxy": rho_all,
            "avg_noise_sigma": sigma_all,
            "avg_noise_healthy": avg_noise_healthy,
            "avg_rank_efficiency": rank_eff_all,
            "enter_transitions": enter,
            "recover_transitions": recover,
            "resurrected_this_gen": resurrect_events,
            "efficiency_violation": rank_eff_all > 0.93,
            "diversity_shannon": shannon_all,
            "diversity_normalized_all": norm_diversity_all,
            "diversity_normalized_healthy": norm_diversity_healthy,
            "effective_archetypes_all": np.exp(shannon_all) if shannon_all > 0 else 1,
            "effective_archetypes_healthy": effective_healthy,
            "avg_faith": faith_all,
            "avg_faith_healthy": faith_healthy,
            "avg_ctc_stability": ctc_stability,
            "avg_drift": drift_all,
            "total_resurrection_events": len(self.resurrection_log),
            "total_resurrection_debt": float(sum(debts)),
            "avg_resurrection_debt": avg_debt,
            "median_resurrection_debt": median_debt,
            "max_resurrection_debt": max_debt,
        }
        # Add warning flags
        if collapsed_fraction > 0.5:
            metrics["warning_collapse_churn"] = True
        if healthy_pop / pop_non_dead < 0.4 and pop_non_dead > 0:
            metrics["warning_low_health"] = True
        if resurrect_events > 0.1 * pop_non_dead and self.generation > self.config.generations - 25:
            metrics["warning_resurrection_dependency"] = True
        if norm_diversity_healthy > 0.9:
            metrics["flag_diversity_success"] = True
        if avg_CI_healthy < 0.5:
            metrics["warning_low_coherence"] = True
        if rolling_death_rate > 0.10:
            metrics["warning_high_death_rate"] = True
        if avg_noise_healthy < 0.015 and rho_all < 0.78:
            metrics["warning_over_stabilized"] = True
        
        metrics = self._json_convert(metrics)
        self.history.append(metrics)
        
        # Archetype counts
        self.archetype_counts.append({
            "generation": self.generation,
            **{arch: arch_counts_all[arch] for arch in arch_counts_all}
        })
        
        # Archetype lifecycle summary (per generation)
        lifecycle_row = {"generation": self.generation}
        for arch in ["Explorer","Philosopher","Creator","Scientist","Strategist","Empath","Rebel"]:
            arch_entities = [e for e in all_non_dead if e.archetype == arch]
            count = len(arch_entities)
            births = sum(1 for b in self.birth_log if b.get("generation") == self.generation and b.get("child_archetype") == arch)
            deaths = sum(1 for d in self.death_log if d.get("generation") == self.generation and d.get("archetype") == arch)
            lifecycle_row[f"{arch}_count"] = count
            lifecycle_row[f"{arch}_births"] = births
            lifecycle_row[f"{arch}_deaths"] = deaths
        self.archetype_lifecycle.append(lifecycle_row)
        
        if enter > 0 or recover > 0:
            self.phase_log.append({"generation": self.generation, "entered": int(enter), "recovered": int(recover)})
    
    def _json_convert(self, obj):
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: self._json_convert(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self._json_convert(i) for i in obj]
        return obj
    
    # ------------------------------------------------------------------
    # Resilient CSV writers (union schemas)
    # ------------------------------------------------------------------
    @staticmethod
    def _write_dicts_csv(filename: str, rows: List[Dict[str, Any]], preferred: Optional[List[str]] = None):
        if not rows:
            return
        all_keys = set()
        for row in rows:
            all_keys.update(row.keys())
        preferred = preferred or []
        fieldnames = [k for k in preferred if k in all_keys]
        fieldnames += sorted(k for k in all_keys if k not in fieldnames)
        with open(filename, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            for row in rows:
                w.writerow(row)
    
    def write_history_csv(self, filename: str):
        self._write_dicts_csv(filename, self.history,
                              preferred=["generation", "healthy_population", "collapsed_fraction",
                                         "diversity_normalized_healthy", "avg_CI_norm_healthy",
                                         "death_rate", "rolling_death_rate_10gen"])
    
    def write_archetype_csv(self, filename: str):
        self._write_dicts_csv(filename, self.archetype_counts, preferred=["generation"])
    
    def write_phase_csv(self, filename: str):
        self._write_dicts_csv(filename, self.phase_log, preferred=["generation", "entered", "recovered"])... (22 KB left)
