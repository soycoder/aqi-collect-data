# Devloping use python3

## File
```
│-- src
	│-- README.md   
	│-- bme280
		│-- adafruit_bme280_test.py   
			*/using Library/* : adafruit_bme280
	
	│--light
	  	│-- bh1750.py                  
		  	*/using Library/ : smbus mutibus(SDA,SCL)
	
	│-- test-multibus
	   	│-- multiple_bmp280.py 
		   	*/using Library/* : smbus mutibus(SDA,SCL)
	
	│-- pms3003
		│-- 
    
```

.
+-- src
	+-- _
	|   +-- 
	+-- _light
	|   +-- 
	+-- _layouts
	|   +-- default.html
	+-- _
	|   +-- 
	+-- readme.md

## Data
1. Humity, Temperature, Pressure
	- BME280(I2C)
2. Light intensity
	- bh1750(I2C)
3. PM1.0 / 2.5 / 10
	- pms3003