# Bridgewater Instruments

A repository of Python-based remote interfaces for a variety of different instruments in the Bridgewater Photonics Lab. These currently include:

- Optical Spectrum Analyzer
- Waveshaper
- Thorlabs Power Meter
- Optical Motor System

This repository is meant to be collaborative, meaning all photonics students are welcome to make improvements to any of the code.

## Basic Installation

To install the repo, simply open Git and run:

```
git clone https://github.com/elibriskin/Bridgewater-Instruments.git
```

## General Configuration/Dependencies

The various instruments require different drivers and other dependencies in order to run properly. For example, the Waveshaper program relies on a set of utility files that come with the instrument,
while the optical motor system requires Arduino IDE. Specific device configuration details will be included below.

## Python Dependencies
In order to run these scripts, you must ensure you have all of the libraries insntallled. The most important ones are:
- *Pyvisa*: this library enables remote communication of instruments
- *Numpy*: Used for array based computations
- *Pandas*: Standard library for data/file manipulation
- *Matplotlib*: Standard library for data visualization

## OSA

### Instrument Configuration

The OSA program currently runs through a GPIB connection. To enable this connection:

1. Take a GPIB-USB adapter and connect from the OSA to local computer.
   ![image](https://github.com/user-attachments/assets/a819daa8-f8d2-41b7-bf24-dd5e75acd406)


2. You must enable GPIB remote connection on actual OSA before running scripts. To do this, follow instructions from the manual excerpt below.
   
   ![image](https://github.com/user-attachments/assets/e23eca54-0c15-467c-bbe1-02b11a0fe7de)

### Python Initialization

1. Once the GPIB connection is established, open Python (preferrably a Jupyter notebook, these are optimal for easily running instruments).
2. Make sure pyvisa is installed and run the following command. If the OSA is connected and properly configured with GPIB, you should see a 'GPIB' address. Copy and paste this, as you will
   need it to initialize the OSA.
   
   ```
   import pyvisa as visa
   
   rm = visa.ResourceManager()
   rm.list_resources()
   ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::14::INSTR')
   ```

3. Once GPIB address is copied, initialize the OSA by running the following code. You should now be connected and are now able to communicate with the OSA remotely.

   ```
   from OSA import OSA
   
   device_address = "GPIB0::1::INSTR"
   osa = OSA(address=device_address)
   osa.initialize()
   ```

### Basic OSA Commands

There are a number of current commands for the OSA that can be implemented remotely. This is not exhaustive, and others are welcomed and encouraged to add in additiona remote functions.

#### Setting the center wavelength

```
osa.set_center_wavelength(1900)
```

#### Setting the wavelength span

```
osa.set_wavelength_span(50)
```

#### Displaying the wavelength range

```
start_wavelength = 1400
stop_wavelength = 1600
osa.display_wavelength_range(start_wavelength, stop_wavelength)
```

#### Running a simple sweep
*IMPORTANT*: The speed of a wavelength sweep and scan on the OSA is contingent on certain parameters, such as the sweep speed and the wavelength resolution. The OSA has a default timeout time where remote operations 
will time out after a given number of seconds. Therefore for a scan that is slower, the OSA may timeout before the scan is completed. To prevent this from happening, you must make sure you set the OSA timeout time 
before running a scan.
```
import matplotlib.pyplot as plt

#Time in ms
osa.osamain.timeout = 120e3

wavelengths, intensities = osa.get_single_trace(1400, 1600)

plt.plot(wavelengths, intensities)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (dBm)')
```

#### Running a more complicated sweep
```
osa.osamain.timeout = 120e3
start_wavelength = 1400
stop_wavelength = 1600
sensitivity= "HIGH2"
sweep_speed = "2x"
sweep_mode = "SINGLE"
wavelengths, intensities = osa.get_single_trace_with_params(start_wavelength, stop_wavelength, sensitivity, sweep_speed, sweep_mode)

plt.plot(wavelengths, intensities)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (dBm)')
```

