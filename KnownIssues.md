# S02 Know Issues list #

This document contains know issues for the ITxPT 2.1.1 S02 specifications. 

# S02 Known Issues #

## S02 P06 “AVMS” ##


### Section 4.2.3 Pattern Monitoring Operation ###

**Issue:** Within `PatternMonitoringDelivery` the mandatory element `MonitoredPattern` is not present if the vehicle is in DeadRun. This should have been an empty structure in the given case.

**Comment:** This is addressed by an extra XSD for the DeadRun state. There is also a DeadRun example.

### Section 4.2.4 Vehicle Monitoring Operation ###

**Issue:** Within `VehicleMonitoringDelivery` the mandatory element `VehicleActivity` is not present if the vehicle is in DeadRun. This should have been an empty structure in the given case.

**Comment:** This is addressed by an extra XSD for the DeadRun state. There is also a DeadRun example.


### Section 4.2.6 Journey Monitoring Operation ###

**Issue 1:** The max occurrences of OnwardCall is unbound while the max occurrences of PreviousCall is specified with 1.

**Comment:** This issues will be resolved in version 2.2.0 by allowing for an unbound number of occurrences.

**Issue 2:** Within `JourneyMonitoringDelivery` the mandatory element `MonitoredJourney` is not present if the vehicle is in DeadRun. This should have been an empty structure in the given case.

**Comment:** This is addressed by an extra XSD for the DeadRun state. There is also a DeadRun example.



## S02 P09 “MQTT” ##

### Section 3.3 TXT record ###

**Issue:** It is not stated explicitly what the txt-record attribute ‘topic’ points to.  

**Comment:** The under `topic=<path>` given path is inteded to be the ITxPT root-topic. Directly under `<path>` one will find all top-level topics specified by ITxPT MQTT service specifications. In the future, ITxPT services that support MQTT will populate and subscribe under this topic.   