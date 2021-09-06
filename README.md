# SEDAICO Framework

[![github](https://img.shields.io/badge/github-rdsea-blue)](https://github.com/rdsea/) ![](https://img.shields.io/github/repo-size/rdsea/sedaico)

> Note: We are currently revising the prototype and the code will be released soon


SEDAICO (Security Elasticity Dependency Analysis In Computing cOntinuum) framework aids the developers in establishing concrete security-elasticity dependency analytics for the IIoT platform services.

## Components and code structure
The Sedaico framework has the following components and the code has been structured in the same order:

![SEDAICO](figures/framework_new.svg)

## Using the framework:
The framework can be used with the following steps (For an in-depth details checkout the main paper below):
* Annotate your IUT (Implementation under test)
* Run the annotated config files with the PostProcessor
* Run the monitoring profiles
* Deploy the IoT Profile and then test profiles
* Use analytics the generate security-elasticity dependencies

Currently SEDAICO has one analytics and test profile that supports unsecured broker configuration at edge subsystem.

### Dependencies:
* Docker and Docker compose: See: https://docker.com
* Python 3.x and pip
* Bash/sh shell for provisioning IoT sensors from profile

---

### References 
Rohit Raj, Hong-Ling Truong, "On Analysis of Security and Elasticity Dependency in IIoT Platform Services", _The 2021 IEEE International Conference on Services Computing (SCC)_, (to appear).

### Citing
If you use this repository or the paper, please cite as:

```
Rohit Raj, Hong-Ling Truong, "On Analysis of Security and Elasticity Dependency in IIoT Platform Services", _2021 IEEE International Conference on Services Computing (SCC)_, (to appear), 2021.
```

or BibTeX entry

```
@inproceedings{sedaico2021,
author = {Raj, Rohit and Truong, Hong-Linh},
journal = {2021 IEEE International Conference on Services Computing (SCC)},
pages = {to appear},
volume={},
number={},
title = {On Analysis of Security and Elasticity Dependency in IIoT Platform Services},
year = {2021}
}
``` 