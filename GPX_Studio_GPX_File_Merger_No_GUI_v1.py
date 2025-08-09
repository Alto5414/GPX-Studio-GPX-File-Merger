# Hosted on GitHub https://github.com/Alto5414/GPX-Studio-GPX-File-Merger
# Author: Matthew Dawson-Paver
# Original Date: Aug 2025

import os

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
    if "(TRO)" in text:
        return EXT_TRO
    if "(Temp TRO)" in text:
        return EXT_TEMP_TRO
    if "(PA)" in text:
        return EXT_PA
    if "(LR)" in text:
        return EXT_LR
    return EXT_DEFAULT_GREEN

def process_gpx_content(content):
    lines = content.splitlines()

    # --- Step 1: Copy <desc> to above <trkseg> ---
    desc_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<desc>")), None)
    trkseg_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<trkseg>")), None)
    if desc_idx is not None and trkseg_idx is not None:
        desc_line = lines[desc_idx]
        lines.insert(trkseg_idx, desc_line)
        # If we inserted, shift trkseg index for next insertion
        trkseg_idx += 1

    # --- Step 2: Insert <extensions> block above <trkseg> ---
    if trkseg_idx is None:
        trkseg_idx = next((i for i, line in enumerate(lines) if line.lstrip().startswith("<trkseg>")), None)
    if trkseg_idx is not None:
        block = pick_extensions_block(lines)
        block_lines = block.splitlines()
        lines = lines[:trkseg_idx] + block_lines + lines[trkseg_idx:]

    # --- Step 3: Remove everything above first <trk> ---
    try:
        trk_idx = next(i for i, line in enumerate(lines) if line.lstrip().startswith("<trk>"))
    except StopIteration:
        raise ValueError("No <trk> tag found in GPX file!")

    # --- Step 4: Remove </gpx> lines ---
    new_lines = [line for line in lines[trk_idx:] if "</gpx>" not in line]

    return "\n".join(new_lines).strip()

def merge_gpx_from_directory(input_dir, output_filename):
    gpx_files = sorted([
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
        if fname.lower().endswith(".gpx")
    ])
    if not gpx_files:
        print("No GPX files found in the directory.")
        return

    merged_content = []
    for idx, gpx_file in enumerate(gpx_files):
        with open(gpx_file, "r", encoding="utf-8") as f:
            content = f.read()
        processed = process_gpx_content(content)
        if idx > 0:
            merged_content.append("")  # one blank line between files
        merged_content.append(processed)

    output_txt_path = os.path.join(input_dir, output_filename)
    with open(output_txt_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(merged_content))
    print(f"Merged file written to: {output_txt_path}")

# --- Usage ---
input_directory = r"C:\Users\[insertusername]\Downloads\GPX_Downloads" # local directory. change as needed
output_file = "merged_output.gpx"
merge_gpx_from_directory(input_directory, output_file)
