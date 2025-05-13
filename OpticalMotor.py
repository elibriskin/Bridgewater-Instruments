import serial
import time
import pyvisa

class OpticalMotor:
    '''
    This is an instrument class for controlling a mountable stepper motor that can rotate various optical components, such as mirrors,
    beamsplitters, or lasers.
    '''
    def __init__(self, COM):
        self.SerialObj = serial.Serial(COM)
        self.SerialObj.baudrate = 115200  # set Baud rate to 9600
        self.SerialObj.bytesize = 8     # Number of data bits = 8
        self.SerialObj.parity   ='N'    # No parity
        self.SerialObj.stopbits = 1     # Number of Stop bits = 1

    def rotate(self, degrees):
        if type(degrees)!= int:
            raise Exception("Error! Must enter an integer!")
        else:
            degree_str = str(degrees).encode('UTF-8')
            self.SerialObj.write(degree_str)

    def cLose(self):
        self.SerialObj.close()