#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys


def parse_cmake_cache(build_dir):
    cmake_cache = os.path.join(build_dir, "CMakeCache.txt")
    if not os.path.exists(cmake_cache):
        return None, None

    nuttx_dir = None
    build_abs = None

    with open(cmake_cache, "r") as f:
        for line in f:
            if line.startswith("NuttX_SOURCE_DIR:STATIC="):
                nuttx_dir = line.split("=", 1)[1].strip()
            elif line.startswith("NuttX_BINARY_DIR:STATIC="):
                build_abs = line.split("=", 1)[1].strip()

    return nuttx_dir, build_abs


def extract_apps_dir_from_kconfig(build_dir):
    apps_kconfig = os.path.join(build_dir, "nuttx-apps", "Kconfig")
    if not os.path.exists(apps_kconfig):
        return None

    with open(apps_kconfig, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith('source "'):
                source_path = line[8:-1]
                if "build/nuttx-apps" not in source_path:
                    apps_dir = os.path.dirname(source_path)
                    if os.path.basename(apps_dir) == "nuttx-apps":
                        return apps_dir

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Kconfig configuration modification tool (wrapper around kconfiglib setconfig)"
    )

    parser.add_argument(
        "--file",
        default=".config",
        help="Configuration file to modify (default: .config)",
    )

    parser.add_argument(
        "--nuttx-dir",
        default="nuttx",
        help="NuttX source directory (default: nuttx)",
    )

    parser.add_argument(
        "--apps-dir",
        default="nuttx-apps",
        help="NuttX Apps directory (default: nuttx-apps)",
    )

    parser.add_argument(
        "--build-dir",
        default="build",
        help="Build directory (default: build)",
    )

    action_group = parser.add_argument_group("actions")

    action_group.add_argument(
        "--enable",
        metavar="SYMBOL",
        action="append",
        help="Enable a configuration option (set to y)",
    )

    action_group.add_argument(
        "--disable",
        metavar="SYMBOL",
        action="append",
        help="Disable a configuration option (set to n)",
    )

    action_group.add_argument(
        "--set",
        metavar="SYMBOL=VALUE",
        action="append",
        help="Set a configuration option to a specific value (for int, hex, string types)",
    )

    action_group.add_argument(
        "--set-str",
        nargs=2,
        action="append",
        help='Set a string configuration option (e.g., --set-str CONFIG_SYSTEM_HOSTNAME "myboard")',
    )

    action_group.add_argument(
        "--set-val",
        nargs=2,
        action="append",
        help="Set a numeric configuration option (e.g., --set-val CONFIG_IDLETHREAD_STACKSIZE 2048)",
    )

    args = parser.parse_args()

    if not (args.enable or args.disable or args.set or args.set_str or args.set_val):
        parser.error(
            "at least one action required: --enable, --disable, --set, --set-str, or --set-val"
        )

    config_path = args.file

    if config_path == ".config":
        config_path = None
        for candidate in [".config", "build/.config", "nuttx/.config"]:
            if os.path.exists(candidate):
                config_path = candidate
                break

        if not config_path:
            sys.exit(
                "error: .config file not found in current directory or build/ subdirectory"
            )

    config_path = os.path.abspath(config_path)
    config_dir = os.path.dirname(config_path)

    if args.nuttx_dir == "nuttx" and args.build_dir == "build":
        build_dir = config_dir

        nuttx_dir = None
        apps_dir = None

        cmake_nuttx, cmake_build = parse_cmake_cache(build_dir)
        if cmake_nuttx and cmake_build:
            nuttx_dir = cmake_nuttx
            build_dir = cmake_build
            apps_dir = extract_apps_dir_from_kconfig(build_dir)

        if not nuttx_dir:
            search_dir = config_dir
            while search_dir != "/":
                candidate_nuttx = os.path.join(search_dir, "nuttx")
                if os.path.exists(os.path.join(candidate_nuttx, "Kconfig")):
                    nuttx_dir = candidate_nuttx
                    candidate_apps = os.path.join(search_dir, "nuttx-apps")
                    if os.path.exists(candidate_apps):
                        apps_dir = candidate_apps
                    break
                search_dir = os.path.dirname(search_dir)

        if not nuttx_dir:
            sys.exit(
                "error: could not find nuttx directory (searched from config path)"
            )
    else:
        nuttx_dir = args.nuttx_dir
        apps_dir = args.apps_dir
        build_dir = args.build_dir

    nuttx_dir = os.path.abspath(nuttx_dir)
    apps_dir = os.path.abspath(apps_dir) if apps_dir else None
    build_dir = os.path.abspath(build_dir)

    if not os.path.exists(config_path):
        sys.exit(f"error: config file '{config_path}' does not exist")

    if not os.path.exists(nuttx_dir):
        sys.exit(f"error: nuttx directory '{nuttx_dir}' does not exist")

    if apps_dir and not os.path.exists(apps_dir):
        sys.exit(f"error: apps directory '{apps_dir}' does not exist")

    if not os.path.exists(build_dir):
        sys.exit(f"error: build directory '{build_dir}' does not exist")

    env = os.environ.copy()
    env["KCONFIG_CONFIG"] = config_path
    env["srctree"] = nuttx_dir
    env["BINDIR"] = build_dir
    env["APPSBINDIR"] = os.path.join(build_dir, "nuttx-apps")
    env["APPSDIR"] = apps_dir

    if not apps_dir:
        apps_dir = os.path.join(nuttx_dir, "../nuttx-apps")
        if os.path.exists(apps_dir):
            env["APPSDIR"] = os.path.abspath(apps_dir)
        else:
            for search_dir in [os.path.dirname(nuttx_dir), nuttx_dir]:
                candidate = os.path.join(search_dir, "nuttx-apps")
                if os.path.exists(candidate):
                    env["APPSDIR"] = os.path.abspath(candidate)
                    break

    external_dir = env.get("APPSDIR", "")
    external_dir = os.path.join(external_dir, "external")
    if os.path.exists(external_dir):
        external_kconfig = os.path.join(external_dir, "Kconfig")
        if not os.path.exists(external_kconfig):
            try:
                with open(external_kconfig, "w") as f:
                    pass
                os.makedirs(external_dir, exist_ok=True)
            except:
                pass
        if os.path.exists(external_kconfig):
            env["EXTERNALDIR"] = external_dir

    cmd = [
        "setconfig",
        "--kconfig",
        "Kconfig",
        "--no-check-exists",
        "--no-check-value",
    ]

    if args.enable:
        for symbol_name in args.enable:
            if symbol_name.startswith("CONFIG_"):
                symbol_name = symbol_name[7:]
            cmd.append(f"{symbol_name}=y")

    if args.disable:
        for symbol_name in args.disable:
            if symbol_name.startswith("CONFIG_"):
                symbol_name = symbol_name[7:]
            cmd.append(f"{symbol_name}=n")

    if args.set:
        for assignment in args.set:
            if "=" not in assignment:
                sys.exit(
                    f"error: invalid assignment '{assignment}', expected SYMBOL=VALUE format"
                )
            symbol_name, value = assignment.split("=", 1)
            if symbol_name.startswith("CONFIG_"):
                symbol_name = symbol_name[7:]
            cmd.append(f"{symbol_name}={value}")

    if args.set_str:
        for symbol_name, value in args.set_str:
            if symbol_name.startswith("CONFIG_"):
                symbol_name = symbol_name[7:]
            cmd.append(f"{symbol_name}={value}")

    if args.set_val:
        for symbol_name, value in args.set_val:
            if symbol_name.startswith("CONFIG_"):
                symbol_name = symbol_name[7:]
            cmd.append(f"{symbol_name}={value}")

    try:
        result = subprocess.run(
            cmd,
            env=env,
            cwd=nuttx_dir,
            capture_output=True,
            text=True,
        )

        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)

        if result.returncode == 0:
            if result.stdout:
                print(result.stdout.strip())
            sys.exit(0)
        else:
            if result.stdout:
                print(result.stdout.strip())
            sys.exit(result.returncode)
    except FileNotFoundError:
        sys.exit(
            "error: 'setconfig' command not found. Install kconfiglib: pip install kconfiglib"
        )


if __name__ == "__main__":
    main()
