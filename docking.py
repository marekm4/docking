import hashlib
import os
import subprocess
from urllib.request import urlretrieve

from prody import parsePDB, writePDB


def ligand(dir, smiles, ph):
    name = hashlib.md5(f"{ph}_{smiles}".encode()).hexdigest()

    name_smiles = f"{name}.smiles"
    file_smiles = dir / name_smiles
    if not file_smiles.exists():
        file_smiles.write_text(smiles)

    name_scrubbed = f"{name}_scrubbed.sdf"
    if not (dir / name_scrubbed).exists():
        subprocess.run([
            "scrub.py",
            smiles,
            "-o", name_scrubbed,
            "--ph", str(ph),
            "--skip_tautomer",
        ], cwd=dir)

    name_pdbqt = f"{name}.pdbqt"
    if not (dir / name_pdbqt).exists():
        subprocess.run([
            "mk_prepare_ligand.py",
            "-i", name_scrubbed,
            "-o", name_pdbqt,
        ], cwd=dir)

    return name_pdbqt


def receptor(dir, id, center, size):
    name = hashlib.md5(f"{id}_{center[0]}_{center[1]}_{center[2]}_{size[0]}_{size[1]}_{size[2]}".encode()).hexdigest()

    name_pdb = f"{name}.pdb"
    file_pdb = dir / name_pdb
    if not file_pdb.exists():
        urlretrieve(f"https://files.rcsb.org/download/{id}.pdb", file_pdb)

    name_atoms = f"{name}_receptor_atoms.pdb"
    file_atoms = dir / name_atoms
    if not file_atoms.exists():
        atoms_from_pdb = parsePDB(str(file_pdb))
        receptor_selection = "chain A and not water and not hetero"
        receptor_atoms = atoms_from_pdb.select(receptor_selection)
        writePDB(str(file_atoms), receptor_atoms)

    name_receptor = f"{name}_receptor.pdb"
    file_receptor = dir / name_receptor
    if not file_receptor.exists():
        with open(str(file_receptor), "w") as out:
            subprocess.run([
                "grep", "CRYST1", name_pdb
            ], stdout=out, cwd=dir)
        with open(str(file_receptor), "a") as out:
            subprocess.run([
                "cat", name_atoms
            ], stdout=out, cwd=dir)

    name_receptor_FH = f"{name}_receptorFH.pdb"
    file_receptor_FH = dir / name_receptor_FH
    if not file_receptor_FH.exists():
        env = os.environ.copy()
        env["MMTBX_CCP4_MONOMER_LIB"] = "../geostd"
        subprocess.run([
            "mmtbx.reduce2", name_receptor,
            "approach=add", "add_flip_movers=True"
        ], env=env, cwd=dir)

    name_receptor_pdbqt = f"{name}_receptor.pdbqt"
    file_receptor_pdbqt = dir / name_receptor_pdbqt
    if not file_receptor_pdbqt.exists():
        subprocess.run([
            "mk_prepare_receptor.py",
            "-i", name_receptor_FH,
            "-o", f"{name}_receptor",
            "-p", "-v",
            "--default_altloc", "A",
            "--box_center", str(center[0]), str(center[1]), str(center[2]),
            "--box_size", str(size[0]), str(size[1]), str(size[2])
        ], cwd=dir)

    return name_receptor_pdbqt


def docking(dir, receptor, ligand, exhaustiveness):
    out_name = hashlib.md5(f"{exhaustiveness}_{receptor.replace("_receptor.pdbqt", "")}_{ligand.replace(".pdbqt", "")}".encode()).hexdigest() + ".pdbqt"
    if not (dir / out_name).exists():
        subprocess.run([
            "../vina",
            "--receptor", receptor,
            "--ligand", ligand,
            "--config", receptor.replace(".pdbqt", ".box.txt"),
            "--exhaustiveness", str(exhaustiveness),
            "--out", out_name
        ], cwd=dir)

    export_name = out_name.replace(".pdbqt", ".sdf")
    if not (dir / export_name).exists():
        subprocess.run([
            "mk_export.py", out_name,
            "-s", export_name
        ], cwd=dir)

    return out_name


def affinity(dir, docking):
    for line in (dir / docking).read_text().splitlines():
        if "RESULT" in line:
            score = line.split()[3]
            break
    return score


def view(dir, molecule):
    if molecule.endswith("_receptor.pdbqt"):
        return str(dir / molecule.replace("_receptor.pdbqt", "_receptor.pdb"))
    path = dir / molecule.replace(".pdbqt", "_scrubbed.sdf")
    if path.exists():
        return str(path)
    return str(dir / molecule.replace(".pdbqt", ".sdf"))
