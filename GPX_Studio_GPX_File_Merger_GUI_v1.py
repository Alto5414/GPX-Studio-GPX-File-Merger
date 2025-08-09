import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ----- Extension blocks -----
EXT_TRO = """<extensions>
  <gpxx:TrackExtension>
    <gpxx:DisplayColor>Red</gpxx:DisplayColor>
  </gpxx:TrackExtension>
  <gpx_style:line>
    <gpx_style:color>FF0000</gpx_style:color>
  </gpx_style:line>
</extensions>"""

EXT_TEMP_TRO = """<extensions>
  <gpxx:TrackExtension>
    <gpxx:DisplayColor>Blue</gpxx:DisplayColor>
  </gpxx:TrackExtension>
  <gpx_style:line>
    <gpx_style:color>0000FF</gpx_style:color>
  </gpx_style:line>
</extensions>"""

EXT_PA = """<extensions>
  <gpxx:TrackExtension>
    <gpxx:DisplayColor>Orange</gpxx:DisplayColor>
  </gpxx:TrackExtension>
  <gpx_style:line>
    <gpx_style:color>FFA500</gpx_style:color>
  </gpx_style:line>
</extensions>"""

EXT_LR = """<extensions>
  <gpxx:TrackExtension>
    <gpxx:DisplayColor>DarkGray</gpxx:DisplayColor>
  </gpxx:TrackExtension>
  <gpx_style:line>
    <gpx_style:color>444444</gpx_style:color>
  </gpx_style:line>
</extensions>"""

EXT_DEFAULT_GREEN = """<extensions>
  <gpxx:TrackExtension>
    <gpxx:DisplayColor>Green</gpxx:DisplayColor>
  </gpxx:TrackExtension>
  <gpx_style:line>
    <gpx_style:color>00FF00</gpx_style:color>
  </gpx_style:line>
</extensions>"""

def pick_extensions_block(lines):
    """Return the <extensions> block based on the first <name> line."""
    name_line = next((ln for ln in lines if ln.lstrip().startswith("<name>")), None)
    if not name_line:
        return EXT_DEFAULT_GREEN

    text = name_line
    # Priority order (first match wins)
    if "(TRO)" in text:
        return EXT_TRO
    if "(Temp TRO)" in text:
        return EXT_TEMP_TRO
    if "(PA)" in text:
        return EXT_PA
    if "(LR)" in text:
        return EXT_LR
    return EXT_DEFAULT_GREEN

def copy_desc_above_trkseg(lines):
    """
    Copy the first <desc> line to just above the first <trkseg> line.
    If already immediately above, don't duplicate.
    """
    desc_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<desc>")), None)
    trkseg_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<trkseg>")), None)
    if desc_idx is None or trkseg_idx is None:
        return lines, trkseg_idx  # nothing to do

    # If <desc> is already directly above <trkseg>, skip insertion
    if trkseg_idx - 1 >= 0 and lines[trkseg_idx - 1].lstrip().startswith("<desc>"):
        return lines, trkseg_idx

    # Insert a copy of the <desc> line above <trkseg>
    desc_line = lines[desc_idx]
    new_lines = lines[:trkseg_idx] + [desc_line] + lines[trkseg_idx:]
    return new_lines, trkseg_idx + 1  # trkseg has shifted down by one

def insert_extensions_above_trkseg(lines, trkseg_idx=None):
    """
    Insert the chosen <extensions> block above <trkseg>.
    If trkseg_idx is not provided (or changed), recompute it.
    """
    if trkseg_idx is None:
        trkseg_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<trkseg>")), None)
    if trkseg_idx is None:
        return lines  # no <trkseg> present; skip

    block = pick_extensions_block(lines)
    block_lines = block.splitlines()
    return lines[:trkseg_idx] + block_lines + lines[trkseg_idx:]

