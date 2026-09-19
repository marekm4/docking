make scrub:
	scrub.py "$$(cat data/Imatinib.smiles)" -o data/Imatinib_scrubbed.sdf --ph 6 --skip_tautomer

make ligand:
	mk_prepare_ligand.py -i data/Imatinib_scrubbed.sdf -o data/Imatinib.pdbqt
