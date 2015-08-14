# coding=utf-8
# will never be translated
_ = lambda x: x
N_ = lambda x: x
import pdb
from pyanaconda.ui.gui.categories.software import SoftwareCategory
from pyanaconda.ui.gui import GUIObject
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootOnlySpokeMixIn

# export only the spoke, no helper functions, classes or constants
__all__ = ["CloudSpoke","PackStackSpoke"]


class CloudSpoke(NormalSpoke):
    """
​    Class for the CloudSpke. This spoke will only be shown during the setup
    (Summary Hub). This will be in Software Category (OpenStack is a software)  ​
​    """

    mainWidgetName = "CloudSpokeWindow"
#    uiFile = "cloud-enable.glade"
    uiFile = "cloud.glade"
    category = SoftwareCategory
    builderObjects = ["CloudSpokeWindow", "button1", "button1a", "button1b", "button2", "fileurl"]
    icon = "weather-overcast-symbolic"
    title = N_("_CLOUD SUPPORT")

    ### methods defined by API ###
    def __init__(self, data, storage, payload, instclass):
        """
        :see: pyanaconda.ui.common.Spoke.__init__
        :param data: data object passed to every spoke to load/store data
                     from/to it
        :type data: pykickstart.base.BaseHandler
        :param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        :type storage: blivet.Blivet
        :param payload: object storing packaging-related information
        :type payload: pyanaconda.packaging.Payload
        :param instclass: distribution-specific information
        :type instclass: pyanaconda.installclass.BaseInstallClass

        """

        NormalSpoke.__init__(self, data, storage, payload, instclass)

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """

        NormalSpoke.initialize(self)
        self.button1 = self.builder.get_object("button1")
        self.button1a = self.builder.get_object("button1a")
        self.button1b = self.builder.get_object("button1b")
        self.button2 = self.builder.get_object("button2")
        self.link = self.builder.get_object("fileurl")

        # Check if Values Provided in KickStart
        if self.data.addons.org_centos_cloud.state == "False":
            # ADDON : DISABLED
            self.button2.set_active(True)
        else:
            # DEFAULT = ENABLED
            self.button1.set_active(True)
            # If no argument provided DEFAULT --allinone is assumed
            if not (str (self.data.addons.org_centos_cloud.arguments).startswith("--answer-file")):
                self.data.addons.org_centos_cloud.arguments = "--allinone"


    def refresh(self):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh

        """
        if self.data.addons.org_centos_cloud.state == "False":
            #Addon is disabled/ Not mentioned in KS
            self.button2.set_active(True)
        else:
            # DEFAULT ENABLED
            # Addon is enabled
            self.button1.set_active(True)
            if self.data.addons.org_centos_cloud.arguments == "--allinone" or self.data.addons.org_centos_cloud.arguments == "none":
                self.button1a.set_active(True)
            else: # answer-file
                self.button1a.set_active(False)
                self.link.set_text(str (self.data.addons.org_centos_cloud.arguments).replace("--answer-file=", ""))

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the GUI elements.

        """
        if self.button1.get_active():
            self.data.addons.org_centos_cloud.state = str(True)
            if self.button1b.get_active():
                self.data.addons.org_centos_cloud.arguments = "--answer-file=" + str(self.link.get_text())
            else:
                self.data.addons.org_centos_cloud.arguments = "--allinone" # DEFAULT

        else:
            self.data.addons.org_centos_cloud.state = str(False)

    def execute(self):
        """
        The excecute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the GUI elements.

        """

        # TODO: MAYBE Add URL Verfication HERE
        pass

    @property
    def ready(self):
        """
        The ready property that tells whether the spoke is ready (can be visited)
        or not. The spoke is made (in)sensitive based on the returned value.

        :rtype: bool

        """
        #TODO: Add Cloud Package check here
        # this spoke is always ready
        return True

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted according to the returned value.

        :rtype: bool

        """
        return True

    @property
    def mandatory(self):

        """
        The mandatory property that tells whether the spoke is mandatory to be
        completed to continue in the installation process.

        :rtype: bool

        """
        # this is an optional spoke that is not mandatory to be completed
        return False

    @property
    def status(self):
        """
        The status property that is a brief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str

        """
        if self.button1.get_active():
            state = "Enabled"
        else:
            state = "Disabled"

        return _("Cloud Support %s") % state

    ### handlers ###

    def on_button1_toggled(self, button):

        if self.button1.get_active():
            self.button1a.set_sensitive(True)
            self.button1b.set_sensitive(True)
            self.link.set_sensitive(True)
            self.button1a.set_active(True)
        else:
            self.button1a.set_sensitive(False)
            self.button1b.set_sensitive(False)
            self.link.set_sensitive(False)

    def on_button1a_toggled(self, button):
        if self.button1a.get_active():
            self.link.set_sensitive(False)

    def on_button1b_toggled(self, button):
        self.link.set_sensitive(True)
        # pass

    def on_button2_toggled(self, button):
        pass


