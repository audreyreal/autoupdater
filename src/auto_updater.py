# MIT License
#
# Copyright (c) 2022 sweeze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A module for checking for updates to a github repo."""

from json import loads as parse
from sys import platform
import requests
from requests.models import Response
from packaging.version import parse as version_parse

request = lambda url: requests.get(
    url, headers={"User-Agent": "Python Auto Updater, developed by @sw33ze"}, timeout=10
)


def get_latest_release(author: str, repo_name: str) -> dict | None:
    """Takes the author and repo name and returns a dictionary of the latest release generated from the github api.

    Args:
        author (str): Author of the repo. e.g. "sw33ze" in "sw33ze/swarm"
        repo_name (str): Name of the repo. e.g. "swarm" in "sw33ze/swarm"

    Returns:
        dict: Dict containing keys "latest_release", "windows_release", "mac_release", "linux_release"
    """
    response: Response = request(
        f"https://api.github.com/repos/{author}/{repo_name}/releases/latest"
    )
    return parse(response.text)


def check_for_update(data: dict, current_version: str) -> bool:
    """Takes the author, repo name and current version and checks if there is a new version available.

    Args:
        data (dict): parsed json object from the github /repos/{author}/{repo_name}/releases/latest endpoint.
        current_version (str): Current version of the program to check for updates against.

    Returns:
        bool: True if there is a new version available, False otherwise.
    """
    latest_version: str = data["tag_name"].replace("v", "")

    return version_parse(latest_version) > version_parse(current_version)



def get_release_urls(data: dict) -> dict:
    """Takes the data (response.text from github api) and returns a dict containing the urls for the latest release.

    Args:
        data (dict): parsed json object from the github /repos/{author}/{repo_name}/releases/latest endpoint.

    Returns:
        dict: Contains the keys "windows", "linux", and "mac" depending on the platforms published.
    """
    releases: list = data["assets"]
    urls = [release["browser_download_url"] for release in releases]
    releases = {}
    for url in urls:
        if ".exe" in url.lower():
            releases["windows"] = url
        elif any(ext in url.lower() for ext in [".dmg", ".intel", "macos", "osx"]):
            releases["mac"] = url
        else:
            releases["linux"] = url
    return releases


def download_release(releases: dict) -> None:
    """Gets the release for your platform and downloads it.

    Args:
        releases (dict): Dictionary containing keys "windows", "linux", and "mac" depending on the platforms published, and values are the download urls for the release.
    """
    try:
        match platform:
            case "win32":
                url = releases["windows"]
            case "darwin":
                url = releases["mac"]
            case "linux":
                url = releases["linux"]
            case _:
                raise Exception("Unsupported platform")
    except:
        raise Exception("No release available for your platform")
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as f:
        f.write(request(url).content)


def get_release(releases: dict) -> str:
    """Gets the release for your platform and returns it.

    Args:
        releases (dict): Dictionary containing keys "windows", "linux", and "mac" depending on the platforms published, and values are the download urls for the release.

    Returns:
        str: String containing the github release url for the release of your platform.
    """
    try:
        match platform:
            case "win32":
                url = releases["windows"]
            case "darwin":
                url = releases["mac"]
            case "linux":
                url = releases["linux"]
            case _:
                raise Exception("Unsupported platform")
    except:
        raise Exception("No release available for your platform")
    return url