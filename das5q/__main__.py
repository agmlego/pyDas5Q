import das5q
import time

with das5q.Das5Q() as kbd:
    print(f'Keyboard found, running {kbd.get_firmware_version()} firmware')
    for idx in range(250):
        kbd.write_led_color(led=idx, color=das5q.Color(
            red=0, green=0, blue=0))

    colors = [
        das5q.Color('#DD0303'),
        das5q.Color('#F78800'),
        das5q.Color('#F7E600'),
        das5q.Color('#007C25'),
        das5q.Color('#007C25'),
        das5q.Color('#710783'),
    ]
    for idx in range(216):
        col = idx % 24
        row = idx // 24
        print(idx)
        kbd.write_led_color(led=idx, color=colors[row % 6])
        time.sleep(0.1)
