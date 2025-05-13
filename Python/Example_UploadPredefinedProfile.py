import requests
import json
from WSMethods import *

# Define device IP
ip = '169.254.6.8'
# Define profile according to API
profileType = 'bandpass'# blockall, transmit, bandpass, bandstop, gaussian
centerFreq = 194.000    # THz
bandwidth = 1           # THz
attenuation = 0         # dB
port = 1

# Upload predefined profile using above definition
r = uploadPredefinedProfile(ip, profileType, centerFreq, bandwidth, attenuation, port)