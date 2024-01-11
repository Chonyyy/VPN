.PHONY: run
run:
	sudo python3 vpn_gui.py

.PHONY: cliente
cliente:
	python3 cliente_tk.py 

.PHONY: servidor
servidor:
	python3 servidor_gui.py 