from pathlib import Path
import argparse
import requests
import shutil
import sys

OWNER = "GourSahil"
REPO = "repofetch"
BRANCH = "main"

API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"


# ----------------------------
# GitHub directory listing
# ----------------------------
def gh_list(path):
    try:
        r = requests.get(f"{API_BASE}/{path}", timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Failed to list GitHub path: {path}")
        print(e)
        sys.exit(1)


# ----------------------------
# Download file
# ----------------------------
def download(url, target):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()

        target.parent.mkdir(parents=True, exist_ok=True)

        with open(target, "wb") as f:
            f.write(r.content)

    except Exception as e:
        print(f"[ERROR] Failed downloading {url}")
        print(e)
        sys.exit(1)


# ----------------------------
# Recursive downloader
# ----------------------------
def download_tree(repo_path, install_root, base_path):

    items = gh_list(repo_path)

    for item in items:

        if item["type"] == "file":

            raw_url = item.get("download_url")

            if not raw_url:
                print(f"[ERROR] No download URL for {item['path']}")
                sys.exit(1)

            rel_path = Path(item["path"]).relative_to(base_path)
            target = install_root / rel_path

            print(f"Downloading {rel_path}")

            download(raw_url, target)

        elif item["type"] == "dir":

            download_tree(item["path"], install_root, base_path)


# ----------------------------
# Discover apps
# ----------------------------
def discover_apps():

    apps = []

    categories = gh_list("index")

    for cat in categories:

        if cat["type"] != "dir":
            continue

        category = cat["name"]

        apps_dir = gh_list(f"index/{category}")

        for app in apps_dir:

            if app["type"] != "dir":
                continue

            metadata_url = (
                f"https://raw.githubusercontent.com/"
                f"{OWNER}/{REPO}/{BRANCH}/index/{category}/{app['name']}/metadata.json"
            )

            try:
                meta = requests.get(metadata_url, timeout=15).json()
            except Exception:
                continue

            apps.append({
                "name": app["name"],
                "category": category,
                "metadata": meta,
                "path": f"index/{category}/{app['name']}"
            })

    return apps


# ----------------------------
# List apps
# ----------------------------
def list_apps():

    apps = discover_apps()

    for app in apps:

        print(f"\n{app['name']} ({app['category']})")

        for version, info in app["metadata"].items():

            desc = info.get("description", "")
            print(f"  {version} → {desc}")


# ----------------------------
# Search apps
# ----------------------------
def search_apps(query):

    apps = discover_apps()

    for app in apps:

        for version, info in app["metadata"].items():

            desc = info.get("description", "")

            if query.lower() in app["name"].lower() or query.lower() in desc.lower():

                print(f"{app['name']}:{version} - {desc}")


# ----------------------------
# Clean installation directory
# ----------------------------
def clean_install_dir(path):

    if path.exists():

        print(f"Cleaning {path}")

        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"[ERROR] Failed cleaning directory {path}")
            print(e)
            sys.exit(1)

    path.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Install application
# ----------------------------
def install_app(name, version):

    apps = discover_apps()

    for app in apps:

        if app["name"] != name:
            continue

        meta = app["metadata"]

        if version not in meta:
            print("Version not found")
            sys.exit(1)

        install_dir = Path(meta[version]["install_dir"])

        if not install_dir.is_absolute():
            install_dir = Path.home() / install_dir

        print(f"Install path: {install_dir}")

        clean_install_dir(install_dir)

        version_path = f"{app['path']}/{version}"

        print(f"Installing {name}:{version}")

        download_tree(version_path, install_dir, version_path)

        print("Install complete")
        return

    print("Application not found")
    sys.exit(1)


# ----------------------------
# CLI
# ----------------------------
parser = argparse.ArgumentParser(prog="repofetch")

sub = parser.add_subparsers(dest="command")

sub.add_parser("list")

search_cmd = sub.add_parser("search")
search_cmd.add_argument("query")

install_cmd = sub.add_parser("install")
install_cmd.add_argument("name")
install_cmd.add_argument("version")

args = parser.parse_args()

if args.command == "list":
    list_apps()

elif args.command == "search":
    search_apps(args.query)

elif args.command == "install":
    install_app(args.name, args.version)

else:
    parser.print_help()
