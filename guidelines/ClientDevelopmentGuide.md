# ITxPT S02 Client Development Guide - Release V2.1.1#

The S02 Client Development Guide contains general advice for writing client software for ITxPT services specified in S02. 

[KnownIssues.md](../KnownIssues.md) lists known issues regarding the S02 specifications. 

This guide offers advice only. The specifications take precedence. 

## mDNS and DNS-SD ##
ITxPT service interoperability is built on mDNS and DNS-SD. 

### Read and use the SRV and TXT record attributes ###
Most of the SRV and TXT record attributes have reasonable example values. Hence, it is likely though not required that most service implementation will use these example values. However, the client should never make assumptions about the values in the SRV and TXT records, instead evaluate the entries and apply/use their values. 

### Check version ###
The TXT record attribute `version` lists the specification version to which the service is compliant. The client should at minimum log a warning if the version is not in the expected range.

### Changing values ###
Both the SRV and TXT records can potentially change during operation. Especially, `status` and `xstatus` of the inventory service can be used to propagade status information.  So far only rarely implemented, this is likely to become a mandatory feature for future versions of the inventory service. 

## Reading Data ##
Reading data is a primary activity of most ITxPT clients. ITxPT services use either XML or JSON data. 

### Use a real parser ###
While it is sometimes tempting to manually pars "the few fields" of the JSON and XML structure that might be needed, good practice is to rely on a well-tested parser. For both - XML and JSON - Parsers are available in various notions and for various plattforms.

### Tolerate additional data ###
Within a major version ITxPT data provided is backward compatible from a client perspective. E.g. the majority of changes in a minor version update of the specification will be by adding additional data. A client that is capable of ignoring additional/unknown data can achieve to a certain extend forward compatibility.

*Note:* The provided XSDs are aimed at service development and are trying to be as strict as possible regarding the version of the specification they represent.

### Fault tolerance/missing data ###

A client should be fault tolerant where possible and not aggressively fail on missing data. Data that is detected as invalid should be ignored and logged. 

Please raise a specification change request if the specifications are unclear about a case where data might be missing in order to handle this case appropriately in a future version.

## Multicast ##
The GNSSLocation, FMStoIP, and VEHICLEtoIP service use multicast to distribute data.

### Check origin ip-address of data ###
It is good practice to check the origin of the data, since misconfiguration could lead to multiple instances providing data and causing unpredicted behaviour.

The client should check the origin IP address of received multicast data and match the address with DNS-SD data of the service the client wanted to use. At minimum, a client should check if data is received from multiple sources and log this as an error. 

## Other topic ## 

### A service may restart unexpectedly ###

Services can be unexpectedly restarted for various reasons. A client should be able to detect restarted services and re-subscribe where this is required. A service that becomes unavailable should be logged as an error.

### Optional features ### 
Some features of services are specified as optional. A client using an optional feature needs to be able the handle cases when this feature is not available. 


