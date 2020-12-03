import sys

if __name__ == '__main__':
    from audnauseum.app import app

    # Require at least Python v3.8
    if sys.version_info.major < 3 or sys.version_info.minor < 8:
        print('Error: Python v3.8+ is required.', file=sys.stderr)
        print('Your version: ', file=sys.stderr)
        print(sys.version, file=sys.stderr)

    sys.exit(app.exec_())
