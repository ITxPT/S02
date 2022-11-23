# S02 Know Issues list #

This document contains know issues for the ITxPT 2.1.1 S02 specifications. 

# S02 Known Issues #

## S02 P02 GNSSLocation ##

### Section 4.2 "Detailed description of operations and data structures"###

**Issue:** The list of valid values for the GNSSCoordinateSystem element has changed - `P-90` was replaced by `PZ-90`, `IERS` by `ITRF/ITRS` and `NAD27`, `WGS72` were rermoved. This might potentially lead to compatibility issues with consuming 2.1.0/2.1.1 GNSSLocation data.

**Implementation advice:** Since this data element is optional, the implementation should in such a case ignore the element.


## S02 P06 “AVMS” ##

### Section 4.2.3 Pattern Monitoring Operation ###

**Issue:** Within `PatternMonitoringDelivery` the mandatory element `MonitoredPattern` is not present if the vehicle is in DeadRun. This should have been an empty structure in the given case.

**Comment:** This is addressed by an extra XSD for the DeadRun state. There is also a DeadRun example.

### Section 4.2.4 Vehicle Monitoring Operation ###

**Issue:** Within `VehicleMonitoringDelivery` the mandatory element `VehicleActivity` is not present if the vehicle is in DeadRun. This should have been an empty structure in the given case.

**Comment:** This is addressed by an extra XSD for the DeadRun state. There is also a DeadRun example.
