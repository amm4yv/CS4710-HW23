from random import random, shuffle
from functools import reduce
from negotiator_base import BaseNegotiator
import itertools


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.count = 0
        self.other_utility = 0
        self.utilities = []
        self.other_offers = []
        self.level_index = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        permutations = itertools.permutations(preferences)
        templist = []
        for list in permutations:
            value = self.get_similarity(list, self.preferences)
            templist.append((list, value))
        self.utilities = sorted(templist, key=lambda x: float(x[1]), reverse=True)
        self.count = 0
        self.other_utility = 0
        self.other_offers = []
        self.level_index = 0


    def make_offer(self, offer):
        self.other_offers.append(offer)
        utility = self.utility()
        self.count += 1

        if self.count < 2:
            ordering = self.preferences
            self.offer = ordering[:]
            #print(self.utilities)
            return self.offer
        if self.offer_is_acceptable(offer) or self.count == self.iter_limit:
            self.offer = offer[:]
            return offer
        if offer != None:
            level = int(self.utilities[self.level_index][1])
            levels = 0
            highest = 0
            for list in self.utilities:
                if int(list[1]) == level:
                    levels += 1
                    rank = self.get_similarity(offer, list[0])
                    if rank > highest:
                        highest = rank
                        self.offer = list[0]
            self.level_index += levels
            if self.level_index >= len(self.utilities):
                self.level_index = len(self.utilities - 1)
            return self.offer
        else:
            return self.offer

    def offer_is_acceptable(self, offer):
        for x in range(0, self.level_index):
            level = int(self.utilities[x][1])
            for list in self.utilities:
                if int(list[1]) == level:
                    if offer == list[0]:
                        return True
        return False

    def get_similarity(self, list1, list2):
        total = len(list2)
        return reduce(lambda points, item: points + ((total / (list1.index(item) + 1)) - abs(list1.index(item) - list2.index(item))), list1, 0)


    def other_is_stubborn(self):
        return self.other_offers[len(self.other_offers)-2] == self.other_offers[len(self.other_offers)-1]

      # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.other_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        (result, points_a, points_b, count) = results


class RandomNegotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    def make_offer(self, offer):
        # if random() < 0.10 and offer:
        #     # Very important - we save the offer we're going to return as self.offer
        #     self.offer = offer[:]
        #     return offer
        self.count += 1
        utility = self.utility()


        if self.count == self.iter_limit:
            self.offer = offer[:]
            return offer
        if random() < 0.50:
            ordering = self.preferences
            shuffle(ordering)
            self.offer = ordering[:]
            return self.offer
        else:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer

class StubbornNegotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    def make_offer(self, offer):
        # if random() < 0.10 and offer:
        #     # Very important - we save the offer we're going to return as self.offer
        #     self.offer = offer[:]
        #     return offer
        self.count += 1
        utility = self.utility()


        if self.count == self.iter_limit:
            self.offer = offer[:]
            return offer
        else:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer
