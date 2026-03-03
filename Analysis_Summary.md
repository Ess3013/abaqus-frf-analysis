# Comprehensive Analysis Summary: Slenderness Ratio Sweep

This report summarizes the structural analyses performed on a 2D beam model, investigating the impact of the slenderness ratio ($w/L$) on buckling stability and dynamic frequency response.

## 1. Analysis Overview
The study consisted of a parameter sweep across seven different slenderness ratios, ranging from **1/20 (0.05)** to **1/5 (0.20)**. For each ratio, two distinct simulation types were performed:
1.  **Linear Buckling Analysis**: To determine the critical buckling load factor (eigenvalue).
2.  **Frequency Response Function (FRF)**: A steady-state dynamic analysis (100 Hz – 30,000 Hz) to measure total strain energy ($ALLSE$) response.

## 2. Model Parameters
-   **Material**: Steel ($E = 200	ext{ GPa}$, $
u = 0.3$, $ho = 7850	ext{ kg/m}^3$).
-   **Length ($L$)**: 0.005 m.
-   **Load**: Compressive concentrated force of 3,200 N per node (Total 51,200 N across 16 nodes).
-   **Boundary Conditions**: Symmetry ($XASYMM$) applied at the supports.

## 3. Results Table

| Index | Slenderness Ratio ($w/L$) | Radius ($r$) [m] | Buckling Eigenvalue ($\lambda$) | Critical Load [N] | FRF Results |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0.050 | 0.000125 | 1.8287e-03 | 93.6 | [CSV](Sweep_Files/Job_F_S_0_FRF.csv) / [Plot](Sweep_Files/Job_F_S_0_Plot.png) |
| 1 | 0.075 | 0.000188 | 9.2798e-03 | 475.1 | [CSV](Sweep_Files/Job_F_S_1_FRF.csv) / [Plot](Sweep_Files/Job_F_S_1_Plot.png) |
| 2 | 0.100 | 0.000250 | 2.8694e-02 | 1,469.1 | [CSV](Sweep_Files/Job_F_S_2_FRF.csv) / [Plot](Sweep_Files/Job_F_S_2_Plot.png) |
| 3 | 0.125 | 0.000313 | 6.9492e-02 | 3,558.0 | [CSV](Sweep_Files/Job_F_S_3_FRF.csv) / [Plot](Sweep_Files/Job_F_S_3_Plot.png) |
| 4 | 0.150 | 0.000375 | 1.4077e-01 | 7,207.4 | [CSV](Sweep_Files/Job_F_S_4_FRF.csv) / [Plot](Sweep_Files/Job_F_S_4_Plot.png) |
| 5 | 0.175 | 0.000438 | 2.5682e-01 | 13,149.2 | [CSV](Sweep_Files/Job_F_S_5_FRF.csv) / [Plot](Sweep_Files/Job_F_S_5_Plot.png) |
| 6 | 0.200 | 0.000500 | 4.2663e-01 | 21,843.5 | [CSV](Sweep_Files/Job_F_S_6_FRF.csv) / [Plot](Sweep_Files/Job_F_S_6_Plot.png) |

## 4. Observations
-   **Buckling Stability**: The critical buckling load increases non-linearly with the slenderness ratio. Increasing the width by a factor of 4 (from 0.05 to 0.20) resulted in a critical load increase of over 230x.
-   **Dynamic Response**: FRF plots show significant shifts in resonant peaks toward higher frequencies as the structure becomes stiffer (higher $w/L$). Total strain energy levels decrease significantly for stiffer structures under the same harmonic load magnitude.

## 5. File Manifest (Sweep_Files/)
-   `Job_B_S_*.inp`: Input files for buckling simulations.
-   `Job_F_S_*.inp`: Input files for FRF simulations.
-   `Job_F_S_*_FRF.csv`: Extracted Frequency vs. Strain Energy data.
-   `Job_F_S_*_Plot.png`: Log-scale visualization of the FRF response.
