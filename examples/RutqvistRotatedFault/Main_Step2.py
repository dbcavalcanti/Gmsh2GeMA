import json
import os
import shutil
import platform
import subprocess
from sys import argv
import time as timer

def print_title(title):
    print("\n" + "#" * len(title))
    print(title)
    print("#" * len(title) + "\n")

if __name__ == '__main__':

    print(" ")
    print(timer.ctime())
    print_title("Re-meshing process started")
    initial_time = timer.perf_counter()

    # Reading json input file
    json_time_start = timer.perf_counter()
    if len(argv) == 2: # GeometryData is being passed from outside
        input_file_name = argv[1]
    else: # using default name
        input_file_name = 'GeometryData.json'
    print("Time to read JSON input file:          %.3f [s]" % (timer.perf_counter() - json_time_start))

    # Basic paths
    # NOTE: By now, the only accepted paths are the ones without blank spaces.
    #       This must be also accomplished for the "gid_path" variable in .json file.
    #       EXAMPLE: 'C:/Users/Exxon User/...' --> NOT VALID
    #                'C:/Users/ExxonUser/...'  --> VALID
    # TODO: Implement a way to accept paths with blank spaces
    project_path = os.getcwd()
    project_path = project_path.replace(os.sep, '/')
    if platform.system()=='Windows':
        execute_gid = 'gid'
    else:
        execute_gid = './gid'
    with open(input_file_name,'r') as input_file:
        json_data = json.load(input_file)
    gid_path = json_data['gid_path']
    gid_path = gid_path.replace(os.sep, '/')

    gid_project_path = project_path + '/' + 'temp' + '/' + str(json_data['project_name']) + '.gid'
    if not os.path.exists(gid_project_path):
        print(f"The GiD project is not inside temp folder. Please run the 1st step.")
        exit()
    
   # Initialize GiD
    gid_time_start = timer.perf_counter()
    project_batch_file_name = str(json_data['project_name'])+'_step2'+'.bch'
    project_batch_file_path = os.path.join(str(project_path),str(project_batch_file_name))
    project_batch_file_path = project_batch_file_path.replace(os.sep, '/')
    project_file_path = os.path.join(str(project_path),'temp',str(json_data['project_name']))
    project_file_path = project_file_path.replace(os.sep, '/')
    project_gid_file_path = str(project_file_path)+'.gid'
    # print(project_gid_file_path)
    # print(project_file_path)
    with open(project_batch_file_name, 'w') as file:
        file.write('*****MARK START_COMMAND\n')
        file.write('Data\n')
        file.write('Defaults\n')
        file.write('ProblemType\n')
        file.write('ExxonPoromechanicsApplication\n')
        file.write('*****MARK END_COMMAND\n')
        file.write('escape\n')
        file.write('*****MARK START_COMMAND\n')
        file.write('Files\n')
        file.write('Read\n')
        file.write(str(project_gid_file_path)+'\n')
        file.write('*****MARK READ '+str(gid_project_path)+'\n')
        file.write('*****MARK END_COMMAND\n')
        file.write('escape\n')
        file.write('*****MARK START_COMMAND\n')
        file.write('Files\n')
        file.write('Save\n')
        file.write('*****MARK SAVE '+str(gid_project_path)+'\n')
        file.write('*****MARK END_COMMAND\n')
        file.write('escape\n')
        file.write('*****MARK START_COMMAND\n')
        file.write('Quit\n')
    os.chdir(gid_path)
    # subprocess.call(str(execute_gid) + ' -b ' + str(project_batch_file_path),shell=True)
    subprocess.call(str(execute_gid) + ' -n -b ' + str(project_batch_file_path),shell=True)
    os.chdir(project_path)  
    print("Time to initialize GiD:                %.3f [s]" % (timer.perf_counter() - gid_time_start))
   
    # Delete batch file    
    if os.path.exists(project_batch_file_name):
        os.remove(project_batch_file_name)
    else:
        print(f"File '{project_batch_file_name}' does not exist.")

    # Tcl input file
    tcl_input_file_geo = 'temp/GeometryData.tcl'
    
    # Read the .json file
    with open(input_file_name,'r') as file:
        original_json_data = json.load(file)
    
    # Write the .tcl file
    with open(tcl_input_file_geo, 'w') as file:
        file.write('dict set GeometryDataDict export_triangulated_surfaces '+'\"'+str(json_data['export_triangulated_surfaces'])+'\"'+'\n')
        file.write('dict set GeometryDataDict export_closed_regions '+'\"'+str(json_data['export_closed_regions'])+'\"'+'\n')

        file.write('dict set GeometryDataDict initial_fault_mesh_size '+str(json_data['initial_fault_mesh_size'])+'\n')
        file.write('dict set GeometryDataDict initial_regions_mesh_size '+str(json_data['initial_regions_mesh_size'])+'\n')

        file.write('dict set GeometryDataDict iterated_fault_mesh_size '+str(json_data['iterated_fault_mesh_size'])+'\n')
        file.write('dict set GeometryDataDict iterated_regions_mesh_size '+str(json_data['iterated_regions_mesh_size'])+'\n')

        file.write('dict set GeometryDataDict final_fault_mesh_size '+str(json_data['final_fault_mesh_size'])+'\n')
        file.write('dict set GeometryDataDict final_regions_mesh_size '+str(json_data['final_regions_mesh_size'])+'\n')

        file.write('dict set GeometryDataDict model_extension center '+'\"'+str(json_data['model_extension']['center'][0])+' '+str(json_data['model_extension']['center'][1])+'\"'+'\n')
        file.write('dict set GeometryDataDict model_extension size '+'\"'+str(json_data['model_extension']['size'][0])+' '+str(json_data['model_extension']['size'][1])+'\"'+'\n')
        file.write('dict set GeometryDataDict model_extension rotation '+str(json_data['model_extension']['rotation'])+'\n')

        # List of horizons
        horizon_id = 0
        for hor in json_data['horizons']:
            horizon_id += 1
            file.write('dict set GeometryDataDict horizons '+str(horizon_id)+' name \"'+str(hor['name'])+'\"\n')
            patch_id = 0
            for pat in hor['patches']:
                patch_id += 1
                file.write('dict set GeometryDataDict horizons '+str(horizon_id)+' patches '+str(patch_id)+' path \"'+str(pat)+'\"\n')
        
        # List of faults
        fault_id = 0
        for fau in json_data['faults']:
            fault_id += 1
            file.write('dict set GeometryDataDict faults '+str(fault_id)+' name \"'+str(fau['name'])+'\"\n')
            patch_id = 0
            for pat in fau['patches']:
                patch_id += 1
                file.write('dict set GeometryDataDict faults '+str(fault_id)+' patches '+str(patch_id)+' path \"'+str(pat)+'\"\n')

        file.write('return $GeometryDataDict \n')

    # ReMesh with the mesh size indicated in the .json file
    generate_mesh_time_start = timer.perf_counter()
    tcl_proc = 'ExxonPoromechanicsApplication::ReMeshProcess'
    os.chdir(gid_path)
    subprocess.call(str(execute_gid) + ' -n -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
    # NOTE. Comment the previous line and uncomment the following to debug tcl code in GiD
    # subprocess.call(str(execute_gid) + ' -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
    os.chdir(project_path)
    print("Time to re-generate the mesh:          %.3f [s]" % (timer.perf_counter() - generate_mesh_time_start))

    # Temporary files directory
    output_time_start = timer.perf_counter()
    temporary_files_directory_path = os.path.join(str(project_path),'temp')
    temporary_files_directory_path = temporary_files_directory_path.replace(os.sep, '/')

    # Output directory
    output_files_directory_path = os.path.join(str(project_path),'output')
    output_files_directory_path = output_files_directory_path.replace(os.sep, '/')

    # Create output step2 folder
    output_files_directory_path = os.path.join(str(output_files_directory_path),'step2')
    output_files_directory_path = output_files_directory_path.replace(os.sep, '/')

    if not os.path.isdir(output_files_directory_path):
        os.mkdir(str(output_files_directory_path))
    else:
        shutil.rmtree(str(output_files_directory_path), ignore_errors=True)
        os.mkdir(str(output_files_directory_path))

    # Move .msh files from temp folder to output folder
    for files in os.listdir(temporary_files_directory_path):
        if files.endswith('.msh'):
            src = os.path.join(temporary_files_directory_path, files)
            dst = os.path.join(output_files_directory_path, files)
            shutil.move(src, dst)

    print("Time to generate the output folder:    %.3f [s]" % (timer.perf_counter() - output_time_start))
    
    print("--------------------------------------------------")
    print("Total elapsed Time =                   %.3f" % (timer.perf_counter() - initial_time),"[s]")
    print(" ")

    print_title("Re-meshing process finished")