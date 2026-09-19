scrub:
	scrub.py "$$(cat data/Imatinib.smiles)" -o data/Imatinib_scrubbed.sdf --ph 6 --skip_tautomer

ligand:
	mk_prepare_ligand.py -i data/Imatinib_scrubbed.sdf -o data/Imatinib.pdbqt

atoms:
	python atoms.py data/1IEP.pdb data/1IEP_receptor_atoms.pdb

cryst:
	grep CRYST1 data/1IEP.pdb > data/1IEP_receptor.pdb
	cat data/1IEP_receptor_atoms.pdb >> data/1IEP_receptor.pdb

reduce:
	MMTBX_CCP4_MONOMER_LIB="geostd" mmtbx.reduce2 data/1IEP_receptor.pdb approach=add add_flip_movers=True
	mv 1IEP* data
