import subprocess


dependencies = ['pytube', 'pillow', 'customtkinter']  # Add your dependencies here

def install_dependency(dependency):
    try:
        subprocess.check_call(['pip', 'install', dependency])
        print(f"Successfully installed {dependency}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {dependency}")


def main():
    for dependency in dependencies:
        install_dependency(dependency)


if __name__ == "__main__":
    main()