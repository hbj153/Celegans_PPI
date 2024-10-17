import argparse
import os
import numpy as np
import pandas as pd
from denoiser import randomize_matrix, calculate_uncertainty

def main():
    parser = argparse.ArgumentParser(description='Denoise a NxN matrix')
    parser.add_argument('--input_file', required=True, help='Name of the input file (must be in the input folder)')
    args = parser.parse_args()

    # Input and output folder paths
    input_folder = 'input/'
    output_folder = 'output/'

    # Load input matrix from input file in the input folder
    input_file_path = os.path.join(input_folder, args.input_file)
    if not os.path.exists(input_file_path):
        print(f"Error: Input file {input_file_path} does not exist.")
        return

    M_raw = pd.read_csv(input_file_path, header=None).values

    # Preprocess the matrix
    magic = 0
    ml = np.min(M_raw)
    mu = np.max(M_raw)
    Mn = M_raw / (mu + magic)

    # Randomize the matrix
    P, a_in_his, a_out_his, probs_his = randomize_matrix(Mn, iters=100, saveHistory=True, probHistory=True)
    a_in = a_in_his[-1]
    a_out = a_out_his[-1]
    alphas = a_out
    betas = a_in
    a = -np.log(alphas)
    b = -np.log(betas)
    Qij = 1 / Mn - 1

    # Estimate std of alphas and betas
    betas_input = np.array([Qij[i, :] / alphas[i] for i in range(Qij.shape[0])])
    alphas_input = np.array([Qij[:, j] / betas[j] for j in range(Qij.shape[1])])
    betas_std = np.std(betas_input, axis=0)
    alphas_std = np.std(alphas_input, axis=0)
    b_std = np.abs((1 / betas) * betas_std)
    a_std = np.abs((1 / alphas) * alphas_std)

    # Calculate uncertainty of P
    sigma_P = calculate_uncertainty(a, b, a_std, b_std)

    # Calculate z-score
    Z = (Mn - P) / sigma_P
    Z[np.isnan(Z)] = 0
    Z_sym = (Z + Z.T) / np.sqrt(2)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save the output matrices to CSV files in the output folder
    base_file_name = os.path.splitext(args.input_file)[0]

    # Save the output matrices to CSV files in the output folder
    output_file_z = os.path.join(output_folder, f'{base_file_name}_Z.csv')
    output_file_z_sym = os.path.join(output_folder, f'{base_file_name}_Z_sym.csv')
    pd.DataFrame(Z).to_csv(output_file_z, header=None, index=False)
    pd.DataFrame(Z_sym).to_csv(output_file_z_sym, header=None, index=False)
    
    print(f"Denoising complete. Results saved to {output_folder}.")

if __name__ == '__main__':
    main()
