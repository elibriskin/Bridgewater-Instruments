import csv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import pyvisa as visa

class OSA:
    '''
    This is a Python wrapper to communicate with the OSA using GPIB connection. You can use to run parameterized wavelength sweeps
    as well as adjust core options including wavelengths, span, resolution, and speed.
    '''
    def __init__(self, address):
        self.address = address
        self.osamain = None
        self.data = []  # Array to store data
        self.sweep_modes = {
            "SINGLE": 1,
            "REPEAT": 2,
            "AUTO": 3
        }
        self.sensitivies = ["NHLD", "NAUT", "MID", "HIGH1", "HIGH2", "HIGH3", "NORMAL"]
        self.sweep_speeds = ["1x", "2x"]

    def initialize(self):
        rm = visa.ResourceManager()
        self.osamain = rm.open_resource(self.address, timeout=20000)

    def set_start_wavelength(self, wavelength_start):
        '''
        This method sets the starting wavelength of the OSA.
        '''
        self.osamain.write(f":sens:wav:start {wavelength_start}nm")

    def set_stop_wavelength(self, wavelength_stop):
        '''
        This method sets the stop wavelength of the OSA.
        '''
        self.osamain.write(f":sens:wav:stop {wavelength_stop}nm")

    def display_wavelength_range(self, wavelength_start, wavelength_stop):
        '''
        This method sets the wavelength range on the x axis in the window.
        '''
        self.osamain.write(f":DISPLAY:TRACE:X:START {wavelength_start}NM")
        self.osamain.write(f":DISPLAY:TRACE:X:STOP {wavelength_stop}NM")


    def set_wavelength_range(self, wavelength_start, wavelength_stop):
        '''
        This method sets the wavelength range of the OSA.
        '''
        self.osamain.write(f":sens:wav:start {wavelength_start}nm")

        self.osamain.write(f":sens:wav:stop {wavelength_stop}nm")

    def set_wavelength_span(self, span):
        '''
        This method sets the span of the wavelength range.
        '''
        self.osamain.write(f":sens:wav:span {span}nm")

    def set_center_wavelength(self, wavelength):
        '''
        This method sets the center wavelength.
        '''
        self.osamain.write(f":SENSe:WAVelength:CENTer {wavelength}nm")

    def set_center_frequency(self, frequency):
        '''
        This method sets the center wavelength.
        '''
        self.osamain.write(f":SENSe:WAVelength:CENTer {frequency}Hz")

    def set_sweep_mode(self, sweep_mode):
        '''
        This method sets the mode for wavelength sweep. Choices
        are 'AUTO', 'REPEAT', and 'SINGLE.'
        '''
        if sweep_mode in self.sweep_modes.keys():
            self.osamain.write(f":init:smode {self.sweep_modes[sweep_mode]}")
        else:
            raise Exception(f"Invalid sweep mode! Sweep modes are {self.sweep_modes.keys()}")
        
    def set_sweep_speed(self, sweep_speed):
        '''
        This method sets the speed for wavelength sweep. Choices
        are '1X', '2X'.
        '''
        if sweep_speed in self.sweep_speeds:
            self.osamain.write(f":SENSe:SWEep:SPEed {sweep_speed}")
        else:
            raise Exception(f"Invalid sweep mode! Sweep speeds are {self.sweep_speeds}")

    def set_sweep_step(self, sweep_step):
        '''
        Sets the sweep step of the wavelength sweep in nanometers.
        '''
        self.osamain.write(f":SENSE:SWEEP:STEP {sweep_step}NM")   
    
    def set_sweep_auto_points(self, auto_points):
        '''
        Enables automatic determination of sample size for wavelength step.
        '''

        self.osamain.write(f":SENSE:SWEEP:POINTS:AUTO {auto_points}")

    def set_sweep_points(self, points):
        '''
        Sets sweep sample size for a wavelength sweep.
        '''

        self.osamain.write(f":SENSE:SWEEP:POINTS:AUTO {points}")
    
    def set_resolution(self, resolution):
        '''
        This method sets the resolution of the OSA in nanometers.
        '''
        self.osamain.write(f":sens:band:resolution {resolution}nm")

    def window_center_wavelength(self, wavelength):
        '''
        Sets the wavelength of the x axis on the display scale in nm.
        '''
        self.osamain.write(f":DISPLAY:TRACE:X:CENTER {wavelength}NM")

    def set_window_span(self, span):
        '''
        Sets the wavelength span on the display window in nanometers.
        '''
        self.osamain.write(f":DISPLAY:TRACE:X:SPAN {span}NM")

    def set_window_start(self, window_start):
        '''
        Sets the starting wavelength on the display in nanometers.
        '''
        self.osamain.write(f':DISPLAY:TRACE:X:START {window_start}NM')

    def set_window_stop(self, window_stop):
        '''
        Sets the stopping wavelength on the display in nanometers.
        '''
        self.osamain.write(f':DISPLAY:TRACE:X:STOP {window_stop}NM')

    def set_y_reference(self, reference):
        '''
        Sets the reference level of the y axis in the display, based on the 
        current scale.
        '''
        self.osamain.write(f":DISPLAY:TRACE:Y1:RLEVEL {reference}")

    def get_single_trace(self, wavelength_start, wavelength_stop):
        '''
        This method is used to get a trace of an optical spectrum.
        '''
        try:
            #Resets device
            self.osamain.write("*RST")

            #Sets GPIB command format
            self.osamain.write("CFORM1")

            #Set wavelength range
            self.osamain.write(f":sens:wav:start {wavelength_start}nm")
            self.osamain.write(f":sens:wav:stop {wavelength_stop}nm")

            #Sets measurement sensitivity to high
            self.osamain.write(":sens:sens HIGH2")

            #Set wavelength sweep speed
            self.osamain.write(":sens:sens:speed 2x")

            #Sets automatic sampling of points
            self.osamain.write(":sens:sweep:points:auto on")
            print("Preconfig done")

            #Initiates sweep mode to SINGLE sweep
            self.osamain.write(":init:smode 1")
            print("SMODE set")

            #Clears status register
            self.osamain.write("*CLS")
            print("CLS command sent")

            #Initiates wavelength sweep
            self.osamain.write(":init")
            print("INIT command sent")

            #Gets trace
            trace_data = self.osamain.query(':TRACE:Y? TRA')
            print("Query done")
            print(trace_data[:40])

            if trace_data:
                intensities = np.array([float(val) for val in trace_data.split(',')])
                wavelengths = np.linspace(wavelength_start, wavelength_stop, len(intensities))
                return wavelengths, intensities

        except Exception as e:
            print("Error getting single trace:", e)

    def get_single_trace_with_params(self, wavelength_start, wavelength_stop, sensitivity, sweep_speed, sweep_mode):
        '''
        This method is used to get a trace of an optical spectrum that is parameterized.
        '''
        try:
            #Resets device
            self.osamain.write("*RST")

            #Sets GPIB command format
            self.osamain.write("CFORM1")

            #Set wavelength range
            self.osamain.write(f":sens:wav:start {wavelength_start}nm")
            self.osamain.write(f":sens:wav:stop {wavelength_stop}nm")

            #Sets measurement sensitivity to high
            self.osamain.write(f":sens:sens {sensitivity}")

            #Set wavelength sweep speed
            self.osamain.write(f":sens:sens:speed {sweep_speed}")

            #Sets automatic sampling of points
            self.osamain.write(f":sens:sweep:points:auto on")
            print("Preconfig done")

            #Initiates sweep mode to SINGLE sweep
            self.osamain.write(f":init:smode {self.sweep_modes[sweep_mode]}")
            print("SMODE set")

            #Clears status register
            self.osamain.write("*CLS")
            print("CLS command sent")

            #Initiates wavelength sweep
            self.osamain.write(":init")
            print("INIT command sent")

            #Gets trace
            trace_data = self.osamain.query(':TRACE:Y? TRA')
            print("Query done")
            print(trace_data[:40])

            if trace_data:
                intensities = np.array([float(val) for val in trace_data.split(',')])
                wavelengths = np.linspace(wavelength_start, wavelength_stop, len(intensities))
                return wavelengths, intensities

            return wavelengths, intensities
        except Exception as e:
            print("Error getting single trace:", e)