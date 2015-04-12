from random import random, shuffle
from functools import reduce
from negotiator_base import BaseNegotiator
import itertools



class sam4ku_Negotiator(BaseNegotiator):
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.count = 0
        self.other_utility = 0
        self.utilities = []
        self.lists = []
        self.offeredUtilities = []
        self.previous_results = []
        self.round = 0
        self.hasNotLost = True;

    def initialize(self, preferences, iter_limit):
        self.count = 0
        self.offeredUtilities = []

        self.preferences = preferences
        self.iter_limit = iter_limit
        self.lists = itertools.permutations(preferences)
        templist = []
        for list in self.lists:
            value = self.get_utility(list)
            templist.append((list, value))
        #print(self.utilities)

        self.utilities = sorted(templist, key=lambda x: float(x[1]), reverse=True)
        #print(self.utilities)
        # for x in self.utilities:
        #     print(x)

    def get_utility(self, list):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (list.index(item) + 1)) - abs(list.index(item) - self.preferences.index(item))), list, 0)

    def receive_results(self, results):
        self.round += 1
        self.previous_results.append(results)
        #print "Results : ", self.previous_results

    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    def make_offer(self, offer):
        # if random() < 0.10 and offer:
        #     # Very important - we save the offer we're going to return as self.offer
        #     self.offer = offer[:]
        #     return offer


        # Start stubborn
        if self.round == 0:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer
        # see if they ever gave in at the end of a test
        # if so, do not change from max preference
        if self.round > 0:
            # print self.previous_results
            # print "Round : ", self.round
            if self.previous_results[self.round-1][0] == False:
                hasNotLost = False
            if self.previous_results[0][0] == True and self.hasNotLost == True:
                ordering = self.preferences
                self.offer = ordering[:]
                return self.offer
            else:
                ## end stubborn
                if self.count > 0:
                    utility = self.get_utility(offer[:])
                    # print "Utility of this offer: ", utility
                    if utility in self.offeredUtilities:
                        self.offer = offer[:]
                        return self.offer
                if self.count == self.iter_limit - 1:
                    self.offer = offer[:]
                    return self.offer


                # if utility > self.other_utility:
                #     self.offer = offer[:]
                #     return offer
                # if random() < 0.50:
                #     ordering = self.preferences
                #     shuffle(ordering)
                #     self.offer = ordering[:]
                #     return self.offer
                # else:
                ordering = self.utilities[self.count]
                newOffer = []
                for item in ordering[0]:
                    newOffer.append(item)
                # print "hello"
                # print newOffer
                ordering = newOffer
                # print ordering
                # print "goodbye"
                self.offer = ordering[:]
                self.offeredUtilities.append(self.utilities[self.count][1])
                self.count += 1
                # print "Current offer: ", self.offer
                # print "Offered utilities: " , self.offeredUtilities
                return self.offer

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
        self.utilities = []
        self.other_offers = []
        self.iter_limit = 0
        self.pow = 0
        self.count = 0
        self.other_utility = 0
        self.level_index = 0
        self.is_first = False
        self.round = 0
        self.round_results = []
        self.should_be_greedy = False
        self.speed = 1.5
        self.elements = 0
        self.acceptable_utility = 0

    def initialize(self, preferences, iter_limit):
        self.elements = len(preferences)
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.acceptable_utility = self.get_utility(preferences)
        if self.elements < 10:
            permutations = itertools.permutations(preferences)
            templist = []
            #highest = self.get_utility(self.preferences)
            for list in permutations:
                value = self.get_similarity(list, self.preferences)
                templist.append((list, value))
            self.utilities = sorted(templist, key=lambda x: float(x[1]), reverse=True)

        # count = 0
        # positive = 0
        # negative = 0
        # f = open('output.txt', 'w+')
        # for list in self.utilities:
        #     if list[1] > 0:
        #         positive += 1
        #     else:
        #         negative += 1
        #     if (int(list[1]) == int(highest)):
        #         count += 1
        #     else:
        #         f.write(str(highest) + " " + str(count+1) + "\n")
        #         highest = list[1]
        #         count = 0
        # f.write(str(self.utilities[len(self.utilities) - 1][1]) + " " + str(count+1) + "\n")
        # f.write("positive: " + str(positive) + "\n")
        # f.write("negative: " + str(negative) + "\n")
        # f.close()

        self.count = 0
        self.other_utility = 0
        self.other_offers = []
        self.level_index = 0
        self.pow = self.iter_limit/self.speed


    def make_offer(self, offer):
        self.count += 1
        if offer is None:
            self.is_first = True

        if self.round == 0:
            return self.be_greedy(offer)
        else:
            if self.should_be_greedy:
                return self.be_greedy(offer)
            else:
                return self.be_reasonable(offer)

    def be_reasonable(self, offer):
        self.other_offers.append(offer)
        utility = self.utility()

        if self.elements >= 10:
            return self.switch_one(offer)

        if self.count < 2:
            ordering = self.preferences
            self.offer = ordering[:]
            #print(self.utilities)
            return self.offer
        if (self.count == self.iter_limit and not self.is_first) or self.offer_is_acceptable(offer):
            self.offer = offer[:]
            #print("Accepting" + str(self.count))
            return offer
        if offer is not None:
            level = int(self.utilities[self.level_index][1])
            levels = 0
            highest = 0
            for ordering in self.utilities:
                #print(ordering)
                #print(level)
                if int(ordering[1]) == level:
                    levels += 1
                    rank = self.get_similarity(offer, ordering[0])
                    if rank > highest:
                        highest = rank
                        self.offer = list(ordering[0])
            if self.count >= self.pow:
                self.level_index += levels
                #print(self.level_index)
                temp = self.pow/2 + 1
                self.pow += temp
            if self.level_index >= len(self.utilities):
                self.level_index = len(self.utilities) - 1
            return self.offer
        else:
            return self.offer

    def switch_one(self, offer):
        potential_offers = []
        if offer is None:
            self.is_first = True
        else:
            singly_switched = self.get_list(offer)
            temp_list = []
            for ordering in singly_switched:
                value = self.get_similarity(ordering, self.preferences)
                temp_list.append((ordering, value))
            potential_offers = sorted(temp_list, key=lambda x: float(x[1]), reverse=True)

        if offer is not None and self.get_utility(offer) >= self.acceptable_utility:
            self.offer = offer[:]
            #print("Accepting" + str(self.count))
            return offer

        self.acceptable_utility -= len(self.preferences)/4


        self.other_offers.append(offer)
        utility = self.utility()
        self.count += 1
        if self.count % 2 == 1:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer
        else:
            for ordering in potential_offers:
                #print(list[0])
                if ordering[0] != self.preferences:
                    self.offer = list(ordering[0])
                    return self.offer
        ordering = self.preferences
        self.offer = ordering[:]


        return self.offer


    def get_list(self, offer):
        list_of_lists = []
        temp = list(offer)
        for i in range(0, len(temp)):
            current = temp[i]
            for j in range(0, len(temp)):
                if i != j:
                    temp[i] = temp[j]
                    temp[j] = current
                    if temp not in list_of_lists:
                        list_of_lists.append(temp)
                    temp = list(offer)

        return list_of_lists

    def offer_is_acceptable(self, offer):
        for x in range(0, self.level_index):
            if offer == self.utilities[x][0]:
                return True
        return False

    def get_similarity(self, list1, list2):
        total = len(list2)
        return reduce(lambda points, item: points + ((total / (list1.index(item) + 1)) - abs(list1.index(item) - list2.index(item))), list1, 0)

    def be_greedy(self, offer):
        # if self.count == self.iter_limit and not self.is_first:
        #     self.offer = offer[:]
        #     return self.offer
        ordering = self.preferences
        self.offer = ordering[:]
        return self.offer

    def get_utility(self, list):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (list.index(item) + 1)) - abs(list.index(item) - self.preferences.index(item))), list, 0)


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
        self.round_results.append((result, points_a, points_b, count))
        if self.round == 0 and result:
            self.should_be_greedy = True
        if self.should_be_greedy and not result:
            self.should_be_greedy = False
        self.round += 1
        self.count = 0
        if not self.should_be_greedy:
            self.speed += .2
        self.pow = self.iter_limit/self.speed



