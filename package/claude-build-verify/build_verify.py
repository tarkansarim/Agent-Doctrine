#!/usr/bin/env python3
"""
PostToolUse hook: Build verification after C++/CUDA file edits.

Preset-aware — reads per-repo config or detects valid CMake presets before
invoking the build so it never false-fails on repos where 'build' is not a
valid preset.

Per-repo config: create <project-root>/.agent-build-verify.json:
  {
    "command": ["bash", "scripts/build.sh", "qt-shell"],
    "timeout": 600
  }

Exit codes:
  0 = success (build passed, file not C++/CUDA, or no valid build route known)
  2 = BLOCK (build failed — stderr fed back to Claude)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


CPP_CUDA_EXTENSIONS = {'.cu', '.cpp', '.h', '.cuh', '.hpp', '.cc', '.cxx', '.hxx'}
CMAKE_FILES = {'CMakeLists.txt', 'CMakePresets.json'}

# Default build timeout; overridden by per-repo config
DEFAULT_BUILD_TIMEOUT = 600

# Filename for per-repo build configuration
REPO_CONFIG_FILENAME = '.agent-build-verify.json'


def get_file_path(tool_input: dict) -> str:
    return tool_input.get('file_path', tool_input.get('path', ''))


def is_cpp_cuda_file(file_path: str) -> bool:
    if not file_path:
        return False
    basename = os.path.basename(file_path)
    if basename in CMAKE_FILES:
        return True
    _, ext = os.path.splitext(file_path)
    return ext.lower() in CPP_CUDA_EXTENSIONS


def find_project_root(file_path: str) -> str | None:
    directory = os.path.dirname(os.path.abspath(file_path))
    for _ in range(20):
        if (os.path.exists(os.path.join(directory, 'CMakeLists.txt')) or
                os.path.exists(os.path.join(directory, 'Makefile')) or
                os.path.exists(os.path.join(directory, 'scripts', 'build.bat')) or
                os.path.exists(os.path.join(directory, 'scripts', 'build.sh'))):
            return directory
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent
    return None


def load_repo_config(project_root: str) -> dict | None:
    """Load per-repo build config from .agent-build-verify.json, or None."""
    config_path = os.path.join(project_root, REPO_CONFIG_FILENAME)
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, encoding='utf-8') as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


def cmake_preset_names(project_root: str) -> set[str] | None:
    """
    Return the set of configure-preset names from CMakePresets.json, or None
    if no CMakePresets.json exists.
    """
    presets_path = os.path.join(project_root, 'CMakePresets.json')
    if not os.path.exists(presets_path):
        return None
    try:
        with open(presets_path, encoding='utf-8') as fh:
            data = json.load(fh)
        names: set[str] = set()
        for preset in data.get('configurePresets', []):
            if isinstance(preset, dict) and isinstance(preset.get('name'), str):
                names.add(preset['name'])
        for preset in data.get('buildPresets', []):
            if isinstance(preset, dict) and isinstance(preset.get('name'), str):
                names.add(preset['name'])
        return names
    except (json.JSONDecodeError, OSError):
        return None


def find_build_command(project_root: str) -> tuple[list[str] | None, int, str]:
    """
    Return (cmd, timeout_seconds, skip_reason).

    skip_reason is non-empty and cmd is None when no valid build route is
    known — the hook exits 0 with the reason printed so the worker can see it.
    """
    # Per-repo config takes absolute priority.
    repo_config = load_repo_config(project_root)
    if repo_config is not None:
        cmd = repo_config.get('command')
        timeout = repo_config.get('timeout', DEFAULT_BUILD_TIMEOUT)
        if isinstance(cmd, list) and cmd and all(isinstance(c, str) for c in cmd):
            return cmd, int(timeout), ''
        return None, DEFAULT_BUILD_TIMEOUT, (
            f'invalid .agent-build-verify.json in {project_root}; '
            'expected {"command": [...], "timeout": N}'
        )

    build_sh = os.path.join(project_root, 'scripts', 'build.sh')
    if os.path.exists(build_sh):
        presets = cmake_preset_names(project_root)
        if presets is None:
            # No CMakePresets.json — call build.sh with no preset argument.
            return ['bash', build_sh], DEFAULT_BUILD_TIMEOUT, ''
        if 'build' in presets:
            return ['bash', build_sh, 'build'], DEFAULT_BUILD_TIMEOUT, ''
        # CMakePresets.json exists but 'build' is not a valid preset.
        return None, DEFAULT_BUILD_TIMEOUT, (
            f'No "build" preset in CMakePresets.json for {project_root}; '
            f'available: {", ".join(sorted(presets)) or "(none)"}. '
            f'Create {REPO_CONFIG_FILENAME} to configure the build command.'
        )

    cmake_lists = os.path.join(project_root, 'CMakeLists.txt')
    build_dir = os.path.join(project_root, 'build')
    if os.path.exists(cmake_lists):
        if os.path.exists(build_dir):
            return ['cmake', '--build', build_dir, '--config', 'Release'], DEFAULT_BUILD_TIMEOUT, ''
        return None, DEFAULT_BUILD_TIMEOUT, 'CMake build directory not found; skipping build check'

    if os.path.exists(os.path.join(project_root, 'Makefile')):
        return ['make', '-j4'], DEFAULT_BUILD_TIMEOUT, ''

    return None, DEFAULT_BUILD_TIMEOUT, ''


def run_build(project_root: str, build_cmd: list[str], timeout: int) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            build_cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        if len(output) > 500:
            output = '...' + output[-500:]
        if result.returncode != 0:
            return False, output
        return True, 'Build passed'
    except subprocess.TimeoutExpired:
        return False, f'Build timed out after {timeout}s'
    except Exception as exc:
        # Non-fatal — infrastructure errors must not block the worker.
        return True, f'Build check skipped: {exc}'


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})

    if tool_name not in ('Write', 'Edit'):
        sys.exit(0)

    file_path = get_file_path(tool_input)
    if not is_cpp_cuda_file(file_path):
        sys.exit(0)

    project_root = find_project_root(file_path)
    if not project_root:
        sys.exit(0)

    build_cmd, timeout, skip_reason = find_build_command(project_root)
    if build_cmd is None:
        if skip_reason:
            print(f'Build check skipped: {skip_reason}')
        sys.exit(0)

    success, output = run_build(project_root, build_cmd, timeout)
    if success:
        print(f'Build verified after editing {os.path.basename(file_path)}')
        sys.exit(0)

    print(
        f'BUILD FAILED after editing {os.path.basename(file_path)}. '
        f'UNDO your change immediately and fix the compilation error.\n\n'
        f'Build output:\n{output}',
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == '__main__':
    main()
