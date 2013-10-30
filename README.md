Modbus RTU Python
======



If you have serial Modbus/RTU slaves attached to embebbed serial modules, then you'll need to create the original Modbus/RTU requests to send. This is quite easily done with Python.
In the last weeks I have researched a lot about this subject. Many forums say to use libraries: Pymodbus, Minimal Modbus or Modbus-tk. Tested all and say: that it is easier to use and create PySerial polling messages directly than using these libraries.

Requirement: PySerial Library

These tests have been compiled in python 2.7
