__author__ = 'asad'

import os.path
import os, sys
import subprocess
import urllib2
import sys
import tempfile
import shutil
import fileinput
from distutils.dir_util import copy_tree
from pyanaconda.addons import AddonData
from pyanaconda.constants import ROOT_PATH
from pyanaconda import iutil
from pykickstart.options import KSOptionParser
from pykickstart.errors import KickstartParseError, KickstartValueError, formatErrorMsg
from blivet import util

__all__ = ["Cloudks"]

ANSWERS_FILE = "/root/packstack-answers.txt"
GROUP_REQUIRED = ("@Cloud",)


# Mandatory methods (handle_header, handle_line, setup, execute and __str__)

class Cloudks(AddonData):
    def __init__(self, name):

        AddonData.__init__(self, name)
        #TODO: add a dictionary instead of these variables
        self.lines = ""
        self.arguments = "none"
        self.state = "none"
        self.env = "anaconda" # Other possible value: firstboot
#       self.installer = "ks" # Other possible values: gui,tui

    # Creating %addon section in post-install anaconda.cfg file
    def __str__(self):
        addon_str = "%%addon %s " % self.name
        if self.state == "True":
            if self.arguments == "none":
                addon_str += ("--enable \n\n%end\n")
            else:
                addon_str += ("--enable " + str(self.arguments) + "\n\n%end\n")
        else:
            addon_str += ("--disable\n\n%end\n")
        return addon_str

    def handle_header(self, lineno, args):

        op = KSOptionParser()
        op.add_option("--enable", "-e", action="store_true", default=False,
                      dest="state", help="Enable Cloud Support")
        op.add_option("--disable", "-d", action="store_false",
                      dest="state", help="(Default) Disable Cloud Support")
        op.add_option("--allinone", "-a", action="store_true", default=False,
                      dest="mode", help="Specify the mode of Packstack Installation")
        op.add_option("--answer-file", "-f", action="store", type="string",
                      dest="file", help="Specify URL of answers file")
        (options, extra) = op.parse_args(args=args, lineno=lineno)

        # Error Handling
        if str(options.state) == "True":
            self.state = str(options.state)
            if options.file and options.mode:
                msg = "options --allinone and --answer-file are mutually exclusive"
                raise KickstartParseError(msg)
            elif options.file:
                try:
                    response = urllib2.urlopen(options.file)
                    for line in response:
                        self.lines += line
                except urllib2.HTTPError, e:
                    msg = "Kickstart Error:: HTTPError: " + str(e.code)
                    raise KickstartParseError, formatErrorMsg(lineno, msg=msg)
                except urllib2.URLError, e:
                    msg = "Kickstart Error: HTTPError: " + str(e.reason)
                    raise KickstartParseError, formatErrorMsg(lineno, msg=msg)
                except:
                    msg = 'Exception Unable to fetch Answers file'
                    raise KickstartParseError, formatErrorMsg(lineno, msg=msg)
                self.arguments = "--answer-file=" + options.file
            elif options.mode:
                # self.arguments = options.mode
                self.arguments = "--allinone"
            elif extra:
                msg = "Too many Arguments Specified"
                raise KickstartValueError, formatErrorMsg(lineno, msg=msg)

    def handle_line(self, line):
        """
        We don't need to do any line handling unless we want to take packstack
        command line arguments in kickstart
        :param line:
        :return:

        """

        pass

    def finalize(self):
        """

        The finalize method that is called when the end of the %addon section
        (i.e. the %end line) is processed. An addon should check if it has all
        required data. If not, it may handle the case quietly or it may raise
        the KickstartValueError exception.

        """
        # TODO: Maybe do further error handling here
        # no actions needed in this addon
        pass

    def setup(self, storage, ksdata, instclass):

        """
        During installation just install the package group
        Cloud..
        """
        #TODO: Find a better way to add packages (maybe from package file)
        if self.state == "True":
            groups = list(GROUP_REQUIRED)
            for item in groups:
                if item not in ksdata.packages.packageList:
                    ksdata.packages.packageList.append(item)
        else:
            pass

    def execute(self, storage, ksdata, instclass, users):
        """
        Post install activities, first copy the answer file
        from location given in kickstart. Second copy cirrios
        image and rabbitmq public key (both needed for offline packstack run)
        """
        # Create Answers file from given URL TODO:Copy the answer file directly
        # Add if argument==answer-file
        if self.state == "True" and self.env == "anaconda":
            if self.lines is not None:
                answer_file = os.path.normpath(ROOT_PATH + ANSWERS_FILE)
                with open(answer_file, "w") as fobj:
                    fobj.write("%s\n" % self.lines)

            # Copying repodata, cirrios image & rabbitmq public key to Host system from media
            tmpdirectory = tempfile.mkdtemp()
            os.mkdir(ROOT_PATH + "/root/cloud")
            util.mount(device="/dev/disk/by-label/CentOS\\x207\\x20x86_64", mountpoint=tmpdirectory, fstype="auto")
            # copy_tree(tmpdirectory + "/Packages/RDO", os.path.normcase(ROOT_PATH + "/var/www/html/"))
            copy_tree(tmpdirectory + "/Packages/RDO", os.path.normcase(ROOT_PATH + "/root/cloud"))
            util.umount(tmpdirectory)
            shutil.rmtree(tmpdirectory)
            with open(ROOT_PATH + '/etc/hosts', 'a') as file:
                file.write('127.0.0.1 www.rabbitmq.com\n')
            file.close()
            # Copy Addon itself to /usr/share/anaconda/addons
            #TODO: Once Packaged remove this step
            if os.path.exists(ROOT_PATH + "/usr/share/anaconda/addons/org_centos_cloud"):
                os.mkdir(ROOT_PATH + "/usr/share/anaconda/addons/org_centos_cloud")
            shutil.copytree("/usr/share/anaconda/addons/org_centos_cloud",
                            os.path.normcase(ROOT_PATH + "/usr/share/anaconda/addons/org_centos_cloud"))

            # Enabling initial-setup-text service,
            # TODO: Check if Graphical OR Text Service to Enable
            #initial-setup-text.service: Adding $HOME=/root ENV Variable & Enabling
            for line in fileinput.input(ROOT_PATH + '/usr/lib/systemd/system/initial-setup-text.service', inplace=1):
                if line.startswith('Type'):
                    print 'Environment=HOME=/root'
                print line,
            rc = iutil.execInSysroot("ln", ["-s", "usr/lib/systemd/system/initial-setup-text.service",
                                            "etc/systemd/system/multi-user.target.wants/initial-setup-text.service"])
            if rc:
                msg = "Initializing initial-setup-text service failed"
                raise KickstartValueError(msg)
            # NetworkManager: Disable
            rc = iutil.execInSysroot("rm", ["-rf", "etc/systemd/system/multi-user.target.wants/NetworkManager.service",
                                            "etc/systemd/system/dbus-org.freedesktop.NetworkManager.service",
                                            "etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service"])
            if rc:
                msg = "Disabling Network Failed"
                raise KickstartValueError(msg)

        elif (self.env == "firstboot") and (self.arguments == "--allinone"):

            rc = iutil._run_systemctl("enable", "network")
            if rc:
                print ("Network start failed")
            ret = self.run_packstack()
            if ret:
                if (self.cleanup()):
                    raw_input("OpenStack Successfully Setup! Press Any Key To Continue...")
                else:
                    raw_input(
                        "Warning! OpenStack Successfully Setup But System Cleanup failed. Press Any Key To Continue...")
        else:
            pass

    def run_packstack(self):
        """
        Executes PackStack command and displays output to the User.

        """
        shutil.copy(os.path.normcase(ROOT_PATH + "/root/cloud/epel.repo"),
                        os.path.normcase(ROOT_PATH + "/etc/yum.repos.d/epel.repo"))
        shutil.copy(os.path.normcase(ROOT_PATH + "/root/cloud/rabbitmq-signing-key-public.asc"),
                        os.path.normcase(ROOT_PATH + "/var/www/html/rabbitmq-signing-key-public.asc"))

        # Disable All other REPOS
        count = 0
        for line in fileinput.input(ROOT_PATH + "/etc/yum.repos.d/CentOS-Base.repo", inplace=True):
            if line.startswith('gpgcheck'):
                if (count < 3):
                    count += 1
                    print 'enabled=0'
            print line,
        fileinput.close()
        c = 0
        process = subprocess.Popen(["packstack", "--allinone", "--use-epel=y",
                                    "--provision-image-url=/root/cloud/cirros-0.3.1-x86_64-disk.img"],
                                   stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            c += 1

        # TODO: Handle STDOUT ERROR= return False

        print ("Number of lines" +  str(c))
        raw_input("PRESS ANY KEY TO CONITNUTE")
        # Check if Any Service has failed to start
        process = subprocess.Popen(["openstack-status"], stdout=subprocess.PIPE)
        status = ["failed"]
        for line in iter(process.stdout.readline, ''):
            if any(s in line for s in status):
                sys.stdout.write("Failed to start the following Service:\n")
                sys.stdout.write(line)
                return False
            else:
                sys.stdout.write(line)
        return True

    def cleanup(self):
        """
        Called only if PackStack Setup is successful. Returns modified system environment to default.
        It performs the following activities:
        1. Enable Repositories, during installation default repos are disabled {for offline install}
        (NOTE: EPEL repo is not changed back to default, it still points to /root/cloud/)
        2. Remove rabbitmq entry from /etc/hosts file
        3. Disable initial-setup-text service

        """
        count = 3
        for line in fileinput.input(ROOT_PATH + "/etc/yum.repos.d/CentOS-Base.repo", inplace=True):
            if line.startswith("enabled"):
                if count > 0:
                    count -= 1
                    print(line.replace("enabled=0", "enabled=1").rstrip("\n"))
                else:
                    print line,
            else:
                print line,
        fileinput.close()

        for line in fileinput.input(ROOT_PATH + '/etc/hosts', inplace=True):
                print(line.replace("127.0.0.1 www.rabbitmq.com", "").rstrip("\n"))
        fileinput.close()

        ret = iutil._run_systemctl("disable", "initial-setup-text")
        if ret:
            print ("Failed to Disable INITIAL-SETUP-UTILITY\n")
            return False
        os.remove(os.path.normcase(ROOT_PATH + "/var/www/html/rabbitmq-signing-key-public.asc"))
        return True
        #TODO: Maybe remove the /root/cloud folder