def process_gpx_content(content):
    lines = content.splitlines()

    # 1) Copy <desc> above <trkseg> (no duplicate if already there)
    lines, trkseg_idx = copy_desc_above_trkseg(lines)

    # 2) Insert <extensions> block above <trkseg>
    lines = insert_extensions_above_trkseg(lines, trkseg_idx)

    # 3) Trim everything above first <trk>
    try:
        trk_idx = next(i for i, line in enumerate(lines) if line.lstrip().startswith("<trk>"))
    except StopIteration:
        raise ValueError("No <trk> tag found in GPX file!")

    # 4) Remove any </gpx> lines from the retained part
    new_lines = [line for line in lines[trk_idx:] if "</gpx>" not in line]

    return "\n".join(new_lines).strip()

def merge_files(filepaths, output_path):
    if not filepaths:
        raise ValueError("No GPX files selected.")
    merged_content = []
    for idx, gpx_file in enumerate(filepaths):
        with open(gpx_file, "r", encoding="utf-8") as f:
            content = f.read()
        processed = process_gpx_content(content)
        if idx > 0:
            merged_content.append("")  # exactly one blank line between files
        merged_content.append(processed)

    # Ensure .gpx extension
    root, ext = os.path.splitext(output_path)
    if ext.lower() != ".gpx":
        output_path = root + ".gpx"

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(merged_content))
    return output_path

# ----------------- Tkinter UI -----------------
class GPXMergerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPX Merger")
        self.geometry("560x320")
        self.resizable(False, False)

        self.selected_files = []
        self.output_path = ""

        pad = {"padx": 10, "pady": 8}

        tk.Label(self, text="Select GPX files to merge:").grid(row=0, column=0, sticky="w", **pad)
        tk.Button(self, text="Choose .gpx files", command=self.choose_files, width=20).grid(row=0, column=1, **pad)

        self.files_list_var = tk.StringVar(value="No files selected.")
        tk.Label(self, textvariable=self.files_list_var, anchor="w", justify="left", wraplength=520, fg="#333").grid(
            row=1, column=0, columnspan=2, sticky="w", **pad
        )

        tk.Label(self, text="Output file (.gpx):").grid(row=2, column=0, sticky="w", **pad)
        tk.Button(self, text="Choose output...", command=self.choose_output, width=20).grid(row=2, column=1, **pad)

        self.output_var = tk.StringVar(value="No output selected.")
        tk.Label(self, textvariable=self.output_var, anchor="w", justify="left", wraplength=520, fg="#333").grid(
            row=3, column=0, columnspan=2, sticky="w", **pad
        )

        tk.Button(self, text="Merge", command=self.run_merge, width=18, height=2).grid(row=4, column=0, **pad)
        tk.Button(self, text="Quit", command=self.destroy, width=12).grid(row=4, column=1, sticky="w", **pad)

    def choose_files(self):
        paths = filedialog.askopenfilenames(
            title="Select GPX files",
            filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
        )
        if not paths:
            return
        self.selected_files = list(paths)
        # Show short summary
        if len(self.selected_files) == 1:
            disp = os.path.basename(self.selected_files[0])
        else:
            disp = f"{len(self.selected_files)} files selected (first: {os.path.basename(self.selected_files[0])})"
        self.files_list_var.set(disp)

    def choose_output(self):
        # asksaveasfilename lets user pick folder + filename in one dialog
        path = filedialog.asksaveasfilename(
            title="Save merged GPX as",
            defaultextension=".gpx",
            filetypes=[("GPX files", "*.gpx")],
            initialfile="merged_output.gpx"
        )
        if not path:
            return
        # Ensure .gpx extension even if the user removed it
        root, ext = os.path.splitext(path)
        if ext.lower() != ".gpx":
            path = root + ".gpx"
        self.output_path = path
        self.output_var.set(self.output_path)

    def run_merge(self):
        try:
            if not self.selected_files:
                messagebox.showwarning("Missing files", "Please select one or more GPX files.")
                return
            if not self.output_path:
                messagebox.showwarning("Missing output", "Please choose an output .gpx file.")
                return
            out = merge_files(self.selected_files, self.output_path)
            messagebox.showinfo("Success", f"Merged file written to:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = GPXMergerUI()
    app.mainloop()