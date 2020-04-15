#! /bin/python

from i3ipc import Connection
from subprocess import Popen, PIPE, STDOUT

import getopt
import sys
import time

# global connection to i3ipc socket
i3 = Connection()

# build dict with all workspace names and their id
def get_workspace_dict():    
    out = {}
    for output in i3.get_tree():
        for container in output:
            for workspace in output:
                if workspace.type == "workspace":
                    out[workspace.name] = workspace.id

    # remove none workspace container    
    out.pop("__i3_scratch", None)
    return out

# workspace names as newline seperated string
def prep_dmenu_input(dict):
    out = ""
    for key in dict.keys():
        out += key + "\n"

    return out

# interactive mode using dmenu
def interactive(prompt, dict):
    cmd = ["dmenu", "-p", prompt, "-i"]
    stdinput = prep_dmenu_input(dict).encode("utf-8")

    process = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = STDOUT)
    result = process.communicate(stdinput)[0]
    out = result.decode("utf-8").replace("\n", "")
    return out

# Main
def main(argv):
    # dict
    workspace_dict = get_workspace_dict()
    interactive_dict = {"dest" : 1, "src" : 2, "all" : 3}

    # interactive mode using dmenu
    inter = 0

    # focus after switch
    focus = False

    # workspace names
    sname = None
    dname = None
    swap_name = str(time.time_ns())

    # workspace ids
    destination = None
    source = None

    # parse args
    try:
        opts, args = getopt.getopt(argv, "d:fhi:s:", ["destination=", "focus", "help", "interactive=", "source="])

    except getopt.GetoptError:
        usage(1)

    for opt, arg in opts:
        if opt in ("-d", "--destination"):
            dname = arg

        elif opt in ("-f", "--focus"):
            focus = True

        elif opt in ("-h", "--help"):
            usage(0)

        elif opt in ("-i", "--interactive"):
            inter = interactive_dict.get(arg, 4)

        elif opt in ("-s", "--source"):
            sname = arg

    # check for interactive mode
    # unknown interactive option
    if inter == 4:
        print("Error: unknown interactive option!")
        usage(1)
    # destination
    elif inter == 1:
        dname = interactive("Destination: ", workspace_dict)
    # source
    elif inter == 2:
        sname = interactive("Source: ", workspace_dict)
    # both
    elif inter == 3:
        sname = interactive("Source: ", workspace_dict)
        dname = interactive("Destination: ", workspace_dict)


    # no destination given -> exit
    if dname == None:
        print("Error: No destination given!")
        usage(1)

    # no source given -> use focused workspace + update sname
    if sname == None:
        source = i3.get_tree().find_focused().workspace().id
        for wname, wid in workspace_dict.items():
            if wid == source:
                sname = wname
    else:
        source = workspace_dict.get(sname, None)
    
    # check if source could be found
    if source == None:
        print("Error: The source workspace {} could not be found!".format(sname))
        sys.exit(1)

    # destination id    
    destination = workspace_dict.get(dname, None)

    # destination not populated with windows -> just move via name
    if destination == None:
        i3.command("[con_id={}] move to workspace {}".format(source, dname))
        # focus?
        if focus:
            i3.command("workspace {}".format(dname))
        sys.exit()

    # move destination to tmp workspace
    i3.command("[con_id={}] move to workspace {}".format(destination, swap_name))
    # move source to destination
    i3.command("[con_id={}] move to workspace {}".format(source, dname))

    # update dict and get id for swap workspace
    workspace_dict = get_workspace_dict()
    swap_id = workspace_dict.get(swap_name, None)

    # move tmp workspace to source
    i3.command("[con_id={}] move to workspace {}".format(swap_id, sname))

    if focus:
        i3.command("workspace {}".format(dname))
    

# print usage
def usage(exitCode):
    msg = """Usage: i3-workspace-swap [-h] [-s NAME] -d NAME
    -d NAME\t--destination NAME\tdestination workspace by name to move content to
    -f\t\t--focus\t\t\tfocus destination workspace after swap
    -h\t\t--help\t\t\tprint this mesage
    -i OPTION\t--interactive OPTION\tuses dmenu to select dest/src; command line arguments will be overwriten
    -s NAME\t--source NAME\t\tsource workspace by name to move the content from,
    \t\t\t\t\tif none given the currently focused workspace will be used

    Options for interacive mode:
      all\t\tsource and destination
      dest\t\tdestination only
      src\t\tsource only
    """
    print(msg)
    sys.exit(exitCode)


if __name__ == "__main__":
    # more than prog-name in argv
    if len(sys.argv) > 1:
        # start main programm
        main(sys.argv[1:])
    # print usage
    else:
        usage(1)