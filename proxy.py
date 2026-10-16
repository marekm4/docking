from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from docking import ligand, receptor, docking, affinity


work_dir = Path("data")
input_file = work_dir / "chembl_22_clean_1576904_sorted_std_final.smi"
output_file = work_dir / "proxy.csv"

Bcl_xL = receptor(work_dir, "2YXJ", (-9, -16, 11), (25, 31, 18))


def process_molecule(smiles):
    l = ligand(work_dir, smiles, 7.4)
    d = docking(work_dir, Bcl_xL, l, 1)
    a = affinity(work_dir, d)

    return smiles, a


def main():
    with open(input_file, "r", encoding="utf-8") as file:
        smiles_list = [
            line.strip().split("\t")[0]
            for line in file
        ]

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("smiles,affinity\n")

        with ProcessPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(process_molecule, smiles)
                for smiles in smiles_list
            ]

            for future in as_completed(futures):
                try:
                    smiles, a = future.result()
                    outfile.write(f"{smiles},{a}\n")
                    outfile.flush()

                except Exception as e:
                    print(f"Error: {e}")


if __name__ == "__main__":
    main()
