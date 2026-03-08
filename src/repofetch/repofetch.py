from pathlib import Path
import argparse
import json
import requests
import shutil

OWNER = "GourSahil"
REPO = "repofetch"
BRANCH = "main"

API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
RAW_BASE = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}"


def gh_list(path):
    r = requests.get(f"{API_BASE}/{path}")
    r.raise_for_status()
    return r.json()


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

            metadata_url = f"{RAW_BASE}/index/{category}/{app['name']}/metadata.json"

            try:
                meta = requests.get(metadata_url).json()
            except:
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
# Search
# ----------------------------
def search_apps(query):
    apps = discover_apps()

    for app in apps:
        for version, info in app["metadata"].items():
            desc = info.get("description", "")

            if query.lower() in app["name"].lower() or query.lower() in desc.lower():
                print(f"{app['name']}:{version} - {desc}")


# ----------------------------
# Download file
# ----------------------------
def download(url, target):
    r = requests.get(url, stream=True)
    r.raise_for_status()

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "wb") as f:
        shutil.copyfileobj(r.raw, f)


# ----------------------------
# Install
# ----------------------------
def install_app(name, version):
    apps = discover_apps()

    for app in apps:
        if app["name"] != name:
            continue

        meta = app["metadata"]

        if version not in meta:
            print("Version not found")
            return

        install_dir = Path.home() / meta[version]["install_dir"]

        print(install_dir)
        version_path = f"{app['path']}/{version}"

        files = gh_list(version_path)

        print(f"Installing {name}:{version}")

        for f in files:
            if f["type"] == "file":
                target = install_dir / f["name"]
                download(f["download_url"], target)

        print("Install complete")
        return

    print("Application not found")


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
