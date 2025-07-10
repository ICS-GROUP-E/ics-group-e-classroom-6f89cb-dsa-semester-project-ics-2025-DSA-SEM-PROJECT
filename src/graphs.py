class Graphs:
    def __init__(self):
        self.graph = {}

    def add_book_node(self, title):
        if title not in self.graph:
            self.graph[title] = []

    def add_edge(self, book1, book2):
        # we'll use this to connect similar books
        if book1 in self.graph and book2 in self.graph:
            if book2 not in self.graph[book1]:
                self.graph[book1].append(book2)
            if book1 not in self.graph[book2]:
                self.graph[book2].append(book1)

    def get_recommendations(self, title):
        # here we have BFS traversal to recommend the books
        if title not in self.graph:
            return []
        ##

        visited = set()
        recommendations = []
        queue = [title]

        while queue:
            current_book = queue.pop(0)
            if current_book not in visited:
                visited.add(current_book)
                recommendations.append(current_book)
                for neighbor in self.graph[current_book]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        recommendations.remove(title)
        return recommendations[:5]  # Return 5 recommendations


if __name__ =="__main__":
    library = Graphs()



