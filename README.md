# OpenstackAnaconda: OpenStack addon for Anaconda Installer

To ease openstack deployment concerns, this addon aims to provide a robust, customizable and easily installed openstack setup through CentOS installer. The result will be a CentOS (Remixed) ISO with an option to setup openstack during installation. 

Design:

The development involves integrating RDO (Red Hat community's openstack package repository) and Packstack (openstack deployment tool) with Anaconda. The resulting remix will:

    Install RDO (openstack) packages during setup.
    Use packstack to configure & deploy openstack (in post-install phase).

Current Status:

Anaconda has three modes of operation i.e., Kickstart, Graphical and Text User Interfaces. Hence our add-on development is divided into adding openstack installation support for each of these three modes. Uptill now Kickstart support has been implemented i.e., user is able to install openstack through a kickstart file during setup.

Currently GUI support is being developed. After that TUI support and openstack customization options will be added. Final deliverable will be an "CentOS Openstack remix" ISO (~1.2GB) built using CentOS minimal ISO.

Testing Instructions:
1. Fetch CentOS ISO from: <Under Progress>
2. At the first install screen press "TAB" and append the following command: inst.updates=<updates-file url>

Contact Info:
IRC: asad_ (#centos-devel)

 

 
