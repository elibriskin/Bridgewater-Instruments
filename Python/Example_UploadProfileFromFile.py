import requests
import json
import os
from WSMethods import *

# Define device IP
ip = '169.254.6.8'

# Read the "wspTestFile.wsp" file from the same directory as this .py file
string = open(os.path.join(os.path.dirname(__file__),'wspTestFile.wsp')).read()
# Run splitWspString() function using the WSP string from the file
wsFreq, wsAttn, wsPhase, wsPort = splitWspString(string)
# Upload profile using split data
r = uploadProfile(ip, wsFreq, wsAttn, wsPhase, wsPort)
