# OpenStackAnaconda: OpenStack addon for Anaconda Installer

*This is an addon that enables installation/setup of OpenStack during Linux installation.*

[*Background & Motivation*](http://seven.centos.org/2015/07/cloud-in-a-box-centos-openstack-remix/)

** The remixed CentOS 7 ISO can be obtained from: [TBA]**

## Introduction:

To ease openstack deployment concerns, this addon aims to provide a robust, pre-configured (yet customizable) and easily installed openstack setup. The result will be a CentOS (Remixed) ISO
with an option to setup openstack during installation. 

## Implementation:

This addon integrates RDO (Red Hat community's openstack package repository) and Packstack (openstack deployment tool) with Anaconda:

1. During Setup: [RDO](https://www.rdoproject.org/Main_Page) (openstack) packages are installed.
2. Firstboot: OpenStack is configured & deployed using [packstack](https://wiki.openstack.org/wiki/Packstack).

System Requirements:

CentOS 7 (anaconda 19.31.123)
[Cloud Repository- Link TBA]- Meanwhile [Package List](../blob/master/PackageList.md)


## Current Status:

Anaconda has three modes of operation i.e., Kickstart, Graphical and Text User Interfaces. Hence our add-on development is divided into adding openstack installation support for each of these three modes. 
Uptill now Kickstart support has been implemented i.e., user is able to install openstack through a kickstart file during setup.

Currently GUI support is being developed. After that TUI support and openstack customization options will be added.
Final deliverable will be an "CentOS Openstack remix" ISO (~1.2GB) built using CentOS minimal ISO.

## Testing Instructions:
There are three ways to test the addon:

**Method 1.** Fetch CentOS ISO from [Under Progress], which contains the addon and simply run the installer.

**Method 2.** Use "updates.img" file and At the first install screen of CentOS press "TAB" and append the following command: `inst.updates=[Under Progress]`

*Note: The ISO you choose must have all openstack packages, Fetch the CentOS ISO here.*

**Method 3**. Generate updates.img from source: Clone the source from the repository and place it in a new directory tmpo/usr/share/anaconda/addons/. Then from the tmpo directory run the following command:
`find . | cpio -c -o | gzip -9 > updates.img`

Then use Method 2.
 
## Contact Info:
IRC: asad_ (#centos-devel)

 

 
