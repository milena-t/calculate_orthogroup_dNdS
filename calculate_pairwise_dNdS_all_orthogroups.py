## calculate pairwise dNdS for a list of orthogroups
# assumes a list with one orthogroup per line like like in this orthofinder output file:
# Orthogroups/Orthogroups_SingleCopyOrthologues.txt

import sys
import os

## prepare to run calculate_orthogroup_dNdS.py 
## split the complete list into 20 separate files to easier parallelize everything
def split_file(input_file_path, lines_per_file=100):
    file_counter = 1
    line_counter = 0
    output_file = None

    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            if line_counter % lines_per_file == 0:
                if output_file:
                    output_file.close()
                output_file = open(f'single_copy_orthogroups_split_{file_counter}.txt', 'w')
                file_counter += 1
            output_file.write(line)
            line_counter += 1

    if output_file:
        output_file.close()

input_file_path = '/path/to/Orthogroups/Orthogroups_SingleCopyOrthologues.txt'

# only run once 
#split_file(input_file_path, lines_per_file=100)

## take list of OG ids in file as input
## example command:
#  python3 calculate_pairwise_dNdS_all_orthogroups.py single_copy_orthogroups_split_1.txt


if len(sys.argv)>1:
    og_list_filepath = sys.argv[1]

    OG_list = []
    with open(og_list_filepath, "r") as og_list_file:
        OG_list = [OG_id.split("\n")[0] for OG_id in og_list_file.readlines()]

    print(OG_list)

    for OG_id in OG_list:
        print(OG_id)

        ## change this orthofinder results path!
        command = f"python3 calculate_orthogroup_dNdS.py --orthogroup /path/to/Orthogroup_Sequences/{OG_id}.fa --cds /path/to/cd_sall_species --pal2nalbin /path/to/pal2nal.pl --verbose"
        print(command)

        # run the command 
        exit_status = os.system(command)

        # Check the exit status
        if exit_status == 0:
            print(f"{OG_id} finished successfully")
        else:
            print(f"{OG_id} failed with exit status", exit_status)

        
