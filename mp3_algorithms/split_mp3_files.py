import glob
import os
import subprocess
import pathlib
from pydub import AudioSegment
import os

def main():
    base_dir = os.path.abspath('/Users/joerg/Music/Hörspiele/die_drei_fragezeichen')
    mp3_dir = os.path.abspath('/Volumes/WERDERNAS2/HÖRSPIELE2/die_drei_fragezeichen/converted_to_mp3')
    mp3_dir = pathlib.Path(mp3_dir)
    print(mp3_dir)
    # mp3_pattern = os.path.join(mp3_dir, '*.mp3')
    for mp3_file in sorted(mp3_dir.iterdir())[165:]:
        # print(mp3_file)
        if str(mp3_file.stem).startswith('.DS_Store'):
            continue
            print('after', mp3_file)
            print('stem: ', mp3_file.stem)
        print('mp3', mp3_file)
        mp3_with_out_ext = pathlib.Path(mp3_file).stem
        print('mp3_with_out_ext: ', mp3_with_out_ext)
        dir_tmp = pathlib.Path.mkdir(mp3_dir / str(mp3_file.stem))
        dir_tmp_path = os.path.join(mp3_dir, str(mp3_file.stem))
        print('dir_tmp_path: ', dir_tmp_path )

        mp3_track = AudioSegment.from_mp3(mp3_file)
        max_duration = mp3_track.duration_seconds
        #print('Maximum duration: ', int(max_duration))
        max_duration_int = int(max_duration)
        cut_list = [lf*max_duration_int*100 for lf in range(11)]
        # #print(cut_list)
        for i, segment in enumerate(cut_list):
            if i > 0:
                segment_first = cut_list[i-1]
        #         # print('segment_first: ', segment_first)
                segment_last = cut_list[i]
        #         # print('segment_last: ', segment_last)
                mp3_splitted_clip = mp3_track[segment_first:segment_last]
                
                # print('dir_tmp_path: ', dir_tmp_path)
                splitted_mp3_tmp = f"{mp3_with_out_ext}_{i:02d}.mp3"
                # print(f"splitted: ", splitted_mp3_tmp)

                full_path_mp3_splitted = os.path.join(dir_tmp_path, splitted_mp3_tmp )
                print('full: ', full_path_mp3_splitted)
                
                mp3_splitted_clip.export(full_path_mp3_splitted, format="mp3")

    # print(mp3_pattern)
    # file_list = [file for file in sorted(glob.glob(mp3_pattern, recursive = False))]
    # for file in file_list[:2]:
    #     dir_path, file_name = os.path.split(file)
    #     file_name = os.path.splitext(file_name)[0]
    #     print('file_name: ', file_name)

    
    # print('dir_tmp:' , mp3_file.stem)
    # dir_tmp = pathlib.Path.mkdir(mp3_dir / str(mp3_file.stem))

if __name__ == "__main__":
    main()