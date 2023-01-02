import glob
import os
import subprocess

def main():
    base_dir = os.path.abspath('/Users/joerg/Music/Hörspiele/die_drei_fragezeichen')
    ffmpeg_path = os.path.abspath('/opt/homebrew/bin/ffmpeg')
    
    pattern = os.path.join(base_dir, '**', '*.m4b')
    
    file_list = [file for file in glob.glob(pattern, recursive = True)]
    for file in file_list:
        dir_path, file_name = os.path.split(file)
        # Drop the file extension
        file_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(dir_path, file_name + '.mp3')
        
        if not os.path.exists(output_path):
            # Convert
            print('Converting: ' + file)
            subprocess.call([ffmpeg_path, '-i', file, '-acodec', 'libmp3lame', output_path])
        else:
            print('Skipping: ' + file)

if __name__ == "__main__":
    main()