class SwitchOneNegotiator(BaseNegotiator):
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
        self.is_first = False

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        permutations = itertools.permutations(preferences)
        temp_list = []
        for list in permutations:
            value = self.get_similarity(list, self.preferences)
            temp_list.append((list, value))
        self.utilities = sorted(temp_list, key=lambda x: float(x[1]), reverse=True)
        self.count = 0
        self.other_utility = 0
        self.other_offers = []
        self.level_index = 0
        self.pow = self.iter_limit/2


    def make_offer(self, offer):
        potential_offers = []
        if offer is None:
            self.is_first = True
        else:
            singly_switched = self.get_list(offer)
            temp_list = []
            for ordering in singly_switched:
                value = self.get_similarity(ordering, self.preferences)
                temp_list.append((ordering, value))
            potential_offers = sorted(temp_list, key=lambda x: float(x[1]), reverse=True)

        self.other_offers.append(offer)
        utility = self.utility()
        self.count += 1
        if self.count % 2 == 1:
            ordering = self.preferences
            self.offer = ordering[:]
            return self.offer
        else:
            for ordering in potential_offers:
                #print(list[0])
                if ordering[0] != self.preferences:
                    self.offer = list(ordering[0])
                    return self.offer
        ordering = self.preferences
        self.offer = ordering[:]
        return self.offer

    def get_list(self, offer):
        list_of_lists = []
        temp = list(offer)
        for i in range(0, len(temp)):
            current = temp[i]
            for j in range(0, len(temp)):
                if i != j:
                    temp[i] = temp[j]
                    temp[j] = current
                    if temp not in list_of_lists:
                        list_of_lists.append(temp)
                    temp = list(offer)

        return list_of_lists


    def get_similarity(self, list1, list2):
        total = len(list2)
        return reduce(lambda points, item: points + ((total / (list1.index(item) + 1)) - abs(list1.index(item) - list2.index(item))), list1, 0)

    def get_utility(self, list):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (list.index(item) + 1)) - abs(list.index(item) - self.preferences.index(item))), list, 0)


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
        self.count = 0



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
        utility = self.utility()


        # if self.count == self.iter_limit:
        #     self.offer = offer[:]
        #     return offer
        # else:
        ordering = self.preferences
        self.offer = ordering[:]
        return self.offer
