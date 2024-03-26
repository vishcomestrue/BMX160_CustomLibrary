'''!
  @file bmx160lib.py
  @license     The MIT License (MIT)
  @author [Vishwanath R] (email: rvishwanath03@outlook.com) (github: vishcomestrue)
  @version  v1.1.1
  @date  2023-07-19
  @url 
 '''

import smbus
import time

class BMX160:
	_chip_addr = 0x00
	_err_addr = 0x02
	_pmu_status_addr = 0x03
	_mag_data_addr = 0x04
	_gyr_data_addr = 0x0C 
	_acc_data_addr = 0x12
	_mag_conf_addr = 0x44
	_mag_if_0_addr = 0x4C
	_mag_if_1_addr = 0x4D
	_mag_if_2_addr = 0x4E
	_mag_if_3_addr = 0x4F
	_cmd_addr = 0x7E

	_soft_reset_value = 0xb6

	_gyro_125dps_mode = 0.0038110
	_gyro_250dps_mode = 0.0076220
	_gyro_500dps_mode = 0.0152439
	_gyro_1000dps_mode = 0.0304878
	_gyro_2000dps_mode = 0.0609756

	_accel_2g_mode = 0.000061035
	_accel_4g_mode = 0.000122070
	_accel_8g_mode = 0.000244141
	_accel_16g_mode = 0.000488281

	_magn_mode = 0.3

	gyroRange = _gyro_250dps_mode
	accelRange = _accel_2g_mode

	def __init__(self, bus):
		self.bus = smbus.SMBus(bus)
		self.interface_addr = 0x68
		time.sleep(0.2)

	def sensor_details(self):
		data = hex(self.bus.read_byte_data(self.interface_addr, self._chip_addr))
		print(f"Chip ID is: {data}")

	def scan(self):
		try:
			self.bus.read_byte(self.interface_addr)
			print(f"I2C scan successful")
			return True
		except:
			print("I2C scan failed")
			return False

	def begin(self):
		if not self.scan():
			return False
		else:
			self.sensor_details()
			self.soft_reset()
			self.write_into_bmx(self._cmd_addr, 0x11)
			time.sleep(0.1)
			self.write_into_bmx(self._cmd_addr, 0x15)
			time.sleep(0.1)
			self.write_into_bmx(self._cmd_addr, 0x19)
			time.sleep(0.1)
			self.conf_magn()
			return True

	def low_power_mode(self):
		self.soft_reset()
		time.sleep(0.1)
		self.conf_magn()
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x12)
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x17)
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x1B)
		time.sleep(0.1)

	def wake_up_sensor(self):
		self.soft_reset()
		time.sleep(0.1)
		self.conf_magn()
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x11)
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x15)
		time.sleep(0.1)
		self.write_into_bmx(self._cmd_addr, 0x19)
		time.sleep(0.1)

	def soft_reset(self):
		value = self._soft_reset_value
		self.write_into_bmx(self._cmd_addr, value)
		time.sleep(0.2)
		return True

	def read_from_bmx(self, address):
		return self.bus.read_i2c_block_data(self.interface_addr, address)

	def write_into_bmx(self, address, value):
		self.bus.write_byte_data(self.interface_addr, address, value)

	def conf_magn(self):
		self.write_into_bmx(self._mag_if_0_addr, 0x80)
		time.sleep(0.05)
		self.write_into_bmx(self._mag_if_3_addr, 0x01)
		self.write_into_bmx(self._mag_if_2_addr, 0x4B)
		self.write_into_bmx(self._mag_if_3_addr, 0x04)
		self.write_into_bmx(self._mag_if_2_addr, 0x51)
		self.write_into_bmx(self._mag_if_3_addr, 0x0E)
		self.write_into_bmx(self._mag_if_2_addr, 0x52)

		self.write_into_bmx(self._mag_if_3_addr, 0x02)
		self.write_into_bmx(self._mag_if_2_addr, 0x4C)
		self.write_into_bmx(self._mag_if_1_addr, 0x42)
		self.write_into_bmx(self._mag_conf_addr, 0x08)
		self.write_into_bmx(self._mag_if_0_addr, 0x03)
		time.sleep(0.05)

	def set_gyro_range(self, bit):
		if bit == 0:
			self.gyroRange = self._gyro_125dps_mode
		elif bit == 1:
			self.gyroRange = self._gyro_250dps_mode
		elif bit == 2:
			self.gyroRange = self._gyro_500dps_mode
		elif bit == 3:
			self.gyroRange = self._gyro_1000dps_mode
		elif bit == 4:
			self.gyroRange = self._gyro_2000dps_mode
		else:
			self.gyroRange = self._gyro_250dps_mode

	def set_accel_range(self, bit):
		if bit == 0:
			self.accelRange = self._accel_2g_mode
		elif bit == 1:
			self.gyroRange = self._accel_4g_mode
		elif bit == 2:
			self.gyroRange = self._accel_8g_mode
		elif bit == 3:
			self.gyroRange = self._accel_16g_mode
		else:
			self.gyroRange = self._accel_2g_mode

	def get_all_data(self, axis='none'):
		data = self.read_from_bmx(self._mag_data_addr)

		if(data[1] & 0x80):
			magnx = -0x10000 + ((data[1] << 8) | (data[0]))
		else:
			magnx = (data[1] << 8) | (data[0])

		if(data[3] & 0x80):
			magny = -0x10000 + ((data[3] << 8) | (data[2]))
		else:
			magny = (data[3] << 8) | (data[2])

		if(data[5] & 0x80):
			magnz = -0x10000 + ((data[5] << 8) | (data[4]))
		else:
			magnz = (data[5] << 8) | (data[4])

		if(data[9] & 0x80):
			gyrox = -0x10000 + ((data[9] << 8) | (data[8]))
		else:
			gyrox = (data[9] << 8) | (data[8])

		if(data[11] & 0x80):
			gyroy = -0x10000 + ((data[11] << 8) | (data[10]))
		else:
			gyroy = (data[11] << 8) | (data[10])

		if(data[13] & 0x80):
			gyroz = -0x10000 + ((data[13] << 8) | (data[12]))
		else:
			gyroz = (data[13] << 8) | (data[12])

		if(data[15] & 0x80):
			accelx = -0x10000 + ((data[15] << 8) | (data[14]))
		else:
			accelx = (data[15] << 8) | (data[14])

		if(data[17] & 0x80):
			accely = -0x10000 + ((data[17] << 8) | (data[16]))
		else:
			accely = (data[17] << 8) | (data[16])

		if(data[19] & 0x80):
			accelz = -0x10000 + ((data[19] << 8) | (data[18]))
		else:
			accelz = (data[19] << 8) | (data[18])

		magnx *= self._magn_mode
		magny *= self._magn_mode
		magnz *= self._magn_mode

		gyrox *= self.gyroRange
		gyroy *= self.gyroRange
		gyroz *= self.gyroRange

		accelx *= self.accelRange * 9.8
		accely *= self.accelRange * 9.8
		accelz *= self.accelRange * 9.8

		sensor_datas = []

		if axis == 'x':
			sensor_datas.append(magnx)
			sensor_datas.append(gyrox)
			sensor_datas.append(accelx)

		elif axis == 'y':
			sensor_datas.append(magny)
			sensor_datas.append(gyroy)
			sensor_datas.append(accely)

		elif axis == 'z':
			sensor_datas.append(magnz)
			sensor_datas.append(gyroz)
			sensor_datas.append(accelz)

		else:
			sensor_datas.append(magnx)
			sensor_datas.append(magny)
			sensor_datas.append(magnz)

			sensor_datas.append(gyrox)
			sensor_datas.append(gyroy)
			sensor_datas.append(gyroz)

			sensor_datas.append(accelx)
			sensor_datas.append(accely)
			sensor_datas.append(accelz)

		return sensor_datas
