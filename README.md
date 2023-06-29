# Python Travel Time Module

This module is part of the results from the Bachelor's thesis:<br> 
<a href="https://urn.kb.se/resolve?urn=urn:nbn:se:mau:diva-60096" target="_blank">*On the use of routing engines for dynamic travel time calculation within emergency vehicle transport simulation*</a>

#### Thesis abstract:
> Traditional methods for constructing simulation models can involve several
steps that require manual pre-processing of large data sets. This process may
be time-consuming and prone to human errors, while also leading to models
that are inconvenient to customize for varying simulation scenarios. In this
thesis, we propose an alternate data preparation methodology in emergency
vehicle transport simulation, which aims to eliminate parts of the manual
pre-processing. Our research is based on a previous case study using data
from Sweden’s Southern Healthcare Region. The methodology we propose is
instantiated through a proof-of-concept software module that replaces
previously used static input sets by introducing dynamic runtime calculations
of ambulance travel times. This was done in two steps where we first evaluated
several routing engines according to needs extracted from the studied case.
Secondly, we implemented and integrated the chosen routing engine into the
previously mentioned module. Testing of the module showed feasible and
consistent performance, demonstrating the potential usage of our proposed
methodology in emergency vehicle transport simulation.

#### Usage and related technologies
To use the module, an instance of OpenSourceRoutingMachine needs to be pre-loaded with OpenStreetMap data and deployed with Docker. 

* [Docker](https://www.docker.com/)
* [OpenSourceRoutingMachine](https://github.com/Project-OSRM/osrm-backend)
* [OpenStreetMap](https://www.openstreetmap.org/about)

Updated extracts for map data can be downloaded from [Geofabrik](https://download.geofabrik.de/)
