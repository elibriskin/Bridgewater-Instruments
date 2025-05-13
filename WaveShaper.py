import numpy
import json
import requests
from Python.WSMethods import *
from scipy.constants import c

class WaveShaper:

    '''
    This is a module for controlling the Coherent Waveshaper 1000A. It is connected via
    Ethernet connection and communicates via HTTP requests.
    '''

    def __init__(self, ip_address="169.254.6.8", device_frequency=True):
        self.ip_address = ip_address
        self.get_frequency_array = np.vectorize(self.get_frequency)
        if device_frequency == True:
            self.device_info = self.get_device_info()
            self.start_frequency = self.device_info['startfreq']
            self.end_frequency = self.device_info[['stopfreq']]
        else:
            self.start_frequency = None
            self.end_frequency = None

    def get_device_info(self):
        '''
        Gets device info from the Waveshaper
        '''

        #Gets device data in json format
        result = requests.get(f'http://{self.ip_address}/waveshaper/devinfo').json()
        return result

    def get_device_frequencies(self):
        '''
        Gets start and end frequencies of Waveshaper, which can be used to generate a spectral profile.
        '''
        device_info = self.get_device_info()

        #Extracts start and end frequencies from device info
        start_frequency = device_info['startfreq']
        end_frequency = device_info[['stopfreq']]

        return start_frequency, end_frequency

    def upload_profile(self, wsFreq, wsAttn, wsPhase, wsPort):
        '''
        Uploads a spectral profile from frequency, attenuation, and phase arrays
        '''
        r = uploadProfile(self.ip_address, wsFreq, wsAttn, wsPhase, wsPort)

    def get_frequency(self, wavelength):
        '''Converts wavelength to frequency'''
        freq = (c/wavelength) / 1e12 #get frequency in THz
        return freq

    def get_array(self):
        wsFreq = np.linspace(self.start_frequency, self.end_frequency, int((self.end_frequency - self.start_frequency) / 0.001 + 1))
        return wsFreq
    def band_pass(self, center_wavelength, bandwidth):
        '''
        Uploads a band pass profile at a specific center wavelength with a specific bandwidth
        '''
        lambda_start = center_wavelength - (bandwidth/2)
        lambda_stop = center_wavelength + (bandwidth/2)
        frequency_begin = self.get_frequency(lambda_stop)
        frequency_stop = self.get_frequency(lambda_start)
        print(f'lambda begin: {lambda_start} lambda stop: {lambda_stop}')
        print(f'frequency begin: {frequency_begin} frequency stop: {frequency_stop}')
        wsFreq = np.linspace(self.start_frequency, self.end_frequency, int((self.end_frequency - self.start_frequency) / 0.001 + 1))
        wsAttn = 40*np.ones(wsFreq.shape)
        wsAttn[((wsFreq > frequency_begin) & (wsFreq < frequency_stop))] = 0

        return wsAttn

    def band_stop(self, center_wavelength, bandwidth):
        '''
        Uploads a band pass profile at a specific center wavelength with a specific bandwidth
        '''
        lambda_start = center_wavelength - bandwidth
        lambda_stop = center_wavelength + bandwidth
        frequency_begin = self.get_frequency(lambda_stop)
        frequency_stop = self.get_frequency(lambda_start)
        wsFreq = np.linspace(self.start_frequency, self.end_frequency, int((self.end_frequency - self.start_frequency) / 0.001 + 1))
        wsAttn = 40*np.ones(wsFreq.shape)
        wsAttn[((wsFreq < frequency_begin) | (wsFreq > frequency_stop))] = 0

        return wsAttn

    def gaussian(self, wsFreq, center_wavelength, sigma):
        center_frequency = self.get_frequency(center_wavelength)
        # wsFreq = np.linspace(self.start_frequency, self.end_frequency, int((self.end_frequency - self.start_frequency) / 0.001 + 1))
        arr = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((wsFreq - center_frequency) / sigma) ** 2)
        normalized_arr = (arr / np.max(arr)) * 40
        return (-1 * normalized_arr + 40)

