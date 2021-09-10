import os

import labelimg_xml

path_dir = os.getcwd() + '/xml/'
whole_static = [['RBC', 0, 200, 0, 0, 0], ['Platelets', 0, 100, 0, 0, 0]]


def main():
    file_list = [_ for _ in os.listdir(path_dir) if _.endswith('.xml')]
    xml_list = [labelimg_xml.read_xml(path_dir, _) for _ in file_list]

    print('category, count, min, max, avg')
    for page, file in enumerate(xml_list):
        static = [['RBC', 0, 200, 0, 0, 0], ['Platelets', 0, 100, 0, 0, 0]]
        filename = file_list[page]
        title = file[0]
        table = file[1]
        print('{:<9}'.format(filename), end=' : ', flush=True)

        for box in table:
            size = box[3] + box[4] - box[1] - box[2]
            if box[0] == 'RBC':
                label = 0
                if size < 50:
                    continue
            elif box[0] == 'Platelets' or box[0] == 'Platelet':
                label = 1
                if size > 100:
                    continue
            else:
                continue
            static[label][1] += 1
            static[label][2] = size
            static[label][2] = min((static[label][2], size))
            static[label][3] = max((static[label][3], size))
            static[label][4] += size

        for cell in static:
            if cell[1] == 0:
                cell[5] = 0
            else:
                cell[5] = round(cell[4] / cell[1], 3)

        for row in static:
            text = '['
            for item in row:
                text += str(item) + ', '
            text += ']'
            print('{:<42}'.format(text), end='', flush=True)
        print('')

        for r, row in enumerate(whole_static):
            row[1] += static[r][1]
            row[2] = min((row[2], static[r][2]))
            row[3] = max((row[3], static[r][3]))
            row[4] += static[r][4]
    print('─'*40)
    print('{:<9}'.format('Total'), end=' : ', flush=True)

    for cell in whole_static:
        cell[5] = round(cell[4] / cell[1], 3)

    for row in whole_static:
        text = '['
        for item in row:
            text += str(item) + ', '
        text += ']'
        print('{:<42}'.format(text), end='', flush=True)
    print('')

if __name__ == '__main__':
    main()