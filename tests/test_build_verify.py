from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_SOURCE = REPO_ROOT / "package" / "claude-build-verify" / "build_verify.py"
sys.path.insert(0, str(REPO_ROOT / "package" / "claude-build-verify"))

from build_verify import (
    cmake_preset_names,
    find_build_command,
    find_project_root,
    is_cpp_cuda_file,
    load_repo_config,
    REPO_CONFIG_FILENAME,
    DEFAULT_BUILD_TIMEOUT,
)


def run_hook(hook_input: dict, project_dir: str | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    return subprocess.run(
        [sys.executable, str(HOOK_SOURCE)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        cwd=project_dir or os.getcwd(),
        env=env,
    )


class TestIsCppCudaFile(unittest.TestCase):
    def test_cpp_extensions(self):
        for ext in ('.cpp', '.h', '.hpp', '.cc', '.cxx', '.hxx', '.cu', '.cuh'):
            self.assertTrue(is_cpp_cuda_file(f'/some/path/file{ext}'), ext)

    def test_cmake_files(self):
        self.assertTrue(is_cpp_cuda_file('/repo/CMakeLists.txt'))
        self.assertTrue(is_cpp_cuda_file('/repo/CMakePresets.json'))

    def test_non_cpp(self):
        self.assertFalse(is_cpp_cuda_file('/repo/main.py'))
        self.assertFalse(is_cpp_cuda_file('/repo/README.md'))
        self.assertFalse(is_cpp_cuda_file(''))


class TestLoadRepoConfig(unittest.TestCase):
    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = {'command': ['bash', 'scripts/build.sh', 'qt-shell'], 'timeout': 300}
            Path(tmp, REPO_CONFIG_FILENAME).write_text(json.dumps(config))
            result = load_repo_config(tmp)
            self.assertEqual(result, config)

    def test_missing_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_repo_config(tmp))

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, REPO_CONFIG_FILENAME).write_text('not json')
            self.assertIsNone(load_repo_config(tmp))


class TestCmakePresetNames(unittest.TestCase):
    def test_no_presets_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(cmake_preset_names(tmp))

    def test_presets_with_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                'configurePresets': [{'name': 'build'}, {'name': 'dev'}],
            }
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            names = cmake_preset_names(tmp)
            self.assertIn('build', names)
            self.assertIn('dev', names)

    def test_presets_without_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                'configurePresets': [{'name': 'dev'}, {'name': 'qt-shell'}, {'name': 'no-ngx'}],
            }
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            names = cmake_preset_names(tmp)
            self.assertNotIn('build', names)
            self.assertIn('qt-shell', names)

    def test_build_presets_also_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                'configurePresets': [{'name': 'dev'}],
                'buildPresets': [{'name': 'release'}],
            }
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            names = cmake_preset_names(tmp)
            self.assertIn('dev', names)
            self.assertIn('release', names)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'CMakePresets.json').write_text('not json')
            self.assertIsNone(cmake_preset_names(tmp))


