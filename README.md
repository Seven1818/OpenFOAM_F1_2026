# OPENFOAM_F1_2026

OpenFOAM simulation case for the aero-thermal study of a 2026 Formula 1 front wing with active aerodynamics. Developed as part of the MSc Mechanical Engineering thesis at TU Delft (Fluid Dynamics group), using a compressible RANS approach with the k-ω SST turbulence model.

---

## Directory Structure

```
OPENFOAM_F1_2026/
├── 0/                          # Initial & boundary conditions
│   ├── include/                # Shared BC snippets (#include targets)
│   ├── alphat                  # Turbulent thermal diffusivity
│   ├── k                       # Turbulent kinetic energy
│   ├── nut                     # Turbulent kinematic viscosity
│   ├── omega                   # Specific dissipation rate
│   ├── p                       # Pressure
│   ├── T                       # Temperature
│   └── U                       # Velocity
│
├── constant/                   # Physical & turbulence model settings
│   ├── momentumTransport       # Turbulence model selection (k-ω SST)
│   └── physicalProperties      # Fluid properties (compressible, air)
│
├── system/                     # Solver control & mesh configuration
│   ├── blockMeshDict           # Background Cartesian mesh definition
│   ├── controlDict             # Run control, time-stepping, function objects
│   ├── decomposeParDict        # Domain decomposition for parallel runs
│   ├── fvConstraints           # Field constraints (e.g. reference pressure)
│   ├── fvSchemes               # Discretisation schemes
│   ├── fvSolution              # Linear solver settings & relaxation factors
│   ├── meshQualityDict         # snappyHexMesh mesh quality thresholds
│   ├── snappyHexMeshDict       # Primary snappyHexMesh config 
│   ├── streamlines             # Streamline sampling function object
│   └── surfaceFeaturesDict     # surfaceFeatureExtract config for STL feature edges
│
└── Tools/PostProcesser/        # Python post-processing pipeline (PostFOAM)
    ├── functions/              # Modular processing functions (residuals, y+, Cp, …)
    ├── base.py                 # Base classes and shared utilities
    ├── config.yaml             # YAML config: paths, stages, plot settings
    ├── DictParser.py           # OpenFOAM dictionary parser
    ├── PostProcesser.py        # Main pipeline orchestrator
    ├── ReportBuilder.py        # Automated PDF report generation
    ├── Runner_pv.py            # ParaView (pvpython) post-processing runner
    └── Runner.py               # SLURM / CLI entry point for the full pipeline
```

---

## Simulation Overview

| Parameter | Value |
|---|---|
| Solver | `fluid` (compressible, steady-state) |
| Turbulence model | k-ω SST (RANS) |
| Meshing tool | `snappyHexMesh` (half-model + symmetryPlane) |
| HPC cluster | DelftBlue (TU Delft) |
| Geometry | 2026 F1 front wing (SolidWorks --> STL) |
| Active aero configurations | Multiple flap angles |

---

## Key Workflow

1. **Mesh generation** : `surfaceFeatureExtract` → `blockMesh` → `snappyHexMesh` (pass 1 + pass 2)
2. **Decomposition** : `decomposePar` using `decomposeParDict`
3. **Solving** : `fluid` in parallel on DelftBlue
4. **Post-processing** : `PostFOAM` triggers the full pipeline: residual plots → y⁺ maps → surface Cp → forceCoeffs → PDF report

---

## Notes

- The `0/include/` directory holds reusable boundary condition snippets (e.g. inlet profiles, wall functions) referenced via `#include` in field files.
- The `Tools/PostProcesser/` pipeline is developed as a standalone open-source tool (PostFOAM) and is version-controlled separately.