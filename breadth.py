

class BreadthSearch():
    
    def __init__(self,map):
        self.map = map
        self.getNodes()
        self.createGraph()
    
    # Creates a list of not-wall squares
    def getNodes(self):
        self.nodes = []
        for y in range(0,len(self.map.map)):
            for x in range(0,len(self.map.map[y])):
                if self.map.map[y][x].isWall:
                    pass
                else:
                    self.nodes.append(self.map.map[y][x])
    
    def findNeighbors(self,square):
        result = []
        for x,y in [(square.coord.x+i,square.coord.y+j) for i in (-1,0,1) for j in (-1,0,1) if abs(i)!=abs(j)]:
            if x >= 0 and y >= 0 and x < len(self.map.map[0]) and y < len(self.map.map): 
                if not self.map.map[y][x].isWall and self.map.map[y][x]!=square:
                    result.append(self.map.map[y][x])
        return result
    
    # Create a dictionary for bfs
    def createGraph(self):
        self.graph = {}
        for node in self.nodes:
            neighbors = self.findNeighbors(node)
            self.graph[node] = set(neighbors)

    
    # Breadth first search
    def bfs(self,start):

        frontier = []
        frontier.append(start)
        came_from = {}
        came_from[start] = None
        
        while len(frontier) > 0:
            current = frontier.pop(0)
            for next in self.graph[current]:
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = current
                    next.cameFrom = current
       
"""
    def getDistance(self,first,second):
        d1 = sqrt(abs(first.x-self.end.x)^2 * abs(first.y - self.end.y)^2)
        d2 = sqrt(abs(second.x-self.end.x)^2 * abs(second.y - self.end.y)^2)
        return (d1 - d2)
    
    def sortGraph(self,end):
        self.end = end
        for node in self.graph:
            self.graph[node].sort(key = cmp_to_key(self.getDistance))

    def tryBfs(self):
        path = self.bfs(self.graph,self.map[0][13])
        pathasid = []
        for n in path:
            pathasid.append(n.id)
        return pathasid

    def bfs(self, graph, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(graph[vertex] - visited)
        return visited
"""
    
        
        
        