import os
import urllib.request
import subprocess

# # Download MSBuild with VC Build Tools
# url = 'https://aka.ms/vs/17/release/vs_buildtools.exe'
# file_name = 'vs_buildtools.exe'
# urllib.request.urlretrieve(url, file_name)
#
# # Install MSBuild with VC Build Tools
# subprocess.run([file_name, '--quiet', '--add', 'Microsoft.VisualStudio.Workload.VCTools', '--includeRecommended', '--wait'], check=True)
#
# # Clean up downloaded file
# os.remove(file_name)
#
# # Path to the directory containing the MSBuild executable
# msbuild_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin"
#
# # Get the current value of the PATH environment variable
# path_variable = os.environ['PATH']
#
# # Add the MSBuild executable directory to the PATH environment variable
# if msbuild_path not in path_variable:
#     os.environ['PATH'] = msbuild_path + ';' + path_variable

# Path to msbuild.exe
msbuildexe_path = r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\msbuild.exe'

# Path to project file
project_path = r'BS_Runner\BS_Runner\BS_Runner.vcxproj'

# MSBuild command to run
command = [msbuildexe_path, project_path]

# Run the command and capture the output
subprocess.run(command)

