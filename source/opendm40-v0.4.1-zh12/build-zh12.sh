#!/bin/sh
# Build opendm40 v0.4.1 Chinese (zh12) from this source tree.
#   ./build-zh12.sh            normal build (Cargo may fetch crates)
#   ./build-zh12.sh --offline  only if the Cargo cache is already populated
set -e
cd "$(dirname "$0")/firmware"

# rustup installed by rustup-init --no-modify-path: Windows form for rustup,
# MSYS form for PATH (see the upstream README "Toolchain").
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
        if command -v cygpath >/dev/null 2>&1; then
            RUSTUP_HOME="${RUSTUP_HOME:-$(cygpath -m "$HOME/.rustup")}"
            CARGO_HOME="${CARGO_HOME:-$(cygpath -m "$HOME/.cargo")}"
        fi
        ;;
esac
export RUSTUP_HOME="${RUSTUP_HOME:-$HOME/.rustup}"
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}"
PATH="$HOME/.cargo/bin:$PATH"

# stackdepth.py wants llvm-objdump on PATH; build.sh finds llvm-objcopy by
# itself through the sysroot.
if command -v rustc >/dev/null 2>&1; then
    SYSROOT="$(rustc --print sysroot)"
    case "$(uname -s)" in
        MINGW*|MSYS*|CYGWIN*) command -v cygpath >/dev/null 2>&1 && SYSROOT="$(cygpath -u "$SYSROOT")" ;;
    esac
    for d in "$SYSROOT"/lib/rustlib/*/bin; do
        [ -d "$d" ] && PATH="$d:$PATH"
    done
fi
export PATH

# build.sh / stackdepth.py inline Python: UTF-8, no Windows GBK surprises.
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
# stackdepth.py uses shutil.which and needs PATHEXT for llvm-objdump.exe.
export PATHEXT="${PATHEXT:-.COM;.EXE;.BAT;.CMD}"

exec ./build.sh "$@"
