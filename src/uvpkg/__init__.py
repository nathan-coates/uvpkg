from argparse import ArgumentParser
from dataclasses import dataclass
from json import dump as json_dump
from json import load as json_load
from os import makedirs
from os import path as os_path

from plumbum import local


@dataclass
class Config:
    programming_dir: str


def get_application_support_dir(app_name: str) -> str:
    # Get the home directory
    home_dir = os_path.expanduser("~")

    if app_name.strip() == "":
        raise ValueError("Application name must not be empty.")

    # Create the Application Support path using macOS recommended structure
    app_support_path = os_path.join(
        home_dir, "Library", "Application Support", app_name
    )

    # Create the directory if it doesn't exist
    makedirs(app_support_path, exist_ok=True)

    return app_support_path


def get_programming_dir(path: str) -> Config:
    config_path = os_path.join(path, "config.json")

    # Check if config file exists
    if os_path.exists(config_path):
        # Load existing config
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json_load(f)

        # Convert to Config object
        return Config(programming_dir=config_data.get("programming_dir", ""))

    # Config file doesn't exist, create it and prompt user
    print("Config file not found. Creating new config.")
    print("Please enter the programming directory path:")

    # Get user input (fallback to current directory if empty)
    programming_dir = input("> ").strip()
    if not programming_dir:
        raise ValueError("Programming directory path cannot be empty.")

    # Create the config file
    config_data = {"programming_dir": programming_dir}

    with open(config_path, "w", encoding="utf-8") as f:
        json_dump(config_data, f, indent=4, ensure_ascii=False)

    # Return the new Config object
    return Config(programming_dir=programming_dir)


def get_package_name_from_args():
    parser = ArgumentParser(
        description="Build a uv package starter with the specified name."
    )

    # Add a required argument for package name
    parser.add_argument(
        "package_name", type=str, help="The name of the package to build"
    )

    # Parse the arguments
    args = parser.parse_args()

    return args.package_name


def check_uv_installed() -> bool:
    try:
        local["uv"]
        return True
    except Exception:
        return False


def pkg_exists(programming_dir: str, package_name: str) -> bool:
    package_path = os_path.join(programming_dir, package_name)
    return os_path.exists(package_path)


def run_uv(programming_dir: str, package_name: str) -> None:
    uv_executable = local["uv"]

    with local.cwd(programming_dir):
        uv_executable["init", "--package", package_name]()


def main() -> None:
    package_name = get_package_name_from_args()

    if not check_uv_installed():
        print("Error: 'uv' command-line tool is not installed or not found in PATH.")
        return

    app_support_dir = get_application_support_dir("uvpkg")
    config = get_programming_dir(app_support_dir)

    if pkg_exists(config.programming_dir, package_name):
        print(
            f"Error: Package '{package_name}' already exists in '{config.programming_dir}'."
        )
        return

    run_uv(config.programming_dir, package_name)
