from random import random, shuffle
from functools import reduce
from negotiator_base import BaseNegotiator


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.

    def get_similarity(self, list1, list2):
        total = len(list1)
        return reduce(lambda points, item: points + ((total / (list1.index(item) + 1)) - abs(list1.index(item) - list2.index(item))), list1, 0)


    def make_offer(self, offer):
        # if random() < 0.10 and offer:
        #     # Very important - we save the offer we're going to return as self.offer
        #     self.offer = offer[:]
        #     return offer
        self.other_offers.append(offer)

        utility = self.utility()

        self.count += 1

        if self.count < 3:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer
        if self.offer_is_acceptable(offer) or self.count == self.iter_limit:
            self.offer = offer[:]
            return offer
        if self.other_is_stubborn():
            level1 = int(self.utilities[self.level_index][1])
            highest = 0
            for list in self.utilities:
                if int(list[1]) == level1:
                    rank = self.get_similarity(offer, list[0])
                    if rank > highest:
                        highest = rank
                        self.offer = list[0]
                    #print(str(self.get_similarity(offer, list[0])) + " " + str(list[1]))
            #print(self.offer)
            self.level_index += 1
            return self.offer

        if False:
            #print(self.other_offers)
            print(self.other_utility)
            print(self.utility())
            print(self.count)

        # if self.count == self.iter_limit:
        #     self.offer = offer[:]
        #     return offer
        # if utility > self.other_utility:
        #     self.offer = offer[:]
        #     return offer
        # if random() < 0.50:
        #     ordering = self.preferences
        #     shuffle(ordering)
        #     self.offer = ordering[:]
        #     return self.offer
        else:
            return self.offer

    def offer_is_acceptable(self, offer):
        level = int(self.utilities[self.level_index][1])
        for list in self.utilities:
            if int(list[1]) == level:
                if offer == list[0]:
                    return True
        return False


    def other_is_stubborn(self):
        return self.other_offers[len(self.other_offers)-2] == self.other_offers[len(self.other_offers)-1]




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