class PackStackSpoke(FirstbootOnlySpokeMixIn, NormalSpoke):
    """
​    Class for the CloudSpke. This spoke will only be shown during the setup
    (Summary Hub). This will be in Software Category (OpenStack is a software)  ​
​    """

    mainWidgetName = "CloudSpokeWindow"
    uiFile = "packstack.glade"
    builderObjects = ["CloudSpokeWindow", "button1", "progressbar1"]
    icon = "weather-overcast-symbolic"
    title = N_("_CLOUD SUPPORT")
    category = SoftwareCategory

    ### methods defined by API ###
    def __init__(self, data, storage, payload, instclass):
        """
        :see: pyanaconda.ui.common.Spoke.__init__
        :param data: data object passed to every spoke to load/store data
                     from/to it
        :type data: pykickstart.base.BaseHandler
        :param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        :type storage: blivet.Blivet
        :param payload: object storing packaging-related information
        :type payload: pyanaconda.packaging.Payload
        :param instclass: distribution-specific information
        :type instclass: pyanaconda.installclass.BaseInstallClass

        """

        NormalSpoke.__init__(self, data, storage, payload, instclass)

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """

        NormalSpoke.initialize(self)
        self.success = False
        self.complete = False
        self.data.addons.org_centos_cloud.env = "firstboot"
        self.button = self.builder.get_object("button1")
        self.progressbar = self.builder.get_object("progressbar1")
        if self.data.addons.org_centos_cloud.state == "False":
            # Addon is disabled
            self.complete = True
        elif self.data.addons.org_centos_cloud.state == "True":
            #print("--disable")
            if self.data.addons.org_centos_cloud.arguments == "--allinone":
                pass # call run packstack --allinone or activate click button
            elif self.data.addons.org_centos_cloud.arguments: # --answer-file
                pass # call packstack --answer-file ()
            else:
                self.complete = False
    def refresh(self):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh

        """
        pass

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the GUI elements.

        """
        # TODO: add --answer-file
        if self.success:
            self.data.addons.org_centos_cloud.arguments = "--allinone"
        else:
            self.data.addons.org_centos_cloud.arguments = "none"

    def execute(self):
        """
        The excecute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the GUI elements.

        """

        # nothing to do here
        pass

    @property
    def ready(self):
        """
        The ready property that tells whether the spoke is ready (can be visited)
        or not. The spoke is made (in)sensitive based on the returned value.

        :rtype: bool

        """
        #TODO: Add Cloud Package check here
        # this spoke is always ready
        return True

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

        :rtype: bool

        """
        if self.success:
            self.complete = True

        return bool(self.complete)

    @property
    def mandatory(self):
        """
        The mandatory property that tells whether the spoke is mandatory to be
        completed to continue in the installation process.

        :rtype: bool

        """

        # this is an optional spoke that is not mandatory to be completed
        if self.data.addons.org_centos_cloud.state == "True":
            return True
        else:
            return False

    @property
    def status(self):
        """
        The status property that is a brief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str

        """
        if self.success:
            return  _("OpenStack Successfully Setup")
        else:
            return _("OpenStack NOT Setup")

    ### handlers ###
    def on_button1_clicked(self, button, *args):
        if self.data.addons.org_centos_cloud.state == "True":
            # print ("I am on button clicked")
            success = True
        else:
            pass
