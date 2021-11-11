# openwrt-packet-generator
Python files used to generate and meausre packets for communication with an OpenWrt flashed device

## Results
All the important results and graphs can be found in `final_results.zip`.
The entire results for the entire project duration can be found in `csvdump_wed_9pm.zip`, but there's a lot in there that is not relevant to the final release.


## SQM Scripts
The selection of SQM scripts used in the project are also included here as `sqm_scripts.zip`, along with any relevant configuration files involved in their usage.
These scripts should be placed within the `/usr/lib/sqm/` folder in OpenWrt, while the configuration files should be placed at `/etc/config/sqm`. 


## File description
`connections.py`: Library for creating connections between python instances and transferring files between them. Unused ATM
`coordinator.py`: Defines an object that facilitates a single testrun from the coordinator device.
`handler.ipynb`: jupyter notebook that bundles together the commands to run a test and plot/save the results.
`iperf_tools`: Backend library used to start iperf sessions. Incldues functionality for the `iperf3` python library, but all testing was done by subprocessing to the command line interface.
`sensor.py`: Defines an object that facilitates a single testrun from a sensor device.
`testing_handler_sensor.py`: Python script bundling together the commands to run a test from a sensor and save the results.


## Usage
The coordinator instance is easiest to use through the included jupyter notebook.
An instance can be manually started through `coordinator.py`, by running creating a `Coordinator` object then using `Coordinator.run_experiment()`.

An example method of running a sensor instance is included in `testing_handler_sensor.py`.
This can be similarly started manually through `sensor.py`, defining a `Sensor` object and running `Sensor.run_experiment()`.


## Requirements
This library requires [pandas 1.3.4](https://pypi.org/project/pandas/), [numpy 1.21.4](https://pypi.org/project/numpy/) and [iperf3-python 0.1.11](https://pypi.org/project/iperf3/) python libraries to be installed, along with the [iperf3 software](https://iperf.fr/iperf-download.php).
