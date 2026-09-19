make scrub:
	scrub.py "$$(cat data/Imatinib.smiles)" -o data/Imatinib_scrubbed.sdf --ph 6 --skip_tautomer
