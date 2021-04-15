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
        d[Point(int(initial_point[0]), int(initial_point[1]))] = content[1:]

    start = None
    for i in d:

        # determine the starting
        if d[i][0] == 'START':
            start = i

        if (d[i][0] != 'GOAL'):
            # split all the neighbour vectors into a list
            d[i][1] = d[i][1].split("|")

        # convert all neighbour vectors into Point objects
        for j in range(len(d[i][1])):
            vector = d[i][1][j].split(".")
            d[i][1][j] = Point(int(vector[0]), int(vector[1]))

        d[i][-1] = int(d[i][-1])
        d[i][-3] = None

    maze_size = int(len(d) ** 0.5)

    print(d)
    print(maze_size)

    adj_list = {}
    temp = step

    print("about to step into while loop")
    while (temp != maze_size):
        inner = {}

        for i in d:
            lst = []
            for j in range(len(d[i][1])):

                lst.append(i.step(d[i][1][j], temp))

            inner[i] = lst
            adj_list[temp] = inner

        temp += 1
    # print(type(adj_list.keys()[0]))



    # initialize queue with start
    step = 1
    failed = 0
    q = Queue()
    q.enqueue(start)

    # begin the BFS loop
    while q.isEmpty() != True:
        u = q.dequeue()

        if (d[u][0] == 'RED'):
            step += 1
        elif (d[u][0] == 'YELLOW'):
            step -= 1

        if (step == maze_size or step == 0):
            failed = 1
            break

        print("about to go into adj_list")
        print(d)
        print(d[Point(0,2)])

        for i in adj_list[step][u]:

            if d[i][3] == 'white':

                # change the colour
                d[i][3] = 'grey'

                # increase the distance
                d[i][4] += 1

                # update the parent
                d[i][2] = u

                q.enqueue(i)

        d[u][3] = 'black'

    if (failed == 1):
        print("Failed.")
    else:
        # print path here
        print("Good")







