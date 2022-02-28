from operator import attrgetter
from typing import List
from .graph import Graph
import itertools


class Specie:
    id_counter = itertools.count().__next__

    def __init__(self, representant: Graph, members: List[Graph]):

        self.id: int = self.id_counter()
        self.members = members
        self.representant = representant
        self.age = 0
    
    def add_member(self, member):
        self.members.append(member)
    
    def add_member_front(self, member):
        self.members.insert(0, member)

    def remove_members(self):
        self.members = []

    def shuffle_members(self, rng):
        self.members = sorted(self.members, lambda x: rng.random())

    def new_representant_random(self, rng):
        rep = rng.choice(self.members)
        self.representant = rep.clone_graph() 

    def new_representant_highest(self):
        rep = max(self.members, key=attrgetter('original_fit'))
        self.representant = rep.clone_graph() 

    def new_representant_lowest(self):
        rep = min(self.members, key=attrgetter('original_fit'))
        self.representant = rep.clone_graph() 

    def new_representant_first(self):
        rep = self.members[0]
        self.representant = rep.clone_graph() 