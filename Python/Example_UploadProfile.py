import requests
import json
import numpy as np
from WSMethods import *

# Define device IP
ip = '169.254.6.8'

# Get device info 
result = requests.get('http://' + ip + '/waveshaper/devinfo').json()

# Set frequency variables from device info
s = result['startfreq']
e = result['stopfreq']

# Create data for wsp
wsFreq = np.linspace(s, e, int((e-s)/0.001 + 1))
wsAttn = 50*np.power(np.sin(2*np.pi/0.5*(wsFreq-193)),2)
wsPhase = np.zeros(wsFreq.shape)
wsPort = np.ones(wsFreq.shape)

# Upload profile using created data
r = uploadProfile(ip, wsFreq, wsAttn, wsPhase, wsPort)