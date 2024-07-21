"""
Test suite for distutils.

Tests for the command classes in the distutils.command package are
included in distutils.tests as well, instead of using a separate
distutils.command.tests package, since command identification is done
by import rather than matching pre-defined names.
"""

import shutil
from typing import Sequence, Optional


def missing_compiler_executable(
    cmd_names: Sequence[str] = [], compiler_type: Optional[str] = None
):  # pragma: no cover
    """Check if the compiler components used to build the interpreter exist.

    Check for the existence of the compiler executables whose names are listed
    in 'cmd_names' or all the compiler executables when 'cmd_names' is empty
    and return the first missing executable or None when none is found
    missing.

    """
    from distutils import ccompiler, errors, sysconfig

    compiler = ccompiler.new_compiler(compiler=compiler_type)
    sysconfig.customize_compiler(compiler)
    if compiler.compiler_type == "msvc":
        # MSVC has no executables, so check whether initialization succeeds
        try:
            compiler.initialize()
        except errors.DistutilsPlatformError:
            return "msvc"
    for name in compiler.executables:
        if cmd_names and name not in cmd_names:
            continue
        cmd = getattr(compiler, name)
        if cmd_names:
            assert cmd is not None, f"the '{name}' executable is not configured"
        elif not cmd:
            continue
        if shutil.which(cmd[0]) is None:
            return cmd[0]


def get_possible_compiler_types() -> Sequence[str]:
    """Returns a list of compiler types that could be used to build extensions
    for the current interpreter.
    """
    from distutils import ccompiler

    compiler_types = []
    default_compiler_type = ccompiler.get_default_compiler()
    compiler_types.append(default_compiler_type)
    if default_compiler_type == "msvc":
        compiler_types.append("mingw32")
    return compiler_types
