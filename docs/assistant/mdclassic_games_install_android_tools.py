"""Install the reviewed Linux x64 Android tools in a user-owned directory.

Run from repository root with:
    uv run --locked --group android python docs/assistant/mdclassic_games_install_android_tools.py

This provisions archives only. SDK license acceptance and OS prerequisites are
separate steps. It does not change shell profiles or the system Java selection.
"""

import argparse
import hashlib
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request


GOOGLE = "https://dl.google.com/android/repository/"
ARCHIVES = [
    (
        "https://github.com/adoptium/temurin17-binaries/releases/download/"
        "jdk-17.0.20.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.20.1_1.tar.gz",
        "sha256", "3808d1d15e3ec6bd5b84057fb5d84c33d8a1536a258146bcea2e603fc726e08e",
        "jdk-17.0.20.1+1",
    ),
    (
        GOOGLE + "commandlinetools-linux-13114758_latest.zip",
        "sha1", "5fdcc763663eefb86a5b8879697aa6088b041e70", "sdk/cmdline-tools/19.0",
    ),
    (
        GOOGLE + "platform-tools_r37.0.1-linux.zip",
        "sha1", "477254aa5f903c15cf51001717bdf347fb6b53e0", "sdk/platform-tools",
    ),
    (
        GOOGLE + "build-tools_r36_linux.zip",
        "sha1", "b0b6376977657e8ad9b969bacf4093601da2c6fb", "sdk/build-tools/36.0.0",
    ),
    (
        GOOGLE + "platform-36_r02.zip",
        "sha1", "2c1a80dd4d9f7d0e6dd336ec603d9b5c55a6f576", "sdk/platforms/android-36",
    ),
    (
        GOOGLE + "android-ndk-r28c-linux.zip",
        "sha1", "a7b54a5de87fecd125a17d54f73c446199e72a64", "android-ndk-r28c",
    ),
]


def digest(path, algorithm):
    result = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def install(base, url, algorithm, expected, relative):
    target = base / relative
    marker = target / ".classic-games-archive-checksum"
    identity = f"{algorithm}:{expected}\n{url}\n"
    if target.exists() or target.is_symlink():
        if marker.is_file() and marker.read_text() == identity:
            print(f"Already provisioned: {target}", flush=True)
            return
        raise RuntimeError(f"Existing directory has no matching archive record: {target}")

    downloads = base / "downloads"
    downloads.mkdir(exist_ok=True)
    archive = downloads / url.rsplit("/", 1)[1]
    if not archive.is_file() or digest(archive, algorithm) != expected:
        partial = archive.with_name(archive.name + ".partial")
        print(f"Downloading {url}", flush=True)
        with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as stream:
            shutil.copyfileobj(response, stream, length=1024 * 1024)
        if digest(partial, algorithm) != expected:
            raise RuntimeError(f"Archive checksum mismatch: {partial}")
        partial.replace(archive)
    print(f"Verified {algorithm}: {archive.name}", flush=True)

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".install-", dir=base) as temporary:
        staging = Path(temporary)
        if archive.name.endswith(".tar.gz"):
            with tarfile.open(archive) as bundle:
                bundle.extractall(staging, filter="data")
        else:
            # unzip preserves Unix executable bits and the NDK's symlinks.
            subprocess.run(["unzip", "-q", str(archive), "-d", str(staging)], check=True)
        entries = list(staging.iterdir())
        if len(entries) != 1 or not entries[0].is_dir():
            raise RuntimeError(f"Expected one top-level archive directory: {archive}")
        (entries[0] / marker.name).write_text(identity)
        entries[0].rename(target)
    print(f"Installed {target}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path,
        default=Path.home() / ".local/share/classic-games-android",
        help="User-owned tool directory (default: ~/.local/share/classic-games-android)",
    )
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        parser.error("These reviewed archives require a Linux x86_64 host")
    if shutil.which("unzip") is None:
        parser.error("Install the OS unzip prerequisite first")
    base = args.root.expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)
    for archive in ARCHIVES:
        install(base, *archive)
    tools = base / "sdk/tools"
    if tools.is_symlink():
        if tools.resolve() != base / "sdk/cmdline-tools/19.0":
            raise RuntimeError(f"Existing tools symlink points elsewhere: {tools}")
        # A directory symlink makes sdkmanager discover the package twice.
        # Replace only the symlink created by this installer's earlier layout.
        tools.unlink()
    legacy_bin = tools / "bin"
    legacy_bin.mkdir(parents=True, exist_ok=True)
    # Buildozer 1.6.0 expects sdk/tools/bin/sdkmanager, and p4a's API check calls
    # sdk/tools/bin/avdmanager; expose both without duplicating SDK metadata.
    for name in ("sdkmanager", "avdmanager"):
        launcher = legacy_bin / name
        content = (
            '#!/bin/sh\n'
            f'exec "$(dirname "$0")/../../cmdline-tools/19.0/bin/{name}" "$@"\n'
        )
        if launcher.exists() and launcher.read_text() != content:
            raise RuntimeError(f"Existing SDK launcher cannot be replaced: {launcher}")
        launcher.write_text(content)
        launcher.chmod(0o755)
    print(f"Provisioning complete. SDK root: {base / 'sdk'}", flush=True)
    print("Review/accept SDK licenses with sdk/tools/bin/sdkmanager --licenses.", flush=True)


if __name__ == "__main__":
    main()
