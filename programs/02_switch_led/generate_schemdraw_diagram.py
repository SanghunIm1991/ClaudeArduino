import re
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')


def add_white_background(svg_path):
    """schemdrawのSVG出力は背景が透明で、ダークモードのエディタ等で見えにくくなるため、
    viewBoxに合わせた白背景の<rect>を挿入する。"""
    with open(svg_path, encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'viewBox="([\-0-9.]+) ([\-0-9.]+) ([0-9.]+) ([0-9.]+)"', content)
    x, y, w, h = m.groups()
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff"/>'
    content = content.replace('">', '">' + rect, 1)
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(content)

with schemdraw.Drawing(file='circuit_diagram_schemdraw_switch.svg', show=False) as d:
    d += elm.Dot().label('+5V', loc='top')
    d += elm.Line().down().length(1)
    d += elm.Switch().down().length(1.5).label('SW1 タクトスイッチ', loc='right')
    d += elm.Line().down().length(0.7)
    d += elm.Dot()
    d.push()
    d += elm.Line().right().length(3.5).label('D2 (デジタル入力)', loc='right')
    d.pop()
    d += elm.Line().down().length(0.7)
    d += elm.Resistor().down().length(1.5).label('R1: 10kΩ (プルダウン)', loc='right')
    d += elm.Line().down().length(0.5)
    d += elm.Ground()
add_white_background('circuit_diagram_schemdraw_switch.svg')

with schemdraw.Drawing(file='circuit_diagram_schemdraw_led.svg', show=False) as d:
    d += elm.Dot().label('D8 (デジタル出力)', loc='top')
    d += elm.Line().down().length(1)
    d += elm.Resistor().down().length(1.5).label('R2: 1kΩ', loc='right')
    d += elm.Line().down().length(0.7)
    d += elm.LED().down().length(1.5).label('LED1 (赤色)', loc='right')
    d += elm.Line().down().length(0.5)
    d += elm.Ground()
add_white_background('circuit_diagram_schemdraw_led.svg')

print('done')
