import csv
from collections import defaultdict

class NOWHERE:
    def __init__(self, filename = "NOWHERE_DATASET"):
        with open(f'{filename}.csv', 'r') as f:
            reader = csv.reader(f)
            csv_per_line = list(reader)
        self.dataset = csv_per_line

        self.year = {}
        self.geography = {}
        self.reality = defaultdict(dict)
        self.human_factor = defaultdict(dict)
        self.domains = defaultdict(dict)
        self.goals = defaultdict(dict)
        self.means = defaultdict(dict)
        self.my_approach = defaultdict(dict)
        self.content_to_me = defaultdict(dict)

        print("Initializing done")
        self.fill_dicts()

    def fill_dicts(self):
        countries_l = []
        reality_items_l = []
        human_factors_l = []
        domains_l = []
        goals_l = []
        means_l = []
        my_approaches_l = []
        contents_to_me_l = []
        for enum, i in enumerate(self.dataset[3:]):
            if enum == 0:
                countries_l = i[2:7]
                reality_items_l = i[7:28]
                human_factors_l = i[28:33]
                domains_l = i[33:48]
                goals_l = i[48:67]
                means_l = i[67:90]
                my_approaches_l = i[90:115]
                contents_to_me_l = i[115:149]
                continue
            if enum == 1:
                continue

            self.year[i[0]] = i[1]

            self.geography[i[0]] = countries_l[int(i[2:7].index(str(1)))]
            
            for column_val, ri in enumerate(reality_items_l):
                if i[column_val + 7] != "":
                    # ValueError if some are empty 
                    try:
                        self.reality[i[0]][ri] = float(i[column_val + 7])
                    except:
                        continue

            for column_val, ri in enumerate(human_factors_l):
                if i[column_val + 28] != "":
                    try:
                        self.human_factor[i[0]][ri] = float(i[column_val + 28])
                    except:
                        continue

            for column_val, ri in enumerate(domains_l):
                if i[column_val + 33] != "":
                    try:
                        self.domains[i[0]][ri] = float(i[column_val + 33])
                    except:
                        continue
            
            for column_val, ri in enumerate(goals_l):
                if i[column_val + 48] != "":
                    try:
                        self.goals[i[0]][ri] = float(i[column_val + 48])
                    except:
                        continue
            
            for column_val, ri in enumerate(means_l):
                if i[column_val + 67] != "":
                    try:
                        self.goals[i[0]][ri] = float(i[column_val + 67])
                    except:
                        continue

            for column_val, ri in enumerate(my_approaches_l):
                    if i[column_val + 90] != "":
                        try:
                            self.my_approach[i[0]][ri] = float(i[column_val + 90])
                        except:
                            continue
            
            for column_val, ri in enumerate(contents_to_me_l):
                    if i[column_val + 115] != "":
                        try:
                            self.content_to_me[i[0]][ri] = float(i[column_val + 115])
                        except:
                            continue
            
        print("Dictionaries filled")
        

h = NOWHERE()

        