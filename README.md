# GPL to Godot
 Python script to export gpl color palettes to image textures or a ColorPoolArray for the Godot engine.

Requires PILLOW library and python 3.7.

    pip3 install pillow

Usage:

    Usage: [option] [gpl file name] [arguments]
    -i --Creates image textures, requires PILLOW.
    -g -- Prints poolcolorarray for godot project_metadata.cfg.
    -f -- Exports poolcolorarray for godot project_metadata.cfg to text file.
    -m -- Replaces color picker PoolColorArray in godot project.