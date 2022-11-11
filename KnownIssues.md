# S02 Know Issues list #

This document contains know issues for the ITxPT 2.1.1 S02 specifications. 

# S02 Known Issues #

## S02 P02 GNSSLocation ##

### Section 4.2 "Detailed description of operations and data structures"###

**Issue:** The list of valid values for the GNSSCoordinateSystem element has changed - `P-90` was replaced by `PZ-90`, `IERS` by `ITRF/ITRS` and `NAD27`, `WGS72` were rermoved. This might potentially lead to compatibility issues with consuming 2.1.0/2.1.1 GNSSLocation data.

**Implementation advice:** Since this data element is optional, the implementation should in such a case ignore the element.

## S02 P04 FMStoIP ##

### Sections 4.2.3,4.2.4,4.2.5 ###

**Issue:** The attribute `ClientId` is incorrectly declared as unbound. An attribute can only be optional or required. 

**Comment:** The attribute will be handled as optional. In the next update this will be corrected accordingly. 

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

### Section 4.3.2 Planned Pattern Operation ###

**Issue 1:** Language attribute - the language attribute is missing for certain elements in `PlannedPatternDelivery` (examples: PublishedLineLabel, PublishedTtsLineLabel, etc.), `GeneralMessageDelivery`, `ConnectionMonitoringDelivery`. 

**Issue 2:** Language attribute - wrong max occurences for the element with the language attribute. To allow for multiple languages to be present any entry allowing for the language attribute needs to be set to unbound occurrences. 

**Comment:** Version 2.2.1 will fix these issues, as they hinder a full multi-language support.