from random import randint


def square_room(side):
    room = [['1'] * side for _ in range(side)]
    room[0] = ['3'] * side
    room[-1] = ['5'] * side

    for i in range(side):
        room[i][0] = '2'
        room[i][-1] = '7'

    room[0][0] = '4'
    room[-1][0] = '0'  # change edge
    room[0][-1] = '6'  # change edge
    room[-1][-1] = '0'  # change edge

    return room


def map_generator(w, h):
    """:parameter w: number of rooms in length
       :parameter h: number of rooms in height"""
    if w == h == 1:
        return square_room(50)
    rooms = []
    for j in range(h - 1):
        line = []
        for i in range(w - 1):
            line.append(randint(6, int((44 / (w - 1)))))
        line.append(randint(6, min(50 - sum(line), int((44 / (w - 1))))))
        rooms.append(line)
    rooms.append([])
    for k in range(w):
        rooms[-1].append(randint(6, 50 - sum([max(rooms[i]) for i in range(h - 1)])))
    return rooms


if __name__ == '__main__':
    print(*map_generator(5, 5), sep='\n')
