import os
import re
import subprocess
import numpy as np

# Parameters
L_link = 0.005  # Nominal link length in meters (5mm)
slenderness_ratios = np.linspace(0.05, 0.2, 7)  # from 1/20 to 1/5
input_file_base = 'Buckling/Job-1.inp'
results_file = 'Slenderness_Sweep_Results.md'

def run_abaqus_job(job_name, input_file):
    print(f"Running Abaqus job: {job_name}")
    try:
        # Run Abaqus analysis
        # Using interactive to wait for completion
        # On Windows, sometimes the .bat is needed or just abaqus
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
                    # Look for the first mode (usually 3 lines down)
                    for j in range(i+1, min(i+10, len(lines))):
                        # Match numbers like 1.234E-02 or 5.678
                        match = re.search(r'\s+1\s+([\d.E+-]+)', lines[j])
                        if match:
                            eigenvalue = float(match.group(1))
                            return eigenvalue
    except Exception as e:
        print(f"Error parsing dat file: {e}")
    return eigenvalue

def main():
    if not os.path.exists(input_file_base):
        print(f"Base input file {input_file_base} not found.")
        return

    with open(input_file_base, 'r') as f:
        base_content = f.read()

    results = []
    
    # Create a directory for sweep files to avoid cluttering
    sweep_dir = 'Sweep_Files'
    if not os.path.exists(sweep_dir):
        os.makedirs(sweep_dir)

    # Base path for Abaqus (current working dir)
    cwd = os.getcwd()

    for i, S in enumerate(slenderness_ratios):
        w = S * L_link
        r = w / 2.0
        
        job_name = f"Job_S_{i}"
        temp_input_name = f"{job_name}.inp"
        temp_input_path = os.path.join(sweep_dir, temp_input_name)
        
        # Replace the radius in the input file
        pattern = r"(\*Beam Section,.*?section=CIRC\s*\r?\n)([\d.e+-]+)"
        new_content = re.sub(pattern, r"\g<1>" + f"{r:.6f}", base_content)
        
        with open(temp_input_path, 'w') as f:
            f.write(new_content)
        
        # Change directory to run the job
        original_cwd = os.getcwd()
        os.chdir(sweep_dir)
        
        success = run_abaqus_job(job_name, temp_input_name)
        
        if success:
            dat_file = f"{job_name}.dat"
            eigenvalue = parse_eigenvalue(dat_file)
            if eigenvalue:
                results.append((S, w, r, eigenvalue))
                print(f"S={S:.3f}, w={w:.6f}, r={r:.6f} -> Eigenvalue={eigenvalue}")
            else:
                print(f"Failed to parse eigenvalue for S={S:.3f}")
        else:
            print(f"Failed to run job for S={S:.3f}")
        
        os.chdir(original_cwd)

    # Write results to Markdown
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("# Slenderness Ratio Parameter Sweep Results\n\n")
        f.write("| Slenderness Ratio (w/L) | Width (w) [m] | Radius (r) [m] | Eigenvalue (λ) | Critical Load [N] |\n")
        f.write("|-------------------------|---------------|----------------|----------------|-------------------|\n")
        for S, w, r, eig in results:
            # Assuming base load is 16 * 3200 = 51200 N
            crit_load = eig * 51200
            f.write(f"| {S:.3f} (1/{1/S:.1f}) | {w:.6f} | {r:.6f} | {eig:.4f} | {crit_load:.1f} |\n")
        
        f.write("\n\n*Applied load per node: 3200 N, Number of nodes: 16, Total load: 51200 N*\n")

    print(f"Sweep complete. Results written to {results_file}")

if __name__ == "__main__":
    main()
