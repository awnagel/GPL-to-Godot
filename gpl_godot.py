from PIL import Image, ImageDraw
import re
import os
import shutil
from pathlib import Path
import sys

IMAGE_SIZES = [16, 32, 64, 128, 256]
export_path = os.path.join(os.getcwd(), "export")

def read_gpl_file(filepath):
    if os.path.exists(export_path):
        shutil.rmtree(export_path)
    os.makedirs(export_path)
    if not os.path.exists(filepath):
        print("ERROR: Not a valid file path!")
        return
    file = open(filepath)
    contents = file.readlines()
    names = []
    colors = []
    for line in contents:
        l = re.split(r'\t+', line.rstrip('\t\n '))
        #This seems to work, but do need to check for newline
        if len(l) > 2:
            continue
        t = l[0][0]
        #continue
        if not t.isdigit() and t != ' ':
            continue
        colors.append(l[0].split())
        if len(l) == 1 or l[1] == '\n':
            names.append("Untitled")
        else:
            names.append(l[1].split('\n')[0])
    
    return [colors, names]

def create_images(colors, names, image_size):
    for i in range(len(colors)):
        create_image(colors[i], names[i], image_size)

def clamp(x):
        return max(0, min(x, 255))

def create_image(color, name, image_size):
    r = int(color[0])
    b = int(color[1])
    g = int(color[2])
    if name.lower() == "untitled":
        name = "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
    img = Image.new('RGB', (image_size, image_size), color=(r, g, b))
    img.save(os.path.join(export_path, name + ".png"))
    

def create_godot_palette(colors):
    poolarray = "presets=PoolColorArray( "
    i = 0
    print("Amount of colors: " + str(len(colors)))
    for color in colors:
        i += 1
        newColor = [round(float(color[0]) / 255, 6), round(float(color[1]) / 255, 6), round(float(color[2]) / 255, 6), 1]
        if newColor == [0.0, 0.0, 0.0, 1]:
            continue
        poolarray += str(newColor)[1:len(str(newColor))-1]
        if i != len(colors):
            poolarray += ", "
    poolarray += " )"
    return poolarray

def save_config_godot_linux(results, argument):
    print("Exporting to " + argument[3] + "...")
    home = os.path.expanduser("~")
    godot_dir = home + "/.config/godot/projects/"
    if os.path.exists(godot_dir):
        for dirs in os.listdir(godot_dir):
            if dirs.startswith(argument[3]):
                filename = godot_dir + dirs + "/project_metadata.cfg"
                print(filename)
                lines = open(filename, 'r').read().splitlines()
                i = 0
                for line in lines:
                    i += 1
                    if line == "[color_picker]":
                        lines[i + 1] = create_godot_palette(results[0])
                open(filename, 'w').write('\n'.join(lines))

def save_config_godot_windows(results, argument):
    print("Exporting to " + argument[3] + "...")
    home = os.getenv('AppData')
    godot_dir = home + "\Godot\projects\\"
    print(godot_dir)
    if os.path.exists(godot_dir):
        for dirs in os.listdir(godot_dir):
            if dirs.startswith(argument[3]):
                filename = godot_dir + dirs + "\\project_metadata.cfg"
                print(filename)
                lines = open(filename, 'r').read().splitlines()
                i = 0
                for line in lines:
                    i += 1
                    if line == "[color_picker]":
                        lines[i + 1] = create_godot_palette(results[0])
                open(filename, 'w').write('\n'.join(lines))

def main():
    export_path = os.path.join(os.getcwd(), "export")
    if len(sys.argv) >= 3:
        if sys.argv[2].endswith(".gpl"):
            results = read_gpl_file(sys.argv[2])
            if results == None:
                return
            if sys.argv[1] == "-i":
                print("Creating images at " + export_path + "...")
                create_images(results[0], results[1], int(sys.argv[3]))
                return
            elif sys.argv[1] == "-g" and len(sys.argv) == 3:
                print("Creating godot poolcolorarray...")
                print(create_godot_palette(results[0]))
                return
            elif sys.argv[1] == "-f" and len(sys.argv) == 3:
                print("Creating godot export file at " + export_path + "...")
                if os.path.exists(export_path):
                    file = open(export_path + "/godot_export.txt", 'w')
                    file.write(create_godot_palette(results[0]))
                    file.close()
                    return
                else:
                    os.makedirs(export_path)
                    file = open(export_path + "/godot_export.txt", 'w')
                    file.write(create_godot_palette(results[0]))
                    file.close()
                    return
            elif sys.argv[1] == "-m" and len(sys.argv) == 4:
                arg = sys.argv
                arg[3] = arg[3].replace("_", " ")
                if os.name == 'posix':
                    save_config_godot_linux(results, arg)
                elif os.name == 'nt':
                    save_config_godot_windows(results, arg)
                return
        else:
             print("ERROR: Not a GPL file!")
    else:
        if sys.argv[1] == "--help":
                print("Usage: [option] [gpl file name] [arguments]")
                print("-i --Creates image textures, requires PILLOW.")
                print("-g -- Prints poolcolorarray for godot project_metadata.cfg.")
                print("-f -- Exports poolcolorarray for godot project_metadata.cfg to text file.")
                print("-m -- Replaces color picker poolcolorarray in godot project.")
                return
    print("Invalid command, use --help")
    

main()

