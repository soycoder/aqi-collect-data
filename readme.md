# ⛅ AQI collect data
	Place : @Thammasat University Lampang campus.
		1. Inovation Building.
		2. Football Field.

 ## Start
	sudo apt-get update
	sudo apt-get upgrade

	sudo pip3 install --upgrade setuptools

If above doesn't work try

	sudo apt-get install python3-pip
	
 ## 🌎 Visit
	web : in-process []

 ## ▶ Run Command
	cd /home/pi/Desktop/aqi-collect-data/
	python3 aqi-pm-csv.py
	 -or-
	python3 aqi-csv.py
	 -or-
	python aqi-pm3003-csv.py 

 ## 🧱 Create as a Service

- Link Ref :[forums](https://www.raspberrypi.org/forums/viewtopic.php?t=197513)

----
	sudo nano aqi.service
	sudo nano aqi-pm.service
	sudo nano aqi-pm3003.service

1. First, I create a file (.service).

----

	cd /lib/systemd/system/
	sudo nano aqi.service

2. write folloed with below command.

----
	[Unit]
	Description=Hello World
	After=multi-user.target

	[Service]
	Type=simple
	ExecStart=/usr/bin/python /home/pi/hello_world.py
	Restart=on-failure

	[Install]
	WantedBy=multi-user.target


3. How to start a service

----
	sudo chmod 644 /lib/systemd/system/hello.service
	chmod +x /home/pi/hello_world.py

	sudo systemctl daemon-reload
	sudo systemctl enable hello.service
	sudo systemctl start hello.service

4. Later, I can this

----
	# Check status
	sudo systemctl status hello.service

	# Start service
	sudo systemctl start hello.service

	# Stop service
	sudo systemctl stop hello.service

	# Check service's log
	sudo journalctl -f -u hello.service