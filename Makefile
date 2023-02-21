test: run draw
original: run_fulltest_original draw_original

run:
	python3 run_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testone/ --ext ctok --fine 300 --xst --rw
	
run_original:
	python3 run_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testzero/ --ext ctok --fine 300 --xst

draw:
	python3 draw_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testone/

run_fulltest_new:
	python3 run_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testone/ --ext ctok --fine 300 --booz --xst --rw

run_fulltest_original:
	python3 run_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testzero/ --ext ctok --fine 300 --booz --xst

draw_original:
	python3 draw_stellgap.py --dir /home/pedro/Documents/stellgap_pruebas/test/testzero/
