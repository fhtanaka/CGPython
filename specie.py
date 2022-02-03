from operator import attrgetter
from typing import List
from graphviz import Graph
import itertools


class Specie:
    id_counter = itertools.count().__next__

    def __init__(self, representant: Graph, members: List[Graph]):

        self.id: int = self.id_counter()
        self.members = members
        self.representant = representant
    
    def add_member(self, member):
        self.members.append(member)
    
    def add_member_front(self, member):
        self.members.insert(0, member)

    def remove_members(self):
        self.members = []

    def shuffle_members(self, rng):
        self.members = sorted(self.members, lambda x: rng.random())

    def new_representant_random(self, rng):
        self.representant = rng.choice(self.members)

    def new_representant_highest(self):
        self.representant = max(self.members, key=attrgetter('original_fit'))

    def new_representant_lowest(self):
        self.representant = min(self.members, key=attrgetter('original_fit'))

    def new_representant_first(self):
        self.representant = self.members[0]