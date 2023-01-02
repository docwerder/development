import glob
import os
import subprocess

def main():
    base_dir = os.path.abspath('/Users/joerg/Music/Hörspiele/die_drei_fragezeichen')
    base_dir_m4b = os.path.abspath('/Volumes/WERDERNAS2/HÖRSPIELE2/die_drei_fragezeichen')
    
    ffmpeg_path = os.path.abspath('/opt/homebrew/bin/ffmpeg')
    
    pattern = os.path.join(base_dir_m4b, '*.m4b')
    file_list = [file for file in sorted(glob.glob(pattern, recursive = False))]
    for file in file_list[3:100]:
        dir_path, file_name = os.path.split(file)
        # Drop the file extension
        file_name = os.path.splitext(file_name)[0]
        mp3_converted_folder = os.path.join(dir_path, 'converted_to_mp3')
        mp3_output_path = os.path.join(mp3_converted_folder, file_name + '.mp3')
        print(mp3_output_path)
        
        if not os.path.exists(mp3_output_path):
            # Convert
            print('Converting: ' + file)
            subprocess.call([ffmpeg_path, '-i', file, '-acodec', 'libmp3lame', mp3_output_path])
        else:
            print('Skipping: ' + file)

if __name__ == "__main__":
    main()

