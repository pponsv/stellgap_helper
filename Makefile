test: run draw

run:
	python3 run_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testone/ --ext ctok --fine 300 --xst --rw
	
draw:
	python3 draw_stellgap.py