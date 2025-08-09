# GPX-Studio-GPX-File-Merger
**Author**: Matthew Dawson-Paver

**Original Date**: Aug 2025

**Built in**: Python in VS Code

**Context**: I manually manage a single multi-track GPX file, with hundreds of tracks. To add a new track I only need to paste in the <trk> ... </trk> lines from another GPX file, plus apply some <extension> lines to add track colouring. All other lines before or after that are redundant given they are already present in the master file (such as <xml> <gpx>).

**Problem Statement**: The workflow to merge many exported GPX files from GPX Studio (specifically) into the master GPX file is time-consuming, requiring many steps and repetitiveness (open file->re-structure lines->add line coloring->copy->paste->delete file -> repeat). It can take hours to create, export then merge-in 10s of gpx files.

**Program Goal**: Provide few-click solution that automatically performs this process, and merges the ready-to-paste tracks into a single file.

**Included in the repo are two versions**:
1. With GUI, providing GPX file selection
2. No GUI, hard-coded source and output directories.

**Requirements**:
- Python
- tkinter Python module (for the GUI version, not required for the non-GUI one)
- (optional) I personally used VS Code to write and test the code

For awareness, I am not a software engineer. To help me write this program I used ChatGPT.
