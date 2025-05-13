import pyvisa

class PowerMeter:
    '''
    This is an instrument class for controlling a ThorLabs Optical Meter.
    '''
    def __init__(self, gpib_address="USB0::0x1313::0x807B::201103226::INSTR"):
        self.gpib_address=gpib_address
        self.rm = pyvisa.ResourceManager()
        self.connection_state = False
        self.power_main = None

    def initialize(self):
        '''
        Function meant to initialize an instrument by checking to see if GPIB address is registered.
        '''
        if self.gpib_address in self.rm.list_resources():
            self.power_main = self.rm.open_resource(self.gpib_address, write_termination = '\n',read_termination='\n')
            self.connection_state = True
            print("Power Meter Initialized!")
        else:
            raise Exception("GPIB address not available!")

    def get_power(self):
        '''
        Gets measured optical power
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        power = self.power_main.query("READ?")
        return float(power)

    def set_wavelength(self, wavelength):
        '''
        Sets the wavelength of the power meter in nanometers.
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        self.power_main.write(f"SENS:CORR:WAV {wavelength}")

    def get_wavelength(self):
        '''
        Gets current wavelength of the power meter in nanometers.
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        wavelength = self.power_main.query("SENS:CORR:WAV?")
        return wavelength


    def get_beam_diameter(self):
        '''
        Gets current beam diameter
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        self.power_main.query("SENS:CORR:BEAM?")

    def get_current(self):
        '''
        Gets current of beam
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        current = self.power_main.query("MEAS:CURR?")
        return current

    def set_beam_diameter(self, diameter):
        '''
        Sets the beam diameter of the power meter
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        self.power_main.write(f"SENS:CORR:BEAM {diameter}")

    def set_averaging_rate(self, rate):
        '''
        Sets the averaging rate of the power meter
        '''
        if self.connection_state == False:
            raise Exception("No connection!")
        self.power_main.write(f"SENS:AVER:{rate}")


    def close(self):
        '''
        Closes VISA connection
        '''
        self.rm.close()





