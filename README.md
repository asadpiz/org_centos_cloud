# OpenStackAnaconda: OpenStack addon for Anaconda Installer

This is an addon that enables installation/setup of OpenStack during Linux installation.

[*Background & Motivation*](http://seven.centos.org/2015/07/cloud-in-a-box-centos-openstack-remix/)

## Introduction:

To ease openstack deployment concerns, this addon aims to provide a robust, pre-configured (yet customizable) and easily installed openstack setup. The result will be a CentOS (Remixed) ISO
with an option to setup openstack during installation. 

## Implementation:

This addon integrates RDO (Red Hat community's openstack package repository) and Packstack (openstack deployment tool) with Anaconda:

1. During Setup: [RDO](https://www.rdoproject.org/Main_Page) (openstack) packages are installed.
2. Firstboot: OpenStack is configured & deployed using [packstack](https://wiki.openstack.org/wiki/Packstack).

## System Requirements:

*  CentOS 7 (anaconda 19.31.123) Remix ISO (~1.2GB)

* **Note: During Setup You MUST setup the Network Interface otherwise installation will fail**

* Cloud/RDO Packages from CentOS: [Package List](../master/PackageList.md)


## Current Status:

Anaconda has three modes of operation i.e., Kickstart, Graphical and Text User Interfaces. Hence our add-on development is divided into adding openstack installation support for each of these three modes. 
Uptill now GUI & TUI support has been implemented.

Kickstart is also almost supported but there is a piece of code in the initial-setup-utility which prevents packstack from being executed at firstboot.

## Testing Instructions:

* Fetch CentOS Remix ISO, Then Simply run the setup, The remix ISO can be generated through a [script](https://github.com/asadpiz/centos-respin/archive/master.zip).

How to generate Remix ISO: [Instructions](https://github.com/asadpiz/centos-respin/blob/master/README.md) 

* During Setup, there will be a spoke by the name of "Cloud Support". CUrrently both **--allinone** & **--answer-file** modes of packstack are supported. Simply Select the mode and continue.

> [TBA]: Link to Remix ISO*

* [[OPTIONAL]] To use the latest version of addon: At the first install screen of CentOS press "TAB" and append the following command: `inst.updates=[Under Progress]`


## Contact Info:
IRC: asad_ (#centos-devel)

 

 
