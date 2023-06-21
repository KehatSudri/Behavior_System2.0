import os
import sys
import urllib.request
import subprocess
import requests

# Check if MSBuild is installed
msbuild_installed = os.path.exists(
    r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\msbuild.exe")

if not msbuild_installed:
    print("MSBuild not found. Installing MSBuild...")

    # Download MSBuild with VC Build Tools
    print("Downloading MSBuild with VC Build Tools...")
    url = 'https://aka.ms/vs/17/release/vs_buildtools.exe'
    file_name = 'vs_buildtools.exe'
    urllib.request.urlretrieve(url, file_name)

    # Install MSBuild with VC Build Tools
    print("Installing MSBuild with VC Build Tools...")
    subprocess.run(
        [file_name, '--quiet', '--add', 'Microsoft.VisualStudio.Workload.VCTools', '--includeRecommended', '--wait'],
        check=True)

    # Clean up downloaded file
    print("Cleaning up downloaded file...")
    os.remove(file_name)
else:
    print("MSBuild is already installed.")

# Check if BS_Runner is built
bs_runner_path = r'BS_Runner\BS_Runner\BS_Runner.exe'

if not os.path.exists(bs_runner_path):
    print("BS_Runner not built. Building BS_Runner...")

    # Path to msbuild.exe
    msbuildexe_path = r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\msbuild.exe'

    # Path to project file
    project_path = r'BS_Runner\BS_Runner\BS_Runner.vcxproj'

    # MSBuild command to run
    command = [msbuildexe_path, project_path]

    # Run the command and capture the output
    print("Running MSBuild command...")
    subprocess.run(command)
else:
    print("BS_Runner is already built.")

# Check if PostgreSQL is installed
postgresql_installed = os.path.exists(r"C:\Program Files\PostgreSQL\15")

if not postgresql_installed:
    print("PostgreSQL not found. Installing PostgreSQL...")

    # Specify the download URL for the PostgreSQL installer
    url = "https://get.enterprisedb.com/postgresql/postgresql-15.0-1-windows-x64.exe"

    # Specify the file name to save the installer
    installer_filename = "postgresql_installer.exe"

    # Specify the installation directory
    install_directory = "C:\\Program Files\\PostgreSQL\\15"

    # Specify the password for the database user
    password = "doc417"

    # Download the PostgreSQL installer
    print("Downloading PostgreSQL installer...")
    response = requests.get(url)
    with open(installer_filename, 'wb') as installer_file:
        installer_file.write(response.content)

    # Run the installer
    print("Running the PostgreSQL installer...")
    subprocess.run([installer_filename, "--mode", "unattended",
                    "--unattendedmodeui", "minimal",
                    "--superpassword", password,
                    "--servicename", "PostgreSQL",
                    "--datadir", os.path.join(install_directory, "data"),
                    "--installdir", install_directory])

    # Remove the installer file
    print("Cleaning up PostgreSQL installer file...")
    os.remove(installer_filename)
else:
    print("PostgreSQL is already installed.")


def is_module_installed(module_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", module_name], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


# Check if PyInstaller is installed
if not is_module_installed("pyinstaller"):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {e}")
        exit(1)
else:
    print("PyInstaller is already installed.")

spec_file = 'project.spec'

# Run PyInstaller with the .spec file
try:
    subprocess.run(['pyinstaller', '--onefile', spec_file], check=True)
    print("PyInstaller completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"PyInstaller exited with an error status: {e}")

print("Installation completed successfully.")
