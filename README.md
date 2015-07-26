# OpenstackAnaconda: OpenStack addon for Anaconda Installer

To ease openstack deployment concerns, this addon aims to provide a robust, pre-configured (yet customizable) and easily installed openstack setup. The result will be a CentOS (Remixed) ISO
with an option to setup openstack during installation. 

## Implementation:

The development involves integrating RDO (Red Hat community's openstack package repository) and Packstack (openstack deployment tool) with Anaconda. The resulting remix will:

1. Install RDO (openstack) packages during setup.
2. Use packstack to configure & deploy openstack (in post-install phase).

## Current Status:

Anaconda has three modes of operation i.e., Kickstart, Graphical and Text User Interfaces. Hence our add-on development is divided into adding openstack installation support for each of these three modes. 
Uptill now Kickstart support has been implemented i.e., user is able to install openstack through a kickstart file during setup.

Currently GUI support is being developed. After that TUI support and openstack customization options will be added.
Final deliverable will be an "CentOS Openstack remix" ISO (~1.2GB) built using CentOS minimal ISO.

## Testing Instructions:
There are three ways to test the addon:
Method 1. Fetch CentOS ISO from [Under Progress], which contains the addon and simply run the installer.
Method 2. Use "updates.img" file and At the first install screen of CentOS press "TAB" and append the following command: `inst.updates=[Under Progress]`
Note: The ISO you choose must have all openstack packages, Fetch the CentOS ISO here.
Method 3. Generate updates.img from source: Clone the source from the repository and place it in a new directory tmpo/usr/share/anaconda/addons/. Then from the tmpo directory run the following command:
`find . | cpio -c -o | gzip -9 > updates.img`
Then use Method 2.
 
## Contact Info:
IRC: asad_ (#centos-devel)

 

 
