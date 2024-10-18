# Maximum-entropy based background correction

## Cite our study

This code is associated with the manuscript titled **"Nematode Extracellular Protein Interactome Expands Connections between Signaling Pathways"**, authored by Wioletta I. Nawrocka, Shouqiang Cheng, Bingjie Hao, Matthew Rosen, Elena Cortés, Elana Baltrusaitis, Zainab Aziz, István A. Kovács, and Engin Özkan.

The tool provided here plays a role in analyzing the raw protein-protein interaction (PPI) data, contributing to the findings presented in the manuscript.

For more information, you can access the manuscript via the following DOI link: [https://doi.org/10.1101/2024.07.08.602367](https://doi.org/10.1101/2024.07.08.602367).

This project provides a command-line tool to correct the background for NxN matrices using a maximum entropy randomization method. The tool takes an input matrix in `.csv` format, processes it, and outputs the corrected matrix and its corresponding Z-scores to two CSV files.

## Features

- Randomizes a directed weighted network (NxN matrix) using maximum entropy and consider it as background.
- Subtract the background matrix from the original matrix and calculate the z-scores to quantify the significance of PPI signals.
- Outputs results in `.csv` format for further analysis.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Input Format](#input-format)
- [Output](#output)
- [Example](#example)

---

## Installation

1. Clone the repository to your local machine

2. Install the required dependencies:

   ```bash
   pip install numpy pandas
   ```

3. Place your input matrix in the `input` folder. The input file should be a `.csv` file without headers.

---

## Usage

To run the matrix denoising tool, use the following command:

```bash
python cli.py --input_file input.csv
```

### Arguments:

- `--input_file`: The name of the input file located in the `input` folder. The input file should be in `.csv` format.

### Input/Output Structure:

- **Input folder**: The input file should be placed in the `input` folder.
- **Output folder**: The resulting output files will be saved in the `output` folder.

### Example Usage:

```bash
python cli.py --input_file input.csv
```

This command will:

1. Read `input.csv` from the `input` folder.
2. Perform the denoising process and Z-score calculation.
3. Save the outputs as `input_Z.csv` and `input_Z_sym.csv` in the `output` folder.

---

## Input Format

The input matrix must be a `.csv` file located in the `input` folder. The file should not contain headers or row/column indices, just a plain NxN matrix of numbers.

### Example Input File (`input/input.csv`):

```csv
0.1, 0.2, 0.3
0.4, 0.5, 0.6
0.7, 0.8, 0.9
```

This represents a 3x3 matrix.

---

## Output

The results will be saved in the `output` folder with two files generated:

1. **`input_Z.csv`**: This file contains the Z-score matrix calculated from the input matrix.
2. **`input_Z_sym.csv`**: This file contains the symmetrized Z-score matrix.

### Example Output Files:

- **`output/input_Z.csv`**:

  ```csv
  -0.5, 1.2, -0.3
   0.6, -1.0, 0.4
  -0.2, 0.9, -1.5
  ```

- **`output/input_Z_sym.csv`**:

  ```csv
  -0.35, 0.9, -0.25
   0.9, -0.75, 0.5
  -0.25, 0.5, -1.3
  ```

These CSV files are directly usable for further analysis.

***

## Example

1. **Prepare the Input:**
   Place your matrix file in the `input` folder with the name `input.csv`:

   ```csv
   0.1, 0.2, 0.3
   0.4, 0.5, 0.6
   0.7, 0.8, 0.9
   ```

2. **Run the Code:**
   Use the command line to run the denoising tool:

   ```bash
   python cli.py --input_file input.csv
   ```

3. **Check the Output:**
   After the script runs, check the `output` folder for the results. The folder will contain:

   - `input_Z.csv`
   - `input_Z_sym.csv`
