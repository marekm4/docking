```python
from pathlib import Path

from docking import ligand, receptor, docking, affinity

work_dir = Path("data")

ABT_737 = ligand(work_dir, "ABT-737",
                 "CN(C)CC[C@H](CSc1ccccc1)Nc2ccc(cc2[N+](=O)[O-])S(=O)(=O)NC(=O)c3ccc(cc3)N4CCN(CC4)Cc5ccccc5c6ccc(cc6)Cl",
                 7.4)
Navitoclax = ligand(work_dir, "Navitoclax",
                    "CC1(CCC(=C(C1)CN2CCN(CC2)C3=CC=C(C=C3)C(=O)NS(=O)(=O)C4=CC(=C(C=C4)N[C@H](CCN5CCOCC5)CSC6=CC=CC=C6)S(=O)(=O)C(F)(F)F)C7=CC=C(C=C7)Cl)C",
                    7.4)
Bcl_xL = receptor(work_dir, "Bcl-xL", "2YXJ", 30)

Bcl_xL_ABT_737 = docking(work_dir, Bcl_xL, ABT_737, 8)
Bcl_xL_Navitoclax = docking(work_dir, Bcl_xL, Navitoclax, 8)

print(affinity(work_dir, Bcl_xL_ABT_737))
print(affinity(work_dir, Bcl_xL_Navitoclax))
```
