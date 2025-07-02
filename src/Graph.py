class TaskGraph:
    def __init__(self):
        self.graph = {}

    def add_task(self, task):
        if task not in self.graph:
            self.graph[task] = []

    def add_dependency(self, task, depends_on):
        if task in self.graph:
            self.graph[task]
        if depends_on not in self.graph:
            self.graph[depends_on] = []
        self.graph[depends_on].append(task)

    def get_dependencies(self, task):
        return self.graph.get(task, [])

    def topological_sort(self):
        visited = set()
        stack = []

        def visit(node):
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    visit(neighbor)
                stack.append(node)

        for node in self.graph:
            visit(node)

        return stack[::-1]