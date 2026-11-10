#!/usr/bin/env python3
"""Send a debug command to the meter over USBTMC (PyVISA, Windows).

    python dm.py 'DBG:KEY 0' 'DBG:TAP 100,200'
    python dm.py --query 'DBG:BOOT?'

Some replies are Chinese since v0.4.0 (DBG:VIEW?, MMEM:CAT?, SYST:*?), so the
resource is opened as UTF-8; without it PyVISA decodes as ASCII and any
Chinese reply raises UnicodeDecodeError.
"""

import sys

import pyvisa

# Reply text is UTF-8; the Windows console is not. Replace what it cannot show
# instead of dying in the middle of a batch of queries.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    argv = sys.argv[1:]
    rm = pyvisa.ResourceManager("@py")
    names = [r for r in rm.list_resources() if "::4617::53312::" in r]
    if not names:
        sys.exit("meter not found over USBTMC")
    d = rm.open_resource(
        names[0],
        read_termination="\n",
        write_termination="\n",
        timeout=15000,
        encoding="utf-8",
    )

    i = 0
    while i < len(argv):
        if argv[i] == "--query":
            print(d.query(argv[i + 1]).strip())
            i += 2
        else:
            d.write(argv[i])
            print("sent: %s" % argv[i])
            i += 1
    d.close()


main()
