# Zephan M. Enciso
# zenciso@nd.edu
# Intelligent MicroSystems Lab

import os
import sys
from datetime import datetime
from src import tools


def export_kwargs(kwargs, filename, version):
    time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    allow = tools.query(f'Overwrite {filename}?',
                        'yes') if os.path.isfile(filename) else True

    if not allow:
        return

    try:
        fout = open(filename, 'w')
    except Exception as e:
        print(
            f'ERROR: Could not open export file `{filename}` for writing ({e})',
            file=sys.stderr)
        return

    print(f'# cadence_plot ver. {version}', file=fout)
    print(
        f'# Automatically generated on {time.split("T")[0]} at {time.split("T")[1]}',
        file=fout
    )
    print('#' * 80 + '\n', file=fout)

    for kwarg in kwargs:
        try:
            print(kwarg.split('=')[0] + '=' + kwarg.split('=')[1], file=fout)
        except Exception as e:
            print(f'ERROR: Misformed kwarg `{kwarg}` ({e})', file=sys.stderr)

    fout.close()

    print(f'Export:  {os.path.realpath(filename)}')
    return