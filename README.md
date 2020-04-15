# i3-workspace-swap

 A utility for the [i3](https://i3wm.org) tiling window manager, which allows to swap the content of two workspaces. If both, the destination and the source workspace have content on them, the content will be swapped. If only a destination workspace is provided, the workspace will be created with the given name.

## Dependencies
* Python 3.x
* Python i3ipc

## Usage
`i3-workspace-swap [-h] [-s NAME] -d NAME`

Minimal argument:
* `-d NAME` or `--destination NAME`: destination workspace by name to move content to.

Optional arguments:
* `-h` or `--help`: print help message
* `-s NAME` or `--source NAME`: source workspace by name to move the content from, if none given the currently focused workspace will be used