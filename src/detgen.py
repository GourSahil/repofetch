from pathlib import Path
import json
import argparse
import getpass

cwd = Path.cwd()
username = getpass.getuser()
metadata_path = cwd / "metadata.json"


def get_file_paths(work_dir: Path):
    work_dir = Path(work_dir)

    return [
        str(p.relative_to(work_dir))
        for p in work_dir.rglob("*")
        if p.is_file()
    ]


def main():
    parser = argparse.ArgumentParser(
        prog="config-indexer",
        description="Generate metadata for configuration folders."
    )

    parser.add_argument(
        "folder",
        help="Folder containing the configuration files"
    )

    parser.add_argument(
        "install_dir",
        help="Installation directory (example: ~/.config)"
    )

    parser.add_argument(
        "--desc",
        default="",
        help="Short description of the configuration"
    )

    args = parser.parse_args()

    folder = Path(args.folder)
    install_dir = Path(args.install_dir).expanduser()
    description = args.desc

    fpaths = get_file_paths(folder)

    if not fpaths:
        print("Nothing to process!")
        return

    data = {}

    if metadata_path.exists():
        with open(metadata_path, "r") as f:
            data = json.load(f)

    data[folder.name] = {
        "install_dir": str(install_dir),
        "description": description,
        "files": fpaths
    }

    metadata_path.write_text(json.dumps(data, indent=4))

    print(f"Metadata updated for '{folder.name}'")


if __name__ == "__main__":
    main()

