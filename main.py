from pathlib import Path

from docking import ligand, receptor, docking, affinity

work_dir = Path("data")
work_dir.mkdir(parents=True, exist_ok=True)

Navitoclax = ligand(work_dir, "CC1(CCC(=C(C1)CN2CCN(CC2)C3=CC=C(C=C3)C(=O)NS(=O)(=O)C4=CC(=C(C=C4)N[C@H](CCN5CCOCC5)CSC6=CC=CC=C6)S(=O)(=O)C(F)(F)F)C7=CC=C(C=C7)Cl)C", 7.4)
Bcl_xL = receptor(work_dir, "2YXJ", (-9, -16, 11), (25, 31, 18))
Bcl_xL_Navitoclax = docking(work_dir, Bcl_xL, Navitoclax, 32)
print(affinity(work_dir, Bcl_xL_Navitoclax))
