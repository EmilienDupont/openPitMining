all:
	./SimpleServer.py

test:
	./openPitMining.py

clean:
	-rm gurobi.log *.pyc *.lp
