__author__ = 'asad'

_ = lambda x: x
N_ = lambda x: x
from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.common import FirstbootOnlySpokeMixIn
from pyanaconda.constants import ANACONDA_ENVIRON, FIRSTBOOT_ENVIRON
from pykickstart.constants import FIRSTBOOT_RECONFIG

# export only the HelloWorldSpoke and HelloWorldEditSpoke classes
__all__ = ["CloudSpoke", "PackStackSpoke"]


class CloudSpoke(NormalTUISpoke):
    """
    Class for the Hello world TUI spoke that is a subclass of NormalTUISpoke. It
    is a simple example of the basic unit for Anaconda's text user interface.
    Since it is also inherited form the FirstbootSpokeMixIn, it will also appear
    in the Initial Setup (successor of the Firstboot tool).

    :see: pyanaconda.ui.tui.TUISpoke
    :see: pyanaconda.ui.common.FirstbootSpokeMixIn
    :see: pyanaconda.ui.tui.tuiobject.TUIObject
    :see: pyaanconda.ui.tui.simpleline.Widget

    """

    ### class attributes defined by API ###

    # title of the spoke
    title = N_("Cloud Support")
    category = "localization"

    def __init__(self, app, data, storage, payload, instclass):
        """
        :see: pyanaconda.ui.tui.base.UIScreen
        :see: pyanaconda.ui.tui.base.App
        :param app: reference to application which is a main class for TUI
                    screen handling, it is responsible for mainloop control
                    and keeping track of the stack where all TUI screens are
                    scheduled
        :type app: instance of pyanaconda.ui.tui.base.App
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

        NormalTUISpoke.__init__(self, app, data, storage, payload, instclass)
        # If KickStart provided apply values to spoke

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """
        NormalTUISpoke.initialize(self)
        if self.data.addons.org_centos_cloud.state == "True":
            # Addon is enabled
            self.state = True
        elif self.data.addons.org_centos_cloud.state == "False":
            self.state = False
        else:
            self.state = False
        self.data.addons.org_centos_cloud.state = str(self.state)

    def refresh(self, args=None):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        :see: pyanaconda.ui.tui.base.UIScreen.refresh
        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :return: whether this screen requests input or not
        :rtype: bool

        """

        # if self.data.addons.org_centos_cloud.state == "True":
        #     # Addon is enabled
        #     self.state = True
        # elif self.data.addons.org_centos_cloud.state == "False":
        #     # print("--disable")
        #     self.state = False


        return (True)

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the spoke.

        """

        self.data.addons.org_centos_cloud.state = str(self.state)

    def execute(self):
        """
        The excecute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the spoke.

        """

        # nothing to do here
        pass

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

        :rtype: bool

        """
        return bool(True)

    @property
    def status(self):
        """
        The status property that is a brief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str

        """

        if self.state:
            return _("Cloud Support Enabled\n")
        else:
            return _("Cloud Support Disabled\n")

    def input(self, args, key):
        """
        The input method that is called by the main loop on user's input.

        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :param key: user's input
        :type key: unicode
        :return: if the input should not be handled here, return it, otherwise
                 return INPUT_PROCESSED or INPUT_DISCARDED if the input was
                 processed succesfully or not respectively
        :rtype: bool|unicode

        """

        if str(key) == "y" or str(key) == "Y" or str(key) == "yes":
            self.state = True
        else:
            self.state = False

        # no other actions scheduled, apply changes
        self.apply()
        self.complete = True

        # close the current screen (remove it from the stack)
        self.close()
        return True

    def prompt(self, args=None):
        """
        The prompt method that is called by the main loop to get the prompt
        for this screen.

        :param args: optional argument that can be passed to App.switch_screen*
                     methods
        :type args: anything
        :return: text that should be used in the prompt for the input
        :rtype: unicode|None

        """

        return _("Do You Want to Enable Cloud Support [y|n]\n: ")

class PackStackSpoke(FirstbootOnlySpokeMixIn, NormalTUISpoke):

    # title of the spoke
    title = N_("Cloud Support")

    # categories in text mode are simple strings that are not shown anywhere,
    # every hub just has a list of categories it should display spokes from
    # let's just use one of the standard categories defined for the Summary hub
    category = "localization"

    ### methods defined by API ###
    def __init__(self, app, data, storage, payload, instclass):
        """
        :see: pyanaconda.ui.tui.base.UIScreen
        :see: pyanaconda.ui.tui.base.App
        :param app: reference to application which is a main class for TUI
                    screen handling, it is responsible for mainloop control
                    and keeping track of the stack where all TUI screens are
                    scheduled
        :type app: instance of pyanaconda.ui.tui.base.App
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

        NormalTUISpoke.__init__(self, app, data, storage, payload, instclass)
        # FirstbootOnlySpokeMixIn.__init__(self)


    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """
        NormalTUISpoke.initialize(self)
        # If KickStart provided apply values to spoke
        self.enabled = True
        self.success = False
        if self.data.addons.org_centos_cloud.state == "False":
            #Addon is disabled
            self.msg = "Addon is disabled"
            print (self.msg)
            self.enabled = False
            self.complete = True
        elif self.data.addons.org_centos_cloud.state == "True":
            # Addon is enabled
            # Case mode is also specified in KS
            if self.data.addons.org_centos_cloud.arguments == "--allinone":
                #TODO: maybe it's better defined in initialize.
                # Just run packstack and return success & complete True or False
                print("--allinone provided\n")
                self.complete = True
                self.success = True
                self.msg = "Successfully setup OpenStack"
            elif self.data.addons.org_centos_cloud.arguments == "none":
                #Make the spoke Incomplete, prompt for Input
                self.msg = "Please Confirm if you want to setup OpenStack"
                self.complete = False
                self.success = True

    def refresh(self, args=None):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        :see: pyanaconda.ui.tui.base.UIScreen.refresh
        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :return: whether this screen requests input or not
        :rtype: bool

        """
        print ("in referesh")
        if not self.enabled:
            return  False
        else:
            #print("--disable")
            return True

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the GUI elements.

        """
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
        return (self.enabled)

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

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

        return _(self.msg)

    def prompt(self, args=None):
        """
        The prompt method that is called by the main loop to get the prompt
        for this screen.

        :param args: optional argument that can be passed to App.switch_screen*
                     methods
        :type args: anything
        :return: text that should be used in the prompt for the input
        :rtype: unicode|None

        """

        return _("Do You Want to Setup OpenStack? [y|n]\n: ")

    def input(self, args, key):
        """
        The input method that is called by the main loop on user's input.

        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :param key: user's input
        :type key: unicode
        :return: if the input should not be handled here, return it, otherwise
                 return INPUT_PROCESSED or INPUT_DISCARDED if the input was
                 processed succesfully or not respectively
        :rtype: bool|unicode

        """

        if str (key) == "y" or str (key) == "Y" or str (key) == "yes":
            self.complete = True
        else:
            self.complete = False

        # no other actions scheduled, apply changes
        self.run_packstack(key)
        self.apply()

        # close the current screen (remove it from the stack)
        self.close()
        return True

    def run_packstack(self,key):

        print("IN RUN PACKSTACK")
