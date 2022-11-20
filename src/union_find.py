from typing import List


class UnionFind():
    def __init__(self, number_of_elements: int):
        self.array = [i for i in range(number_of_elements)]

    def union(self, element_1: int, element_2: int):
        if element_1 >= len(self.array) or \
           element_2 >= len(self.array):
            return
        self.array[self.find(element_1)] = self.find(element_2)

    def find(self, element):
        next_element = self.array[element]
        if next_element == element:
            return element
        root = self.find(next_element)
        self.array[element] = root
        return root
