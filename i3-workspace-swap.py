#! /bin/python

from i3ipc import Connection

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

    return out

# Main
def main(argv):
    # dict
    workspace_dict = get_workspace_dict()

    # workspace names
    sname = None
    dname = None
    swap_name = str(time.time_ns())

    # workspace ids
    destination = None
    source = None

    # parse args
    try:
        opts, args = getopt.getopt(argv, "hd:s:", ["help", "destination=", "source="])

    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys,exit()
        
        elif opt in ("-d", "--destination"):
            dname = arg

        elif opt in ("-s", "--source"):
            sname = arg

    # no destination given -> exit
    if dname == None:
        usage()
        sys.exit(2)    

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
    

# print usage
def usage():
    msg = """Usage: i3-workspace-swap [-h] [-s NAME] -d NAME
    -h\t\t--help\t\t\tprint this mesage
    -d NAME\t--destination NAME\tdestination workspace by name to move content to
    -s NAME\t--source NAME\t\tsource workspace by name to move the content from,
    \t\t\t\t\tif none given the currently focused workspace will be used
    """
    print(msg)


if __name__ == "__main__":
    # more than prog-name in argv
    if len(sys.argv) > 1:
        # start main programm
        main(sys.argv[1:])
    # print usage
    else:
        usage()
        sys.exit(1)