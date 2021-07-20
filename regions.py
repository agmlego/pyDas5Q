import json

from PIL import Image, ImageDraw, ImageFont
'''
data = json.load(open(
    r'C:\\Users\\agmlego\\Sync\\rwsir-rc7py\\projects\\das_5Q\\node-lib\\assets\\en-us.json'))

regions = {}

for region in data:
    regions[region['shortName']] = {
        'short_name': region['shortName'],
        'description': region['description'],
        'rectangle': {
            'top': region['topLeftCoordinates']['y'],
            'left': region['topLeftCoordinates']['x'],
            'width': region['width'],
            'height': region['height']
        },
        'leds': region['ledIds']
    }

json.dump(regions, open('en-us.json', 'w'), sort_keys=True, indent=4)
'''

regions = json.load(open('en-us.json', encoding='utf-8'))
min_x = 0
min_y = 0
max_x = 0
max_y = 0
for name, region in regions.items():
    rect = region['rectangle']
    if rect['top'] < min_y:
        min_y = rect['top']
    if rect['left'] < min_x:
        min_x = rect['left']
    if rect['top'] + rect['height'] > max_y:
        max_y = rect['top'] + rect['height']
    if rect['left'] + rect['width'] > max_x:
        max_x = rect['left'] + rect['width']

width = max_x-min_x
height = max_y-min_y
print(f'({min_x:.2f},{min_y:.2f}) to ({max_x:.2f},{max_y:.2f}): {width:.2f}x{height:.2f}')

want_width = 3840
want_height = int(want_width * height/width)
scale = want_width / width
want_width += 100
want_height += 100

x_offset = -min_x * scale + 50
y_offset = -min_y * scale + 50

canvas = Image.new('RGB', (want_width, want_height), 'WHITE')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype(
    font=r'C:\Users\agmlego\AppData\Local\Microsoft\Windows\Fonts\Quivira.otf', size=32)

for name, region in regions.items():
    rect = region['rectangle']
    left = int(rect['left'] * scale + x_offset)
    top = int(rect['top'] * scale + y_offset)
    right = int((rect['left']+rect['width']) * scale + x_offset)
    bottom = int((rect['top']+rect['height']) * scale + y_offset)
    draw.rectangle(xy=((left, top), (right, bottom)),
                   fill='BLACK', outline='BLUE')
    draw.text(xy=((left+right)/2, (top+bottom)/2),
              text=name, fill='RED', anchor='mm', font=font)
    leds = ', '.join(map(str, region['leds']))
    if 'Pipe' in region['description']:
        leds = leds.replace(', ','\n')
    draw.text(xy=((left+right)/2, bottom),
              text=leds, fill='GREEN', anchor='md', font=font)

canvas.show()
canvas.save('en-us.png')