class TestFindBuildCommand(unittest.TestCase):
    def test_repo_config_takes_priority(self):
        with tempfile.TemporaryDirectory() as tmp:
            # create a build.sh too — repo config must win
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            (scripts / 'build.sh').write_text('#!/bin/bash\n')
            config = {'command': ['bash', 'scripts/build.sh', 'qt-shell'], 'timeout': 300}
            Path(tmp, REPO_CONFIG_FILENAME).write_text(json.dumps(config))
            cmd, timeout, reason = find_build_command(tmp)
            self.assertEqual(cmd, ['bash', 'scripts/build.sh', 'qt-shell'])
            self.assertEqual(timeout, 300)
            self.assertEqual(reason, '')

    def test_build_sh_no_cmake_presets(self):
        """build.sh present, no CMakePresets.json → call with no preset arg."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            (scripts / 'build.sh').write_text('#!/bin/bash\n')
            cmd, timeout, reason = find_build_command(tmp)
            self.assertEqual(cmd, ['bash', str(Path(tmp, 'scripts', 'build.sh'))])
            self.assertEqual(reason, '')

    def test_build_sh_cmake_presets_with_build(self):
        """build.sh + CMakePresets.json containing 'build' preset → use it."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            build_sh = scripts / 'build.sh'
            build_sh.write_text('#!/bin/bash\n')
            data = {'configurePresets': [{'name': 'build'}, {'name': 'dev'}]}
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            cmd, timeout, reason = find_build_command(tmp)
            self.assertEqual(cmd, ['bash', str(build_sh), 'build'])
            self.assertEqual(reason, '')

    def test_build_sh_cmake_presets_without_build_preset(self):
        """build.sh + CMakePresets.json lacking 'build' → skip with reason."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            (scripts / 'build.sh').write_text('#!/bin/bash\n')
            data = {'configurePresets': [{'name': 'dev'}, {'name': 'qt-shell'}]}
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            cmd, timeout, reason = find_build_command(tmp)
            self.assertIsNone(cmd)
            self.assertIn('qt-shell', reason)
            self.assertIn('build', reason)

    def test_cmake_build_dir_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.20)\n')
            Path(tmp, 'build').mkdir()
            cmd, timeout, reason = find_build_command(tmp)
            self.assertEqual(cmd, ['cmake', '--build', str(Path(tmp, 'build')), '--config', 'Release'])

    def test_cmake_no_build_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.20)\n')
            cmd, timeout, reason = find_build_command(tmp)
            self.assertIsNone(cmd)

    def test_makefile(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'Makefile').write_text('all:\n\techo ok\n')
            cmd, timeout, reason = find_build_command(tmp)
            self.assertEqual(cmd, ['make', '-j4'])

    def test_invalid_repo_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            (scripts / 'build.sh').write_text('#!/bin/bash\n')
            bad_config = {'command': 'not-a-list'}
            Path(tmp, REPO_CONFIG_FILENAME).write_text(json.dumps(bad_config))
            cmd, timeout, reason = find_build_command(tmp)
            self.assertIsNone(cmd)
            self.assertIn('invalid', reason)


class TestHookIntegration(unittest.TestCase):
    """End-to-end hook invocation tests using subprocess."""

    def _make_hook_input(self, file_path: str, tool_name: str = 'Write') -> dict:
        return {'tool_name': tool_name, 'tool_input': {'file_path': file_path}}

    def test_non_cpp_file_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            py_file = os.path.join(tmp, 'main.py')
            result = run_hook(self._make_hook_input(py_file))
            self.assertEqual(result.returncode, 0)

    def test_no_project_root_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            cpp_file = os.path.join(tmp, 'main.cpp')
            # No build system markers in tmp
            result = run_hook(self._make_hook_input(cpp_file))
            self.assertEqual(result.returncode, 0)

    def test_preset_repo_without_build_preset_exits_zero_with_message(self):
        """Core acceptance test: preset-based repo without 'build' does not block."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            (scripts / 'build.sh').write_text('#!/bin/bash\nexit 1\n')  # would fail if invoked
            data = {'configurePresets': [{'name': 'dev'}, {'name': 'qt-shell'}]}
            Path(tmp, 'CMakePresets.json').write_text(json.dumps(data))
            cpp_file = str(Path(tmp, 'src', 'main.cpp'))
            result = run_hook(self._make_hook_input(cpp_file))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('skipped', result.stdout)

    def test_repo_config_command_invoked(self):
        """Per-repo config command is used and failure blocks."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            build_sh = scripts / 'build.sh'
            build_sh.write_text('#!/bin/bash\necho "error: build failed" >&2\nexit 1\n')
            build_sh.chmod(0o755)
            config = {'command': ['bash', str(build_sh)]}
            Path(tmp, REPO_CONFIG_FILENAME).write_text(json.dumps(config))
            cpp_file = str(Path(tmp, 'main.cpp'))
            result = run_hook(self._make_hook_input(cpp_file))
            self.assertEqual(result.returncode, 2)
            self.assertIn('BUILD FAILED', result.stderr)

    def test_repo_config_success_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp, 'scripts')
            scripts.mkdir()
            build_sh = scripts / 'build.sh'
            build_sh.write_text('#!/bin/bash\necho "build ok"\nexit 0\n')
            build_sh.chmod(0o755)
            config = {'command': ['bash', str(build_sh)]}
            Path(tmp, REPO_CONFIG_FILENAME).write_text(json.dumps(config))
            cpp_file = str(Path(tmp, 'main.cpp'))
            result = run_hook(self._make_hook_input(cpp_file))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_non_write_edit_tool_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            cpp_file = str(Path(tmp, 'main.cpp'))
            result = run_hook(self._make_hook_input(cpp_file, tool_name='Read'))
            self.assertEqual(result.returncode, 0)


class TestInstaller(unittest.TestCase):
    def test_install_creates_hook_and_registers_post_tool_use(self):
        with tempfile.TemporaryDirectory() as tmp:
            sys.path.insert(0, str(REPO_ROOT / "scripts"))
            from install_claude_build_verify import install_hook
            hook_target, settings_path = install_hook(Path(tmp))
            self.assertTrue(hook_target.exists())
            settings = json.loads(settings_path.read_text())
            post_tool = settings.get('hooks', {}).get('PostToolUse', [])
            commands = [
                hook.get('command', '')
                for entry in post_tool
                if isinstance(entry, dict)
                for hook in (entry.get('hooks') or [])
                if isinstance(hook, dict)
            ]
            self.assertTrue(
                any('agent-doctrine-build-verify.py' in c for c in commands),
                f"hook not registered: {commands}",
            )

    def test_install_removes_legacy_hook_from_settings(self):
        """Re-installing must remove the old ad-hoc registration."""
        with tempfile.TemporaryDirectory() as tmp:
            settings_path = Path(tmp, 'settings.json')
            legacy_settings = {
                'hooks': {
                    'PostToolUse': [
                        {
                            'matcher': 'Write|Edit',
                            'hooks': [
                                {
                                    'type': 'command',
                                    'command': (
                                        "python3 -c \"import os,runpy;runpy.run_path("
                                        "os.path.expanduser('~/.claude/hooks/build-verify.py'),"
                                        "run_name='__main__')\""
                                    ),
                                    'timeout': 180000,
                                }
                            ],
                        }
                    ]
                }
            }
            settings_path.write_text(json.dumps(legacy_settings))
            sys.path.insert(0, str(REPO_ROOT / "scripts"))
            from install_claude_build_verify import install_hook
            install_hook(Path(tmp))
            settings = json.loads(settings_path.read_text())
            commands = [
                hook.get('command', '')
                for entry in settings.get('hooks', {}).get('PostToolUse', [])
                if isinstance(entry, dict)
                for hook in (entry.get('hooks') or [])
                if isinstance(hook, dict)
            ]
            self.assertFalse(
                any('build-verify.py' in c and 'agent-doctrine' not in c for c in commands),
                f"legacy hook still present: {commands}",
            )


if __name__ == '__main__':
    unittest.main()
