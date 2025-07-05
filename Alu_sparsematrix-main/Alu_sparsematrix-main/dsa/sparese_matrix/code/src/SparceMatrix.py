import os

def list_matrix_files(input_dir):
    """List all .txt files in input_dir and return the list."""
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    if not files:
        raise FileNotFoundError(f"No .txt files found in {input_dir}")
    print("Available matrix files:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    return files

def load_sparse_matrix(filename):
    """Read sparse matrix from a text file and return rows, cols, and dict."""
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            rows = int(lines[0].split('=')[1].strip())
            cols = int(lines[1].split('=')[1].strip())
            matrix = {}
            for line in lines[2:]:
                if not (line.startswith("(") and line.endswith(")")):
                    raise ValueError("Invalid tuple format")
                parts = line.strip('() \n').split(',')
                if len(parts) != 3:
                    raise ValueError("Invalid tuple format")
                try:
                    i = int(parts[0].strip())
                    j = int(parts[1].strip())
                    val = int(parts[2].strip())
                    matrix[(i, j)] = val
                except:
                    raise ValueError("Tuple contains non-integer values")
            return rows, cols, matrix
    except Exception as e:
        raise ValueError(f"Error reading '{filename}': {e}")

def add_sparse(A, B):
    result = A.copy()
    for key, val in B.items():
        result[key] = result.get(key, 0) + val
    return result

def sub_sparse(A, B):
    result = A.copy()
    for key, val in B.items():
        result[key] = result.get(key, 0) - val
    return result

def mul_sparse(rA, cA, A, rB, cB, B):
    if cA != rB:
        raise ValueError("Can't multiply: cols of A must equal rows of B")
    B_indexed = {}
    for (k, j), val in B.items():
        B_indexed.setdefault(k, []).append((j, val))
    result = {}
    for (i, k), valA in A.items():
        if k in B_indexed:
            for j, valB in B_indexed[k]:
                result[(i, j)] = result.get((i, j), 0) + valA * valB
    return rA, cB, result

def print_sparse(matrix):
    for (i, j), val in sorted(matrix.items()):
        print(f"({i},{j},{val})")

def save_sparse(matrix, rows, cols, filename):
    with open(filename, 'w') as f:
        f.write(f"rows={rows}\ncols={cols}\n")
        for (i, j), val in sorted(matrix.items()):
            f.write(f"({i},{j},{val})\n")
    print(f"\n Saved to {filename}")

def main():
    # Define input and output folders relative to this script location
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sample_inputs'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sample_outputs'))

    # Create output folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List files from input_dir
    files = list_matrix_files(base_dir)
    if len(files) < 2:
        raise ValueError("Need at least two .txt matrix files to proceed.")

    # User selects files
    i1 = int(input("\nChoose first matrix by number: ")) - 1
    i2 = int(input("Choose second matrix by number: ")) - 1
    file1 = os.path.join(base_dir, files[i1])
    file2 = os.path.join(base_dir, files[i2])

    # Load matrices
    r1, c1, M1 = load_sparse_matrix(file1)
    r2, c2, M2 = load_sparse_matrix(file2)

    # Choose operation
    print("\nChoose operation:\n1. Add\n2. Subtract\n3. Multiply")
    op = input("Enter option (1/2/3): ").strip()

    if op == '1':
        if r1 != r2 or c1 != c2:
            raise ValueError("Matrix size mismatch for addition.")
        result = add_sparse(M1, M2)
        result_rows, result_cols = r1, c1
        print("\n Result (Addition):")
        print_sparse(result)

    elif op == '2':
        if r1 != r2 or c1 != c2:
            raise ValueError("Matrix size mismatch for subtraction.")
        result = sub_sparse(M1, M2)
        result_rows, result_cols = r1, c1
        print("\n Result (Subtraction):")
        print_sparse(result)

    elif op == '3':
        result_rows, result_cols, result = mul_sparse(r1, c1, M1, r2, c2, M2)
        print("\n Result (Multiplication):")
        print_sparse(result)

    else:
        raise ValueError("Invalid option selected.")

    # Save results?
    save = input("\nSave result to file? (yes/no): ").strip().lower()
    if save == "yes":
        name = input("Enter filename (e.g., result.txt): ").strip()
        out_path = os.path.join(output_dir, name)
        save_sparse(result, result_rows, result_cols, out_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n {e}")

