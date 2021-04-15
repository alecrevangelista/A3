import sys

class Point:
    """ Represent a two-dimensional point
    x - horizontal position
    y - vertical position
    """

    def __init__(self, x, y):
        """ Initialize a new point
        """
        self.x, self.y = int(x), int(y)

    def __str__(self):
        """ Return a string representation of self
        """
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        """
        Return a string that would evaluate to a Point equivalent to self
        """
        return "Point({}, {})".format(self.x, self.y)

    def step(self, other, step):
        """ Apply the step size to a given point and return the new neighbour
        """
        return Point(self.x + (other.x * step), self.y + (other.y * step))


class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

if __name__ == '__main__':

    # You do NOT need to include any error checking.
    # I found this particular check personally helpful, when I forgot to provide a filename.
    if len(sys.argv) != 2:
        print("Usage: python3 Alice.py <inputfilename>")
        sys.exit()

    # Here is how you open a file whose name is given as the first argument
    f = open(sys.argv[1])

    d = {}
    step = 1

    for line in f:
        line = line.strip()
        content = line.split(",")
        initial_point = content[0].split(".")
        d[Point(int(initial_point[0]), int(initial_point[1])).__str__()] = content[1:]
        d[Point(int(initial_point[0]), int(initial_point[1])).__str__()].append(Point(int(initial_point[0]), int(initial_point[1])))

    start = None
    for i in d:

        # determine the starting
        if d[i][0] == 'START':
            start = i

        if (d[i][0] != 'GOAL'):
            # split all the neighbour vectors into a list
            d[i][1] = d[i][1].split("|")
        else:
            goal = i

        # convert all neighbour vectors into Point objects
        for j in range(len(d[i][1])):
            vector = d[i][1][j].split(".")
            d[i][1][j] = Point(int(vector[0]), int(vector[1]))

        d[i][-2] = int(d[i][-2])
        d[i][-4] = None


    maze_size = int(len(d) ** 0.5)

    print(d)
    print(maze_size)

    adj_list = {}
    temp = step

    while (temp != maze_size):
        inner = {}

        for i in d:
            lst = []
            for j in range(len(d[i][1])):

                lst.append(d[i][-1].step(d[i][1][j], temp))

            inner[i] = lst
            adj_list[temp] = inner

        temp += 1
    print(adj_list)

    # initialize queue with start
    step = 1
    failed = 0
    q = Queue()
    q.enqueue(start)

    # begin the BFS loop
    while q.isEmpty() != True:
        u = q.dequeue()

        if (d[u.__str__()][0] == 'RED'):
            step += 1
        elif (d[u.__str__()][0] == 'YELLOW'):
            step -= 1

        if (step == maze_size or step == 0 or failed == 1):
            failed = 1
            break

        for i in adj_list[step][u.__str__()]:
            try:
                if d[i.__str__()][3] == 'white':

                # change the colour
                    d[i.__str__()][3] = 'grey'

                # update the parent
                    d[i.__str__()][2] = u

                # increase the distance
                    d[i.__str__()][4] = d[d[i.__str__()][2].__str__()][4] + 1

                    q.enqueue(i)
            except(KeyError):
                failed = 1
                break
        d[u.__str__()][3] = 'black'

    if (failed == 1):
        print("No sol")
    else:
        # print path here
        last = []
        dist = d[goal][4]
        last.append(d[goal][-1])
        while d[goal][2] is not None:
            last.append(d[goal][2])
            goal = str(d[goal][2])
        print(last)
        print(dist)



