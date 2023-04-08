import subprocess

from pathlib import Path
from typing import Any, Dict, Iterable


def main():
    logo = r""" ____  _  _        ___  __    __  __ _  __  ____       ___  _  _  ____  ____  ____  ____ 
(  _ \( \/ ) ___  / __)/  \  /  \(  / )(  )(  __)___  / __)/ )( \(_  _)(_  _)(  __)(  _ \
 ) __// \/ \(___)( (__(  O )(  O ))  (  )(  ) _)(___)( (__ ) \/ (  )(    )(   ) _)  )   /
(__)  \_)(_/      \___)\__/  \__/(__\_)(__)(____)     \___)\____/ (__)  (__) (____)(__\_)"""

    print(logo)
    project_variables = get_values()
    
    pm_cc_dir = Path(__file__).parent
    pm_cc_project_name_directory = pm_cc_dir / "project_name"
    pm_cc_src_project_name_sub_directory = pm_cc_project_name_directory / "src" / "project_name".replace("-","_")
    
    project_location = Path(project_variables["location"])
    project_location.mkdir(exist_ok=False)
    try:
        subprocess.run(["git", "init"], cwd=project_location)
    except:
        print("Git not found, skipping the initiation of a repository...")
    src_dir = project_location / "src"
    src_dir.mkdir()
    project_name_dir = src_dir / project_variables["name"]
    project_name_dir.mkdir()
    resources_dir = project_name_dir / "resources"
    resources_dir.mkdir()
    tests_dir = project_location / "tests"
    tests_dir.mkdir()
    copy_files(pm_cc_src_project_name_sub_directory, project_name_dir, ["__init__.py"])
    copy_files(pm_cc_project_name_directory, project_location, ["LICENSE", "setup.py"])
    copy_file_with_replacements(pm_cc_project_name_directory, project_location, "pyproject.toml", project_variables)
    copy_file_with_replacements(pm_cc_project_name_directory, project_location, "README.md", project_variables)



def copy_files(source_directory: Path, dest_directory: Path, file_names: Iterable[str]):
    for file_name in file_names:
        source_bytes = (source_directory / file_name).read_bytes()
        (dest_directory / file_name).write_bytes(source_bytes)

def copy_file_with_replacements(source_directory: Path, dest_directory: Path, file_name: str,  project_variables: Dict):
    source_file_path = source_directory / file_name
    source_file_text = source_file_path.read_text()

    dest_file_text = find_and_replace(source_file_text, project_variables)
    dest_file_path = dest_directory / file_name
    dest_file_path.write_text(dest_file_text)

def create_pyproject_toml(source_directory: Path, dest_directory: Path, project_variables: Dict):
    source_file_path = source_directory / "pyproject.toml"
    source_file_text = source_file_path.read_text()
    
    dest_file_text = find_and_replace(source_file_text, project_variables)
    dest_file_path = dest_directory / "pyproject.toml"
    dest_file_path.write_text(dest_file_text)

def get_values(defaults=None):
    if defaults is not None:
        user_name = defaults["author.name"]
        email = defaults["author.email"]
        project_name = get_prompt("Project name", defaults["name"])
        project_description =  get_prompt("Description", defaults["description"], allow_empty=True)
        entered_value = get_prompt("Project location",  Path(defaults["location"]).resolve())
        if Path(entered_value).is_absolute():
            project_location = Path(entered_value)
        else:
            project_location = (Path(temp_location) / Path(defaults["location"])).resolve()
        
        requires_python = get_prompt("Requires Python", defaults["requires_python"])
        home_page_url = get_prompt("Home page URL", defaults["homepage"], allow_empty=True)
        issues_url = get_prompt("Issues URL", defaults["issues"], allow_empty=True)
    else:
        user_name, email = get_user_name_and_email()
        cwd = Path()
        cwd_name = cwd.resolve().name
        project_name = get_prompt("Project name", cwd_name)
        project_description =  get_prompt("Description", allow_empty=True)
        temp_location = cwd / project_name
        entered_value = get_prompt("Project location", temp_location.resolve())
        if Path(entered_value).is_absolute():
            project_location = Path(entered_value)
        else:
            project_location = (Path(temp_location) / Path(entered_value)).resolve()
            
        requires_python = get_prompt("Requires Python", ">=3.10")
        home_page_url = get_prompt("Home page URL", allow_empty=True)
        issues_url = get_prompt("Issues URL", allow_empty=True)

    project_variables = {
        "author.name": user_name,
        "author.email": email,
        "name": project_name,
        "description": project_description,
        "location": project_location,
        "requires_python": requires_python,
        "homepage": home_page_url,
        "issues": issues_url
    }

    # Print an empty line between input collection and display to improve legibility
    print() 
    for k, v in project_variables.items():
        print(f"{k}: {v}")

    looks_ok = get_bool_prompt("\nCreate project?", True)
    
    if not looks_ok:
        print("\nNo worries, let's try again... (or press Ctrl+c to exit)")
        project_variables = get_values(defaults=project_variables)

    return project_variables


def find_and_replace(input_text: str, variable_replacements):
    output_text = input_text
    for k, v in variable_replacements.items(): 
        if k != "location":
            output_text = output_text.replace(f"<{k}>", v)
    return output_text


def get_user_name_and_email():
    try:
        git_data = subprocess.check_output(["git", "config", "--global", "--list"]).decode().strip().split("\n")
        git = {}
        for item in git_data:
            k, v = item.split("=")
            git[k.lower()] = v.strip()
        user_name = git['user.name']
        email = git["user.email"]
    except FileNotFoundError:
        user_name = get_prompt("User name (e.g. github username)")
        email = get_prompt(f"Email")
    finally:
        return user_name, email

def get_prompt(prompt: str, default_value: Any = "", allow_empty: bool =False) -> Any:
    val = input(f"{prompt} [{default_value}]: ")
    if val.strip() == "":
        if allow_empty:
            if default_value:
                return default_value
            return ""
        if default_value:
            return default_value
        while val.strip() == "":
            val = input(f"{prompt} [{default_value}]: ")
    return val.strip()

def get_bool_prompt(prompt: str, default_value: bool=False) -> Any:
    trans = {
        "y": True,
        "n": False,
        "": default_value
    }
    val = input(f"{prompt} [{'Y' if default_value else 'N'}]: ")
    val = val.strip().lower()

    while val not in trans:
        val = input(f"{prompt} [{'Y' if default_value else 'N'}]: ")
    return trans[val]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()