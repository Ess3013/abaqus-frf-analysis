# Abaqus Buckling Analysis Results

## Job Information

| Parameter | Value |
|-----------|-------|
| **Job Name** | Job-1 |
| **Model Name** | Model-1 |
| **Analysis Type** | Linear Buckling (*Buckle) |
| **Date** | 26-Feb-2026 |
| **Time** | 20:27:00 |
| **Status** | ✅ COMPLETED |

---

## Model Summary

| Component | Details |
|-----------|---------|
| **Element Type** | B21 (2-node linear beam in plane) |
| **Number of Elements** | 200 |
| **Number of Nodes** | 548 (148 defined + 400 internal) |
| **Total Variables** | 444 |
| **Material** | Steel |
| **Young's Modulus** | 200 GPa |
| **Poisson's Ratio** | 0.3 |
| **Beam Section** | Circular, diameter = 1 mm |

---

## Boundary Conditions & Loading

| Set | Type | Description |
|-----|------|-------------|
| **Set-5** | Boundary (XASYMM) | X-axis symmetry on bottom edge (16 nodes) |
| **Set-4** | Concentrated Load | -3200 N in Y-direction on top edge (16 nodes) |

---

## Buckling Eigenvalue Results

**Formula:** Critical Buckling Load = Eigenvalue (λ) × Applied Load (3200 N)

| Mode | Eigenvalue (λ) | Critical Buckling Load (N) | Critical Buckling Load (kN) |
|:----:|:--------------:|:--------------------------:|:---------------------------:|
| 1 | 5.3650 | 17,168 | **17.17** |
| 2 | 5.8301 | 18,656 | 18.66 |
| 3 | 7.8822 | 25,223 | 25.22 |
| 4 | 8.0947 | 25,903 | 25.90 |
| 5 | 8.5146 | 27,247 | 27.25 |

### Key Result

> **First Critical Buckling Load: 17.17 kN**
> 
> The honeycomb structure will buckle when the compressive load reaches approximately **17.2 kN**.

---

## Eigenvalue Extraction Parameters

| Parameter | Value |
|-----------|-------|
| **Method** | Subspace Iteration |
| **Number of Eigenvalues Requested** | 5 |
| **Maximum Iterations** | 30 |
| **Number of Vectors in Iteration** | 10 |
| **Load Case for Constraints** | 2 |

---

## Warnings

⚠️ **Beam Curvature Warning:**
> For 112 beam elements, the average curvature about the local 1-direction differs by more than 0.1 degrees per unit length as compared to the default curvature. This may be due to a user-specified normal or due to the nodal averaging routine used by Abaqus.

**Note:** This warning is common for honeycomb geometries and is typically acceptable for engineering analysis.

---

## Analysis Performance

| Metric | Value |
|--------|-------|
| **User Time** | 0.70 seconds |
| **System Time** | 0.00 seconds |
| **Total CPU Time** | 0.70 seconds |
| **Wallclock Time** | 1 second |

---

## Output Files Generated

| File | Description |
|------|-------------|
| `Job-1.odb` | Output database (for visualization in Abaqus/CAE) |
| `Job-1.dat` | Text output with eigenvalue results |
| `Job-1.msg` | Message file with solver information |
| `Job-1.sta` | Status file |
| `Job-1.prt` | Print file |
| `Job-1.com` | Command file |

---

## How to View Mode Shapes

To visualize the buckling mode shapes in Abaqus/CAE:

```bash
abaqus cae database=Job-1.odb
```

1. Open **Visualization** module
2. Go to `Results → Step/Frame`
3. Select buckling modes 1-5
4. View deformed shape with mode displacement contours

---

## Conclusion

The linear buckling analysis of the hexagonal honeycomb structure under compressive loading (3200 N) indicates:

- **Critical buckling load factor:** 5.365
- **First buckling mode load:** 17.17 kN
- **Analysis completed successfully** with 1 warning (beam curvature)

The structure is stable up to approximately **17.2 kN** compressive load before buckling occurs.

---

*Report generated from Abaqus Learning Edition 2025*
