import id3
import sys

hurrengoa = None
datuak = None

def lag_inprimatu(zuhaitza, aukera, indent, azkena):
    global hurrengoa
    global datuak

    sys.stdout.write(indent)
    if azkena:
        sys.stdout.write('\\-')
        indent += (len(aukera)+5)*' '
    else:
        sys.stdout.write('|-')
        indent += '|' + (len(aukera)+4)*' '

    seme_kop = len(zuhaitza.children.keys())
    if seme_kop == 0:
        sys.stdout.write(aukera + '-->' + zuhaitza.label + '\n')
    else:
        sys.stdout.write(aukera + '-->' + zuhaitza.label + ' <' + str(hurrengoa) + '>'+ '\n')
        datuak += str(hurrengoa) + ':\n'
        for n in zuhaitza.gains.keys():
            datuak += ' * ' + n + ': ' + str(zuhaitza.gains[n]) + '\n'
        datuak += '\n'
        hurrengoa += 1

    kont = 0
    for option in zuhaitza.children.keys():
        lag_inprimatu(zuhaitza.children[option], option, indent, kont == seme_kop - 1)
        kont += 1

def inprimatu(zuhaitza):
    global hurrengoa
    global datuak

    hurrengoa = 1
    datuak = '\n\n'

    seme_kop = len(zuhaitza.children.keys())

    if seme_kop == 0:
        sys.stdout.write(zuhaitza.label + '\n')
    else:
        sys.stdout.write(zuhaitza.label + ' <' + str(hurrengoa) + '>'+ '\n')
        datuak += str(hurrengoa) + ':\n'
        for n in zuhaitza.gains.keys():
            datuak += ' * ' + n + ': ' + str(zuhaitza.gains[n]) + '\n'
        datuak += '\n'
        hurrengoa += 1

    kont = 0
    for option in zuhaitza.children.keys():
        lag_inprimatu(zuhaitza.children[option], option, '', kont == seme_kop - 1)
        kont += 1
    sys.stdout.write(datuak)


def main():
    atributuak = ['Non', 'Noiz', 'Lebron hasten da', 'Wade-ren erasoa',  'Wade-ren defentsa', 'Haslem-en aurkaria', 'Emaitza']
    datuak = [
        ['Etxean',  '19:00', 'Bai', 'Zentroan',   'Aurreratua', 'Altua', 'Irabazi'],
        ['Etxean',  '19:00', 'Bai', 'Alboetatik', 'Atzeratua',  'Baxua', 'Irabazi'],
        ['Kanpoan', '19:00', 'Bai', 'Alboetatik', 'Aurreratua', 'Altua', 'Irabazi'],
        ['Etxean',  '17:00', 'Ez',  'Alboetatik', 'Atzeratua',  'Altua', 'Galdu'  ],
        ['Kanpoan', '21:00', 'Bai', 'Alboetatik', 'Aurreratua', 'Baxua', 'Galdu'  ],
        ['Kanpoan', '19:00', 'Ez',  'Zentroan',   'Aurreratua', 'Altua', 'Irabazi'],
        ['Etxean',  '19:00', 'Ez',  'Alboetatik', 'Atzeratua',  'Altua', 'Galdu'  ],
        ['Etxean',  '19:00', 'Bai', 'Zentroan',   'Atzeratua',  'Altua', 'Irabazi'],
        ['Kanpoan', '19:00', 'Bai', 'Zentroan',   'Atzeratua',  'Baxua', 'Irabazi'],
        ['Etxean',  '21:00', 'Ez',  'Alboetatik', 'Atzeratua',  'Baxua', 'Galdu'  ],
        ['Kanpoan', '19:00', 'Ez',  'Alboetatik', 'Aurreratua', 'Baxua', 'Galdu'  ],
        ['Kanpoan', '17:00', 'Ez',  'Zentroan',   'Aurreratua', 'Altua', 'Irabazi'],
        ['Etxean',  '19:00', 'Ez',  'Zentroan',   'Atzeratua',  'Altua', 'Galdu'  ],
        ['Etxean',  '21:00', 'Ez',  'Alboetatik', 'Aurreratua', 'Baxua', 'Galdu'  ],
        ['Etxean',  '17:00', 'Bai', 'Zentroan',   'Aurreratua', 'Altua', 'Irabazi'],
        ['Kanpoan', '17:00', 'Ez',  'Zentroan',   'Aurreratua', 'Baxua', 'Irabazi'],
        ['Etxean',  '17:00', 'Bai', 'Alboetatik', 'Aurreratua', 'Altua', 'Irabaz' ]
]

    data = []
    for l in datuak:
        new_record = {}
        for i in range(len(atributuak)):
            new_record[atributuak[i]] = l[i]
        data.append(new_record)
    atributuak.remove('Emaitza')
    zuhaitza = id3.id3(data, 'Emaitza', atributuak)
    inprimatu(zuhaitza)
    
    """
    sys.stdout.write('Zuhaitza probatzen...\n')
    emaitza = id3.use_decision_tree({'Noiz' : '17:00'}, zuhaitza)
    if emaitza:
        sys.stdout.write(emaitza + '    egingo du\n')
    else:
        sys.stdout.write('Ez dago datu nahikorik\n')
    """

if __name__ == '__main__':
    main()