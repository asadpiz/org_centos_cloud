__author__ = 'asad'

_ = lambda x: x
N_ = lambda x: x
from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.common import FirstbootOnlySpokeMixIn
from pyanaconda.ui.tui.simpleline import TextWidget, CheckboxWidget
import urllib2



# export only the HelloWorldSpoke and HelloWorldEditSpoke classes
__all__ = ["CloudSpoke", "PackStackSpoke"]

#TODO: Maybe use EditTUISpoke for a more Uniform Interface

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

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """
        # If KickStart provided apply values to spoke
        NormalTUISpoke.initialize(self)
        self.link = "<URL>"
        if self.data.addons.org_centos_cloud.state == "False":
            # Addon is Disabled
            self.state = False
            self.mode = "disabled"
        else: #DEFAULT
            self.state = True
            if self.data.addons.org_centos_cloud.arguments == "--allinone" or self.data.addons.org_centos_cloud.arguments == "none":
                self.mode = "allinone"
            else: # ANSWER FILE
                self.link = str (self.data.addons.org_centos_cloud.arguments).replace("--answer-file=", "")
                self.mode = "answerfile"
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
        NormalTUISpoke.refresh(self, args)
        # It should always prompt
        box1 = CheckboxWidget(title="1. MODE: ALLINONE", text="DEFAULT", completed= (self.mode == "allinone"))
        box2 = CheckboxWidget(title="2. MODE: ANSWER FILE", text=self.link, completed= (self.mode == "answerfile"))
        box3 = CheckboxWidget(title="3. Disable OpenStack Support",completed=(self.mode == "disabled"))
        self._window += [box1, "", box2, "", box3, ""]
        return (True)

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the spoke.

        """

        self.data.addons.org_centos_cloud.state = str(self.state)
        if self.mode=="allinone":
             self.data.addons.org_centos_cloud.arguments = "--allinone"
        elif self.mode=="answerfile":
            self.data.addons.org_centos_cloud.arguments = "--answer-file=" + str (self.link)


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
        or uncompleted accSording to the returned value.

        :rtype: bool

        """
        # Default value is provided in INIT, so it's always complete
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
            return _("Cloud Support: Enabled\n")
        else:
            return _("Cloud Support: Disabled\n")

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

        if str(key) == "2":
            self.link == raw_input("Please Enter URL To Answer File:")
            #TODO: URL VALIDATION
            self.state = True
            self.mode = "answerfile"
            try:
                response = urllib2.urlopen(self.link)
                for line in response:
                    self.data.addons.org_centos_cloud.lines += line
                self.state = True
                self.mode = "answerfile"
            except:
                raw_input('Exception Unable to fetch Answers file! Press Any Key To Continue')

        elif str (key) == "3":
            self.state = False
            self.mode = "disabled"
        else:
            self.state = True
            self.mode = "allinone"

        # no other actions scheduled, apply changes
        self.apply()
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

        return _("Choose An Option For OpenStack Support [1|2|3]:")

class PackStackSpoke(FirstbootOnlySpokeMixIn, NormalTUISpoke):

    title = N_("Cloud Support")
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

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """
        NormalTUISpoke.initialize(self)

        self.enabled = True
        self.msg = ""
        self.data.addons.org_centos_cloud.env = "firstboot"
        if self.data.addons.org_centos_cloud.state == "False":
            #Addon is disabled
            self.enabled = False
            self.complete = True
            self.msg = "Cloud Support: Disabled"
        elif self.data.addons.org_centos_cloud.state == "True":
            # Addon is enabled
            # Case mode is also specified in KS
            if str(self.data.addons.org_centos_cloud.arguments).startswith("--answer-file"):
                self.complete = True
                self.msg = "PackStack Mode: " + str(self.data.addons.org_centos_cloud.arguments)
            else:
                # DEFAULT MODE: --allinone is assumed
                self.complete = True
                self.msg = "PackStack Mode: --allinone"

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
        NormalTUISpoke.refresh(self, args)
        # It should always prompt
        box1 = CheckboxWidget(title="1. Enable Cloud Support",
                                  text="OpenStack MODE: " + str(self.data.addons.org_centos_cloud.arguments),
                                  completed=(self.data.addons.org_centos_cloud.state == "True"))
        box2 = CheckboxWidget(title=("2. Disable Cloud Support"), completed= (self.data.addons.org_centos_cloud.state == "False"))
        self._window += [box1, "", box2, ""]
        return (self.enabled) # Don't Prompt if ADDON was disabled during setup, because no packages have been installed



    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the GUI elements.

        """
        if self.data.addons.org_centos_cloud.state == "False":
            self.data.addons.org_centos_cloud.arguments = ""
        else:
            if not (str(self.data.addons.org_centos_cloud.arguments).startswith("--answer-file")):
                self.data.addons.org_centos_cloud.arguments = "--allinone"

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
        return True

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

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

        return _("Do You Want to Setup OpenStack? [1|2]\n: ")

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
        if str(key) == "2":
            self.data.addons.org_centos_cloud.state = "False"
            self.msg = "Cloud Support is Disabled"
        elif str (key) == "1":
            self.data.addons.org_centos_cloud.state = "True"
            self.msg = "Cloud Support: Enabled"
        else:
            pass

        # no other actions scheduled, apply changes
        self.apply()
        # close the current screen (remove it from the stack)
        self.close()
        return True
