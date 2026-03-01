import os
import re
import subprocess
import numpy as np

# Parameters
L_link = 0.005  # Nominal link length in meters (5mm)
slenderness_ratios = np.linspace(0.05, 0.2, 7)  # from 1/20 to 1/5

# Input files
input_buckling_base = 'Buckling/Job-1.inp'
input_frf_base = 'Job-1.inp'
results_file = 'Slenderness_Sweep_Results.md'

def run_abaqus_job(job_name, input_file):
    print(f"Running Abaqus job: {job_name}")
    try:
        cmd = f"abaqus job={job_name} input={input_file} interactive ask_delete=OFF"
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running job {job_name}: {e}")
        return False

def parse_eigenvalue(dat_file):
    if not os.path.exists(dat_file):
        print(f"Dat file {dat_file} not found.")
        return None
    
    eigenvalue = None
    try:
        with open(dat_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "MODE NO      EIGENVALUE" in line:
                    for j in range(i+1, min(i+10, len(lines))):
                        match = re.search(r'\s+1\s+([\d.E+-]+)', lines[j])
                        if match:
                            eigenvalue = float(match.group(1))
                            return eigenvalue
    except Exception as e:
        print(f"Error parsing dat file: {e}")
    return eigenvalue

def extract_frf_data(root_dir, odb_rel_path, csv_rel_path):
    # odb_rel_path and csv_rel_path are relative to Sweep_Files
    # we are currently IN Sweep_Files
    print(f"Extracting FRF data from {odb_rel_path}")
    try:
        # Script is in root
        script_path = os.path.join(root_dir, 'extract_frf.py')
        odb_path = os.path.abspath(odb_rel_path)
        csv_path = os.path.abspath(csv_rel_path)
        
        cmd = f'abaqus python "{script_path}" "{odb_path}" "{csv_path}"'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting FRF from {odb_rel_path}: {e}")
        return False

def plot_frf_data(root_dir, csv_rel_path, png_rel_path):
    print(f"Plotting FRF data from {csv_rel_path}")
    try:
        script_path = os.path.join(root_dir, 'plot_frf_sweep.py')
        csv_path = os.path.abspath(csv_rel_path)
        png_path = os.path.abspath(png_rel_path)
        
        cmd = f'python "{script_path}" "{csv_path}" "{png_path}"'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error plotting FRF from {csv_rel_path}: {e}")
        return False

def main():
    root_dir = os.getcwd()
    
    if not os.path.exists(input_buckling_base) or not os.path.exists(input_frf_base):
        print("Required base input files not found.")
        return

    with open(input_buckling_base, 'r') as f:
        buckling_content = f.read()
    with open(input_frf_base, 'r') as f:
        frf_content = f.read()

    results = []
    sweep_dir = 'Sweep_Files'
    if not os.path.exists(sweep_dir):
        os.makedirs(sweep_dir)

    for i, S in enumerate(slenderness_ratios):
        w = S * L_link
        r = w / 2.0
        
        # 1. Buckling Analysis
        job_b = f"Job_B_S_{i}"
        inp_b = os.path.join(sweep_dir, f"{job_b}.inp")
        
        pattern = r"(\*Beam Section,.*?section=CIRC\s*\r?\n)([\d.e+-]+)"
        new_b_content = re.sub(pattern, r"\g<1>" + f"{r:.6f}", buckling_content)
        with open(inp_b, 'w') as f: f.write(new_b_content)
        
        os.chdir(sweep_dir)
        # Check if already done to save time if re-running
        if not os.path.exists(f"{job_b}.dat"):
            success_b = run_abaqus_job(job_b, f"{job_b}.inp")
        else:
            success_b = True
        eigenvalue = parse_eigenvalue(f"{job_b}.dat") if success_b else None
        os.chdir(root_dir)
        
        # 2. FRF Analysis
        job_f = f"Job_F_S_{i}"
        inp_f = os.path.join(sweep_dir, f"{job_f}.inp")
        
        new_f_content = re.sub(pattern, r"\g<1>" + f"{r:.6f}", frf_content)
        with open(inp_f, 'w') as f: f.write(new_f_content)
        
        os.chdir(sweep_dir)
        if not os.path.exists(f"{job_f}.odb"):
            success_f = run_abaqus_job(job_f, f"{job_f}.inp")
        else:
            success_f = True
            
        csv_path = f"{job_f}_FRF.csv"
        png_path = f"{job_f}_Plot.png"
        if success_f:
            if extract_frf_data(root_dir, f"{job_f}.odb", csv_path):
                plot_frf_data(root_dir, csv_path, png_path)
        os.chdir(root_dir)
        
        if success_b or success_f:
            results.append({
                'S': S, 'w': w, 'r': r, 
                'eigenvalue': eigenvalue,
                'frf_csv': csv_path if os.path.exists(os.path.join(sweep_dir, csv_path)) else None,
                'frf_plot': png_path if os.path.exists(os.path.join(sweep_dir, png_path)) else None
            })
            print(f"S={S:.3f} -> Buckling λ={eigenvalue}, FRF complete.")

    # Write summary
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("# Slenderness Ratio Parameter Sweep Results\n\n")
        f.write("Includes both Buckling and FRF (Steady State Dynamics) analyses.\n\n")
        f.write("| Slenderness Ratio (w/L) | Width (w) [m] | Radius (r) [m] | Buckling Eigenvalue (λ) | FRF Data | FRF Plot |\n")
        f.write("|-------------------------|---------------|----------------|-------------------------|----------|----------|\n")
        for res in results:
            S, w, r, eig, frf, plot = res['S'], res['w'], res['r'], res['eigenvalue'], res['frf_csv'], res['frf_plot']
            eig_str = f"{eig:.4e}" if eig else "N/A"
            frf_str = f"[CSV]({sweep_dir}/{frf})" if frf else "N/A"
            plot_str = f"[PNG]({sweep_dir}/{plot})" if plot else "N/A"
            f.write(f"| {S:.3f} | {w:.6f} | {r:.6f} | {eig_str} | {frf_str} | {plot_str} |\n")
        
    print(f"Sweep complete. Results written to {results_file}")

if __name__ == "__main__":
    main()
