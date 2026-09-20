import subprocess


def ligand(dir, name, smiles, ph):
    name_smiles = f"{name}.smiles"
    name_scrubbed = f"{name}_scrubbed.sdf"
    name_pdbqt = f"{name}.pdbqt"

    file_smiles = dir / name_smiles
    file_smiles.write_text(smiles)

    subprocess.run([
        "scrub.py",
        smiles,
        "-o", name_scrubbed,
        "--ph", str(ph),
        "--skip_tautomer",
    ], cwd=dir)

    subprocess.run([
        "mk_prepare_ligand.py",
        "-i", name_scrubbed,
        "-o", name_pdbqt,
    ], cwd=dir)

    return name_pdbqt


def receptor(dir, name, id, box):
    pass
    return


def docking(dir, ligand, receptor, exhaustiveness):
    pass
    return


def score(dir, docking):
    return 0.0
