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
    print_title("Initial meshing process started")
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

    # Initialize GiD
    gid_time_start = timer.perf_counter()
    project_batch_file_name = str(json_data['project_name'])+'.bch'
    project_batch_file_path = os.path.join(str(project_path),str(project_batch_file_name))
    project_batch_file_path = project_batch_file_path.replace(os.sep, '/')
    project_file_path = os.path.join(str(project_path),str(json_data['project_name']))
    project_file_path = project_file_path.replace(os.sep, '/')
    project_gid_file_path = str(project_file_path)+'.gid'
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
        file.write('SaveAs\n')
        file.write('-alsoresults:1\n')
        file.write('-geoversion:current\n')
        file.write('--\n')
        file.write(str(project_gid_file_path)+'\n')
        file.write('*****MARK SAVE '+str(project_file_path)+'\n')
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

    # Transform every OFF file to GiD surfaces
    model_time_start = timer.perf_counter()
    tcl_proc = 'ExxonPoromechanicsApplication::FromOFFFilesToGiDSurfaces'
    tcl_input_file_patch = 'PatchData.tcl'
    for hor in json_data['horizons']:
        for pat in hor['patches']:
            file_name_with_extension = os.path.basename(pat)
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            patch_file_path_no_extension = os.path.join(str(project_path),str(file_name))
            patch_file_path_no_extension = patch_file_path_no_extension.replace(os.sep, '/')
            patch_gid_file_path = str(patch_file_path_no_extension)+'.gid'
            # Tcl input file
            with open(tcl_input_file_patch, 'w') as file:
                file.write('dict set PatchDict file_path '+'\"'+str(pat)+'\"'+'\n')
                file.write('dict set PatchDict gid_file_path '+'\"'+str(patch_gid_file_path)+'\"'+'\n')
                file.write('return $PatchDict \n')
            os.chdir(gid_path)
            subprocess.call(str(execute_gid) + ' -n -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
            # subprocess.call(str(execute_gid) + ' -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
            os.chdir(project_path)
    for fau in json_data['faults']:
        for pat in fau['patches']:
            file_name_with_extension = os.path.basename(pat)
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            patch_file_path_no_extension = os.path.join(str(project_path),str(file_name))
            patch_file_path_no_extension = patch_file_path_no_extension.replace(os.sep, '/')
            patch_gid_file_path = str(patch_file_path_no_extension)+'.gid'
                # Tcl input file
            with open(tcl_input_file_patch, 'w') as file:
                file.write('dict set PatchDict file_path '+'\"'+str(pat)+'\"'+'\n')
                file.write('dict set PatchDict gid_file_path '+'\"'+str(patch_gid_file_path)+'\"'+'\n')
                file.write('return $PatchDict \n')
            os.chdir(gid_path)
            subprocess.call(str(execute_gid) + ' -n -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
            # subprocess.call(str(execute_gid) + ' -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
            os.chdir(project_path)
    print("Time to create the model:              %.3f [s]" % (timer.perf_counter() - model_time_start))

    # Modify input files
    temporary_time_start = timer.perf_counter()
    with open(input_file_name,'r') as input_file:
        json_data = json.load(input_file)
        horizons_index = -1
        for hor in json_data['horizons']:
            horizons_index += 1
            patches_index = -1
            for pat in hor['patches']:
                patches_index += 1
                file_name, file_extension = os.path.splitext(pat)
                file_with_new_extension = file_name + '.gid'
                file_path = os.path.join(str(project_path),str(file_with_new_extension))
                file_path = file_path.replace(os.sep, '/')
                json_data['horizons'][horizons_index]['patches'][patches_index] = file_path
        faults_index = -1
        for fau in json_data['faults']:
            faults_index += 1
            patches_index = -1
            for pat in fau['patches']:
                patches_index += 1
                file_name, file_extension = os.path.splitext(pat)
                file_with_new_extension = file_name + '.gid'
                file_path = os.path.join(str(project_path),str(file_with_new_extension))
                file_path = file_path.replace(os.sep, '/')
                json_data['faults'][faults_index]['patches'][patches_index] = file_path
        new_json_data = json.dumps(json_data, indent=4)
    auxiliar_json_file_name = 'AuxGeometryData.json'
    with open(auxiliar_json_file_name, 'w') as file:
        file.write(new_json_data)
    with open(auxiliar_json_file_name,'r') as file:
        json_data = json.load(file)

    # Tcl input file
    tcl_input_file_geo = 'GeometryData.tcl'
    
    with open(input_file_name,'r') as file:
        original_json_data = json.load(file)
    
    # original_json_data = json.load(input_file_name)
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
    print("Time to generate the temporary files:  %.3f [s]" % (timer.perf_counter() - temporary_time_start))


    # Import all surfaces inside one GiD file
    generate_mesh_time_start = timer.perf_counter()
    tcl_proc = 'ExxonPoromechanicsApplication::GenerateInitialMesh'
    os.chdir(gid_path)
    # subprocess.call(str(execute_gid) + ' -n -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
    # NOTE. Comment the previous line and uncomment the following to debug tcl code in GiD
    subprocess.call(str(execute_gid) + ' -t \"' + str(tcl_proc) + '\" ' + str(project_gid_file_path),shell=True)
    os.chdir(project_path)
    print("Time to generate the initial mesh:     %.3f [s]" % (timer.perf_counter() - generate_mesh_time_start))

    # Delete auxiliary files
    output_time_start = timer.perf_counter()
    for hor in json_data['horizons']:
        for pat in hor['patches']:
            shutil.rmtree(pat, ignore_errors=True)
    for fau in json_data['faults']:
        for pat in fau['patches']:
            shutil.rmtree(pat, ignore_errors=True)

    # Delete auxiliary .json file
    if os.path.exists(auxiliar_json_file_name):
        os.remove(auxiliar_json_file_name)
    else:
        print(f"File '{auxiliar_json_file_name}' does not exist.")

    # Create temporary folder
    temporary_files_directory_path = os.path.join(str(project_path),'temp')
    temporary_files_directory_path = temporary_files_directory_path.replace(os.sep, '/')

    if not os.path.isdir(temporary_files_directory_path):
        os.mkdir(str(temporary_files_directory_path))
    else:
        shutil.rmtree(str(temporary_files_directory_path), ignore_errors=True)
        os.mkdir(str(temporary_files_directory_path))

    # Create output general folder
    output_files_directory_path = os.path.join(str(project_path),'output')
    output_files_directory_path = output_files_directory_path.replace(os.sep, '/')

    if not os.path.isdir(output_files_directory_path):
        os.mkdir(str(output_files_directory_path))
    else:
        shutil.rmtree(str(output_files_directory_path), ignore_errors=True)
        os.mkdir(str(output_files_directory_path))

    # Create output step1 folder
    output_files_directory_path = os.path.join(str(output_files_directory_path),'step1')
    output_files_directory_path = output_files_directory_path.replace(os.sep, '/')

    if not os.path.isdir(output_files_directory_path):
        os.mkdir(str(output_files_directory_path))
    else:
        shutil.rmtree(str(output_files_directory_path), ignore_errors=True)
        os.mkdir(str(output_files_directory_path))

    # Move all the .tcl dictionaries to the temp folder and .msh to the output
    for files in os.listdir(project_path):
        if files.endswith('.tcl'):
            shutil.move(str(files), str(temporary_files_directory_path))
        elif files.endswith('.msh'):
            shutil.move(str(files), str(output_files_directory_path))
        
    # Move all the .gid projects to the temp folder
    for item in os.listdir(project_path):
        item_path = os.path.join(str(project_path),str(item))
        if item.endswith('.gid') and os.path.isdir(item_path):
            shutil.move(str(item_path), str(temporary_files_directory_path))

    print("Time to generate the output folder:    %.3f [s]" % (timer.perf_counter() - output_time_start))

    print("--------------------------------------------------")
    print("Total elapsed Time =                   %.3f" % (timer.perf_counter() - initial_time),"[s]")
    print(" ")
    print_title("Initial meshing process finished")