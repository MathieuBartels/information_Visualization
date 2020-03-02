import csv
import os
from collections import defaultdict

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class NOWHERE():
    '''
    This class contains many different dictionaries for easy data acces from the NOWHERE dataset.
    ----------
    Attributes
    ----------
    year : dict
        maps from an image name to the year in which the image is taken

    geography: dict
        maps from the image name to the continent where the image was taken

    reality: defaultdict(dict)
        maps from the image name to the reality subsections and from each subsection it maps to the value

    human_factor: defaultdict(dict)
        maps from the image name to the human_factor subsections and from each subsection it maps to the value

    domains: defaultdict(dict)
        maps from the image name to the domains subsections and from each subsection it maps to the value
    
    goals: defaultdict(dict)
        maps from the image name to the goals subsections and from each subsection it maps to the corresponding value

    means: defaultdict(dict)
        maps from the image name to the means subsections and from each subsection it maps to the corresponding value
    
    my_approach: defaultdict(dict)
        maps from the image name to the my_approach subsections and from each subsection it maps to the corresponding value
    
    conent_to_me: defaultdict(dict)
        maps from the image name to the content_to_me subsections and from each subsection it maps to the corresponding value

    naming_convention: dict
        maps from the image name to the corresponding integer indicated in the NOWHERE_naming_convention
    '''
    def __init__(self, filename = "app/data/NOWHERE_DATASET", naming_convention = "app/data/NOWHERE_Naming_Convention"):
        with open(f'{filename}.csv', 'r') as f:
            reader = csv.reader(f)
            csv_per_line = list(reader)

        with open(f'{naming_convention}.csv', 'r') as g:
            name_reader = csv.reader(g)
            name_csv_per_line = list(name_reader)

        self.dataset = csv_per_line
        self.naming_convention_csv = name_csv_per_line

        self.year = {}
        self.geography = {}
        self.reality = defaultdict(dict)
        # self.human_factor = defaultdict(dict)
        self.human_factor = defaultdict(list) # columndata bokeh needs a list
        self.domains = defaultdict(dict)
        self.goals = defaultdict(dict)
        self.means = defaultdict(dict)
        self.my_approach = defaultdict(dict)
        self.content_to_me = defaultdict(dict)

        self.naming_convention = {}

        print("Initializing done")
        self.fill_naming_convention()
        self.fill_dicts()

    def fill_naming_convention(self):
        for i in self.naming_convention_csv:
            self.naming_convention[i[1]] = i[0]

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
                        self.human_factor[i[0]].append(float(i[column_val + 28])) 
                    except:
                        self.human_factor[i[0]].append(float(0)) 
                        continue
                    # try:
                    #     self.human_factor[i[0]][ri] = float(i[column_val + 28]) # dict method
                    # except:
                    #     continue
                else:
                    self.human_factor[i[0]].append(float(0)) 

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

nowhere_metadata = NOWHERE()