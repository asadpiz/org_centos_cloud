__author__ = 'asad'

import pdb
import os.path
from pyanaconda.addons import AddonData
from pyanaconda.constants import ROOT_PATH
from pykickstart.options import KSOptionParser
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pyanaconda import iutil
from pyanaconda.kickstart import Firstboot

__all__ = ["Packstackks"]

ANSWERS_FILE = "/root/packstack-answers.txt"
GROUP_REQUIRED = ("@Cloud",)


class Packstackks(AddonData):
    def __init__(self, name):

        AddonData.__init__(self, name)
        self.lines = ""
        self.arguments = False

    # Creating %addon section in post-install anaconda.cfg file
    def __str__(self):

        addon_str = "%%addon %s" % self.name
        if self.arguments:
            addon_str += " --allinone"  # TODO: Add support for other modes
        addon_str += "\n%s\n%%end\n" % self.lines
        return addon_str

    def handle_header(self, lineno, args):

        op = KSOptionParser()
        # TODO: Use STORE method for getting --answer-file=<URL> location

        op.add_option("--allinone", action="store_true", default=True,
                      dest="mode", help="Specify the mode of Packstack Installation")
        (options, extra) = op.parse_args(args=args, lineno=lineno)

        # Reject any additional arguments.
        # TODO: Modify when adding support for other modes

        if not options.mode:
            msg = "Exception no mode specified"
            raise KickstartParseError, formatErrorMsg(self.lineno, msg=msg)
        elif extra:
            msg = "Unhandled arguments on %%addon line for %s" % self.name
            if lineno is not None:
                raise KickstartParseError(formatErrorMsg(lineno, msg=msg))
            else:
                raise KickstartParseError(msg)

        # Store the result of the option parsing
        self.arguments = options.mode

    def handle_line(self, line):
        """
        The handle_line method that is called with every line from this addon's
        %addon section of the kickstart file.

        :param line: a single line from the %addon section
        :type line: str

        """

        # simple example, we just append lines to the text attribute
        if self.lines is "":
            self.lines = line.strip()
        else:
            self.lines += " " + line.strip()

    def finalize(self):
        """
        The finalize method that is called when the end of the %addon section
        (i.e. the %end line) is processed. An addon should check if it has all
        required data. If not, it may handle the case quietly or it may raise
        the KickstartValueError exception.

        """

        # no actions needed in this addon
        pass

    def setup(self, storage, ksdata, instclass):
        # During installation just install the package group Cloud..
        """
        groups = list(GROUP_REQUIRED)
        for item in groups:
            if item not in ksdata.packages.packageList:
                ksdata.packages.packageList.append(item)
                # TODO: Copy CIRIOS image & rabbitmq certificate file at this stage.
        """
        pass
    def execute(self, storage, ksdata, instclass, users):
        # Create Answers file (currently --allinone so no answers-file)
        answer_file = os.path.normpath(ROOT_PATH + ANSWERS_FILE)
        with open(ANSWERS_FILE, "w") as fobj:
            fobj.write("%s\n" % self.lines)
        pdb.set_trace()
        iutil._run_systemctl("stop", "NetworkManager")
        iutil._run_systemctl("disable", "NetworkManager")
        iutil.start_service("network")
