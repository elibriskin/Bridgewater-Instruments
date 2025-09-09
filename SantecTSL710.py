import csv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import pyvisa as visa

class SantecTSL710:
    '''
    This is a Python wrapper to communicate with the Santect TSL 710 Tunable laser via GPIB
    connection.
    '''
    def __init__(self, address):
        self.address = address
        self.stcmain = None
        self.data = []  # Array to store data
        self.states = {
            "ON": 1,
            "OFF": 0
        }
        self.power_units = {
            "dBm": 0,
            "mW": 1
        }
        self.spectral_units = {
            "nm": 0,
            "THz": 1
        }
        self.sweep_modes = {
            "step": 0,
            "continous": 1
        }

    def initialize(self):
        rm = visa.ResourceManager()
        self.stcmain = rm.open_resource(self.address, timeout=20000)

    def set_laser(self, laser_state):
        '''
        Sets the laser on or off.
        '''
        self.stcmain.write(f"SOUR:PW:STATE {self.states[laser_state]}")

    def set_attenuation(self, attenuation):
        '''
        Sets the laser attenuation.
        '''
        self.stcmain.write(f"SOUR:POW:ATT {attenuation}")

    def get_attenuation(self):
        '''
        Gets current laser attenuation/
        '''
        self.stcmain.query("SOUR:POW:ATT?")


    def set_auto_attenuation(self, attenuation_option):
        '''
        Enables automatic attenuation for power control
        '''
        attenuation_options = {
            "manual": 0,
            "automatic": 1
        }
        self.stcmain.write(f"POW:ATT:AUT {attenuation_options[attenuation_option]}")

    def get_power_unit(self):
            '''
            Set the power unit of the laser.
            '''
            power_unit = self.stcmain.query(f"POW:UNIT?")
            return power_unit

    def set_power_unit(self, power_unit):
        '''
        Set the power unit of the laser.
        '''
        self.stcmain.write(f"POW:UNIT: {self.power_units[power_unit]}")
    
    def get_set_power(self):
        '''
        Gets the power set level of the laser.
        '''
        power = self.stcmain.query(f"POW?")
        return float(power)
    
    def get_power(self):
        '''
        Gets the actual/monitored power level of the laser.
        '''
        power = self.stcmain.query("POW:ACT?")
        return float(power)

    def set_power(self, power_unit, power):
        '''
        Sets the power level of the laser.
        '''
        self.set_power_unit(power_unit)
        self.stcmain.write(f"POW: {power}")

    def set_spectral_unit(self, spectral_unit):
        '''
        Sets the unit of the laser to wavelength or THz.
        '''
        self.stcmain.write(f"WAV:UNIT: {self.spectral_units[spectral_unit]}")

    def get_wavelength(self, unit, wavelength):
        '''
        Sets the wavelength of the laser.
        '''
        wavelength = self.stcmain.query(f"WAV?")
        return float(wavelength)

    def set_wavelength(self, wavelength):
        '''
        Sets the wavelength of the laser.
        '''
        self.set_spectral_unit("nm")
        self.stcmain.write(f"WAV {wavelength}")

    def get_frequency(self):
        '''
        Sets the frequency in terahertz.
        '''
        frequency = self.stcmain.query("FREQ?")
        return frequency

    def set_frequency(self, frequency):
        '''
        Sets the frequency in terahertz.
        '''
        self.set_spectral_unit("THz")
        self.stcmain.write(f"FREQ {frequency}")

    def get_sweep_cycles(self):
        '''
        Get the number of sweep cycles for a wavelength sweep.
        '''
        sweep_cycles = self.stcmain.query("WAV:SWE:CYCL?")
        return float(sweep_cycles)

    def set_sweep_cycles(self, sweep_cycles):
        '''
        Set the number of sweep cycles for a wavelength sweep.
        '''
        self.stcmain.write(f"WAV:SWE:CYCL {sweep_cycles}")

    def set_sweep_mode(self, sweep_mode, sweep_direction):
        '''
        Sets the sweep mode of the laser.
        '''
        sweep_mode_selection = self.sweep_modes[sweep_mode]

        if sweep_direction == "two-way":
            sweep_mode_selection += 2

        self.stcmain.write(f"WAV:SWE:MOD {sweep_mode_selection}")

    def set_sweep_speed(self, sweep_speed):
        '''
        Sets the sweep speed of the laser.
        '''
        self.stcmain.write(f"WAV:SWE:SPE {sweep_speed}")
