'''!
  @file test1.py
  @license     The MIT License (MIT)
  @author [Vishwanath R] (github: vishcomestrue)
  @version  v1.0.0
  @date  2023-07-19
  @url 
 '''
from bmx160lib import BMX160
import time

bmx = BMX160(1)

while not bmx.begin():
	time.sleep(2)

def main():
	while True:
		data = bmx.get_all_data()
		time.sleep(0.2)
		print("Magnetometer readings : x: {0:.2f} uT, y: {1:.2f} uT, z: {2:.2f} uT".format(data[0],data[1],data[2]))
		print("Gyroscope readings    : x: {0:.2f} g, y: {1:.2f} g, z: {2:.2f} g".format(data[3],data[4],data[5]))
		print("Acceleration readings : x: {0:.2f} m/s^2, y: {1:.2f} m/s^2, z: {2:.2f} m/s^2".format(data[6],data[7],data[8]))
		print(" ")

if __name__ == '__main__':
	print("Starting the program....")
	try:
		main()
	except KeyboardInterrupt:
		print("\nReceived a Keyboard Interrupt, stopping the program......")
		time.sleep(1.5)
		print("Program Stopped!")
