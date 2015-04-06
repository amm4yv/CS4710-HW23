from functools import reduce
import itertools
from operator import itemgetter

class BaseNegotiator:
    # Constructor - Note that you can add other fields here; the only 
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.count = 0
        self.other_utility = 0
        self.utilities = []
        self.lists = []

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences 
    def initialize(self, preferences, iter_limit):
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
        for x in self.utilities:
            print(x)


    def get_utility(self, list):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (list.index(item) + 1)) - abs(list.index(item) - self.preferences.index(item))), list, 0)


    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list), 
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        self.offer = offer
        return offer


    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (self.offer.index(item) + 1)) - abs(self.offer.index(item) - self.preferences.index(item))), self.offer, 0)

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.other_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        (result, points_a, points_b, count) = results