import os
import shutil
from datetime import datetime, timedelta

def read_filenames(directory):
    """Reads all filenames from a given directory."""
    return set(os.listdir(directory)) if os.path.exists(directory) else set()

def find_common_files(dir1_files, dir2_files):
    """Finds common filenames between two sets of filenames."""
    return dir1_files.intersection(dir2_files)

def extract_valid_times(filenames):
    """Extracts valid timestamps from HFSA filenames."""
    return {fname.split('.')[1]: fname for fname in filenames}

def calculate_next_day_time(valid_time):
    """Calculates the timestamp 24 hours after the given valid timestamp."""
    try:
        dt = datetime.strptime(valid_time, "%Y%m%d%H")
        next_day_dt = dt + timedelta(hours=24)
        return next_day_dt.strftime("%Y%m%d%H")
    except ValueError:
        return None

def match_gfs_files(hfsa_trim_files, gfs_files):
    """Matches GFS files to HFSA files based on 24-hour future timestamps."""
    gfs_file_list = []
    for hfsa_file in hfsa_trim_files:
        valid_time = hfsa_file.split('.')[1]
        next_day_time = calculate_next_day_time(valid_time)
        if next_day_time:
            matched_gfs = next((fname for fname in gfs_files if next_day_time in fname), None)
            gfs_file_list.append(matched_gfs if matched_gfs else "MISSING")
    return gfs_file_list

def write_filenames_to_file(output_path, filenames, append_dir_name):
    """Writes filenames to a specified file with appended directory name."""
    with open(output_path, 'w') as file:
        for fname in filenames:
            file.write(os.path.join(append_dir_name, fname) + '\n')

def main():
    # Define directories
    hfsa_dir = "/glade/derecho/scratch/biswas/HAFS_EVAL/HAFS/HAFSV2/024/HFSA"
    hfsb_dir = "/glade/derecho/scratch/biswas/HAFS_EVAL/HAFS/HAFSv2p0p1A/024"
    gfs_dir = "/glade/derecho/scratch/biswas/HAFS_EVAL/GFS"
    output_dir = "user_specified_directory_24hr"

    # Read filenames from directories
    hfsa_files = read_filenames(hfsa_dir)
    hfsb_files = read_filenames(hfsb_dir)
    gfs_files = read_filenames(gfs_dir)

    # Find common files between HFSA and HFSB
    common_files = find_common_files(hfsa_files, hfsb_files)

    # Write trimmed HFSA and HFSB filenames
    hfsa_trim_path = os.path.join(output_dir, "HFSA-Trim.txt")
    hfsb_trim_path = os.path.join(output_dir, "HFSB-Trim.txt")
    write_filenames_to_file(hfsa_trim_path, common_files, hfsa_dir)
    write_filenames_to_file(hfsb_trim_path, common_files, hfsb_dir)

    # Match GFS files to HFSA-Trim.txt
    gfs_file_list = match_gfs_files(common_files, gfs_files)

    # Write matching GFS filenames
    gfs_output_path = os.path.join(output_dir, "GFS-Matched.txt")
    write_filenames_to_file(gfs_output_path, gfs_file_list, gfs_dir)

if __name__ == "__main__":
    main()
