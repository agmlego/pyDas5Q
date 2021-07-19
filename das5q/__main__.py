import das5q

with das5q.Das5Q() as kbd:
    print(f'Keyboard found, running {kbd.get_firmware_version()} firmware')
