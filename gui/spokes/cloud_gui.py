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
    uiFile = "cloud-enable.glade"
    category = SoftwareCategory
    builderObjects = ["CloudSpokeWindow", "switch2"]
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
        self.switch = self.builder.get_object("switch2")
        if self.data.addons.org_centos_cloud.state == "True":
            # Addon is enabled
            self.switch.set_active(True)
            self.complete = True
        elif self.data.addons.org_centos_cloud.state == "False":
            #print("--disable")
            self.switch.set_active(False)
            self.complete = True
        else:
            self.complete = False

    def refresh(self):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh

        """
        if self.data.addons.org_centos_cloud.state == "True":
            # Addon is enabled
            self.switch.set_active(True)
        elif self.data.addons.org_centos_cloud.state == "False":
            #print("--disable")
            self.switch.set_active(False)

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the GUI elements.

        """
        self.data.addons.org_centos_cloud.state = str(self.switch.get_active())

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
        or uncompleted according to the returned value.

        :rtype: bool

        """

        return bool(self.complete)

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
        if self.switch.get_active():
            state = "on"
        else:
            state = "off"

        return _("Cloud Support %s") % state

    ### handlers ###

    def on_switch2_notify(self, switch, *args):
        pass
    #
    #     if self.switch.get_active():
    #         self.state = "on" #TODO: If switch active then check if Cloud Repo is available?
    #     else:
    #         state = "off"



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
        self.success = False
        self.complete = False
        NormalSpoke.initialize(self)
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
            self.data.addons.org_centos_cloud.arguments = "--disable"

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
            print ("I am on button clicked")
            success = True
        else:
            pass
