import os
import urllib.request
import requests
import subprocess

# MSBuild installer
# Download MSBuild with VC Build Tools
url = 'https://aka.ms/vs/17/release/vs_buildtools.exe'
file_name = 'vs_buildtools.exe'
urllib.request.urlretrieve(url, file_name)

# Install MSBuild with VC Build Tools
subprocess.run(
    [file_name, '--quiet', '--add', 'Microsoft.VisualStudio.Workload.VCTools', '--includeRecommended', '--wait'],
    check=True)

# Clean up downloaded file
os.remove(file_name)

# Path to the directory containing the MSBuild executable
msbuild_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin"

# Get the current value of the PATH environment variable
path_variable = os.environ['PATH']

# Add the MSBuild executable directory to the PATH environment variable
if msbuild_path not in path_variable:
    os.environ['PATH'] = msbuild_path + ';' + path_variable

# BS_Runner builder
# Path to msbuild.exe
msbuildexe_path = r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\msbuild.exe'

# Path to project file
project_path = r'BS_Runner\BS_Runner\BS_Runner.vcxproj'

# MSBuild command to run
command = [msbuildexe_path, project_path]

# Run the command and capture the output
subprocess.run(command)

# PostgreSQL installer
# Specify the download URL for the PostgreSQL installer
url = "https://get.enterprisedb.com/postgresql/postgresql-14.0-1-windows-x64.exe"

# Specify the file name to save the installer
installer_filename = "postgresql_installer.exe"

# Specify the installation directory
install_directory = "D:\\Program Files\\PostgreSQL\\14"

# Specify the password for the database user
password = "doc417"

# Download the PostgreSQL installer
response = requests.get(url)
with open(installer_filename, 'wb') as installer_file:
    installer_file.write(response.content)

# Run the installer
subprocess.run([installer_filename, "--mode", "unattended",
                "--unattendedmodeui", "minimal",
                "--superpassword", password,
                "--servicename", "PostgreSQL",
                "--datadir", os.path.join(install_directory, "data"),
                "--installdir", install_directory])

# Remove the installer file
os.remove(installer_filename)
