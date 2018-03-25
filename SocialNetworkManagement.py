# -*- coding: utf-8 -*-
import os
import sys
import collections
import heapq
import argparse 

class SocialNetworkMangement():
        
    def __init__(self):
        self.people = set()
        self.relations = collections.defaultdict(list)
    
    def load(self, path):       
        if not path:
            path = os.path.abspath('SocialNetwork.txt')
        elif not os.path.isfile(path):
            print("File path {} does not exist. Exiting...".format(path))
            sys.exit()
        
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                person_a, person_b = line.strip().split(',')
                #add person a and person b into the set. the structure set keeps each element is unique
                #the relation dict {} maps the person to the list [] which has the relation with him
                #relation A - B means A -> B and B -> A. so we add both of them into the relations
                self.people.update({person_a, person_b})
                self.relations[person_a].append(person_b)
                self.relations[person_b].append(person_a)
    
    def get_pepople_number(self):
        return len(self.people)
    
    def get_minimum_distance(self, person_a = 'STACEY_STRIMPLE', person_b = 'RICH_OMLI'):
        #whether A or B does not exist, we consider it's unreabable and the distance is infinte
        if person_a not in self.people or person_b not in self.people:
            print("people does not exist")
            return sys.maxsize
        
        current_position = person_a
        distance = dict((key, sys.maxsize) for key in self.relations.keys())
        distance[current_position] = 0
        pepople_number = self.get_pepople_number()
        min_heap = []

        #use dijkstra to get the short distance between A and B.
        #Note dijkstra is just fit for the single original start.
        #use breadth first search to search the path
        while pepople_number != 0:
            pepople_number = pepople_number - 1
            
            for p in self.relations[current_position]:
                if distance[p] > distance[current_position] + 1:
                    distance[p] = distance[current_position] + 1
                    heapq .heappush(min_heap, (distance[p], p))
            
            #use the minimum heap to keep the elements which are not visited
            #we always visit the minimun element as the next position
            if min_heap:
                _, current_position = heapq.heappop(min_heap)                       
        return distance[person_b]      
        
        
    
def main():
    parser = argparse.ArgumentParser(description='Social Network Management')
    parser.add_argument('-p', '--path', help='The path to the socialnetwork.txt, Default is "SocialNetwork.txt"', type=str, required=False, default=None)
    parser.add_argument('-a', '--person_a', help='The name of person A, Default is "STACEY_STRIMPLE"',type=str, required=False, default='STACEY_STRIMPLE')
    parser.add_argument('-b', '--person_b', help='The name of person B, Default is "RICH_OMLI"',type=str, required=False, default='RICH_OMLI')
    args = parser.parse_args()
    
    social_network_management = SocialNetworkMangement()
    social_network_management.load(args.path)
    print('the total number of people in the social network is {}'.format(social_network_management.get_pepople_number()))
    print('the distance between A and B is {}'.format(social_network_management.get_minimum_distance(args.person_a, args.person_b)))
    
if __name__ == '__main__':
    main()