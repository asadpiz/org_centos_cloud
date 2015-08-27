# OpenStackAnaconda: OpenStack Addon for Anaconda Installer

This is an addon that enables installation/setup of OpenStack during CentOS installation ([*Background & Motivation*](http://seven.centos.org/2015/07/cloud-in-a-box-centos-openstack-remix/))

## Introduction:

To ease openstack deployment concerns, this addon aims to provide a robust, pre-configured (yet customizable) and easily installed openstack setup. The result is a [CentOS 7 (Remixed) ISO](http://buildlogs.centos.org/gsoc2015/cloud-in-a-box/CentOS-7-x86_64-RDO-1503-2015082701.iso) with an option to setup openstack during installation. 

## Implementation:

This addon integrates RDO (Red Hat community's openstack package repository) and Packstack (openstack deployment tool) with Anaconda:

1. During Setup: [RDO](https://www.rdoproject.org/Main_Page) (openstack) [packages](http://mirror.centos.org/centos/7/cloud/x86_64/openstack-kilo/) are installed.
2. Firstboot: OpenStack is configured & deployed using [packstack](https://wiki.openstack.org/wiki/Packstack).

* List of RDO Packages Installed can be accessed at: [Package List](../master/PackageList.md)
* 
## System Requirements:

*  CentOS 7 (anaconda 19.31.123) Remix ISO (~1GB) [LINK](http://buildlogs.centos.org/gsoc2015/cloud-in-a-box/CentOS-7-x86_64-RDO-1503-2015082701.iso)

*  System with atleast 1 NIC configured and 4GB RAM. 

* **Note: During Setup You MUST setup the Network Interface otherwise installation will fail**

## Current Status:

Anaconda has three modes of operation i.e., Kickstart, Graphical and Text User Interfaces. Hence our add-on development is divided into adding openstack installation support for each of these three modes. 
Uptill now GUI & TUI support has been implemented.

Kickstart is also almost supported but there is a piece of code in the initial-setup-utility which prevents packstack from being executed at firstboot.

## Usage Instructions:

* Fetch [CentOS Remix ISO](http://buildlogs.centos.org/gsoc2015/cloud-in-a-box/CentOS-7-x86_64-RDO-1503-2015082701.iso), Then Simply run the setup. 

> The remix ISO can also be generated locally through a [script](https://github.com/asadpiz/centos-respin/archive/master.zip). 

* After Selecting Language the Main Hub should look like this:

![Alt text](/../screenshots/1.png?raw=true "Main Hub")

* **Network Configuration**: Go to Network & HostName Spoke and Enable Network by Clicking the toggle button:

![Alt text](/../screenshots/2.png?raw=true "Network Spoke")

* After Enabling Network the Spoke should display the Network Summary.
![Alt text](/../screenshots/2-1.png?raw=true "Network Spoke")

* **Cloud Support**: Go to Cloud Support Spoke:
![Alt text](/../screenshots/3.png?raw=true "Cloud Spoke")

* **PackStack Mode**: Select the mode of PackStack Installation, currently both *--allinone* & *--answer-file* are supported.
![Alt text](/../screenshots/4.png?raw=true "Cloud Spoke-2")

* **Summary**: The Summary Hub should Look like the following i.e., both Network Interface and Cloud Support must be enabled. Then Click "Begin Installation"
![Alt text](/../screenshots/5.png?raw=true "Summary")

* At Firstboot, the following Installation screen will be displayed. Just Go to *License Information* and accept the license:

![Alt text](/../screenshots/6.png?raw=true "Firstboot")

* Just Press *c* and OpenStack Setup via Packstack will begin.
![Alt text](/../screenshots/8.png?raw=true "Firstboot")


> **[[OPTIONAL]]** To use the latest version of addon: At the first install screen of CentOS press "TAB" and append the following command: `inst.updates=https://github.com/asadpiz/org_centos_cloud/releases/download/v0.1-alpha/updates.img`


## Contact Info:
IRC: asad_ (#centos-devel)

 

 
