import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_exp:

    """opt_example class"""

    def activate_cm_shell_exp(self):
        pass

    @command
    def do_exp(self, args, arguments):
        """
        Usage:
               exp clean
               exp delete NAME
               exp create [NAME]
               exp info [NAME]
               exp cloud NAME
               exp image NAME
               exp flavour NAME
               exp index NAME
               exp count N

        Manages the vm

        Arguments:

          NAME           The name of a service or server
          N              The number of VMs to be started


        Options:

           -v       verbose mode

        """
        log.info(arguments)

        if arguments["clean"]:
            log.info("clean the vm")
            return

        if arguments["delete"] and arguments["NAME"]:
            log.info("delete the vm")
            return

        if arguments["info"] and arguments["NAME"]:
            log.info("vm info")
            return

        if arguments["create"] and arguments["NAME"]:
            log.info("vm info")
            return
