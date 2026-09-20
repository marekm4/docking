```python
from pathlib import Path

from docking import ligand, receptor, docking, affinity

work_dir = Path("data")
work_dir.mkdir(parents=True, exist_ok=True)

Imatinib = ligand(work_dir, "Imatinib", "CC1=C(NC2=NC=CC(C3=CN=CC=C3)=N2)C=C(NC(C4=CC=C(CN5CCN(C)CC5)C=C4)=O)C=C1", 6)
C_ABL_KINASE = receptor(work_dir, "C_ABL_KINASE", "1IEP", 20)
C_ABL_KINASE_Imatinib = docking(work_dir, C_ABL_KINASE, Imatinib, 8)
print(affinity(work_dir, C_ABL_KINASE_Imatinib))
```
