# GPX-Studio-GPX-File-Merger
**Author**: Matthew Dawson-Paver

**Original Date**: Aug 2025

**Built in**: Python in VS Code

**Context**: I manually manage a single multi-track GPX file, with hundreds of tracks. To add a new track I only need to paste in the <trk> ... </trk> lines from another GPX file, plus apply some <extension> lines to add track colouring. All other lines before or after that are redundant given they are already present in the master file (such as <xml> <gpx>).

**Problem Statement**: The workflow to merge many exported GPX files from <a href="https://gpx.studio/app" target="_blank">GPX Studio</a>* into the master GPX file is time-consuming, requiring many steps and repetitiveness (open file->re-structure lines->add line coloring->copy->paste->delete file -> repeat). It can take hours to create, export then merge-in 10s of gpx files. <BR>
<i>*Specifically designed to work with GPX Studio GPX files without the OpenStreetMap details option selected. May work with GPX files from other sources but can't be guarenteed. </i>

**Program Goals**: 
1. Provide few-click solution that automatically performs this process, and merges the ready-to-paste tracks into a single file. Example below.
2. All contents should be compatible with the <a href="https://www.topografix.com/gpx/1/1/" target="_blank">GPX 1.1 Schema</a> and import and display correctly in the Android GPX apps I use (<a href="https://www.drivemodedashboard.com/" target="_blank">DMD2</a>, <a href="https://vecturagames.com/gpxviewerproios/" target="_blank">GPX Viewer Pro</a>).

Example of the transformation:
<img width="800" alt="image" src="https://github.com/user-attachments/assets/90135828-6097-4b96-a570-866d84cadaee" />

**Included in the repo are two versions**:
1. With GUI, providing GPX file selection
2. No GUI, hard-coded source and output directories.

**Requirements**:
- Python
- tkinter Python module (for the GUI version, not required for the non-GUI one)
- (optional) I personally used VS Code to write and test the code

For awareness, I am not a software engineer. To help me write this program I used <a href="https://chatgpt.com/" target="_blank">ChatGPT</a>.
