import utils


class congruenceClosure:
    def __init__(self, cube):
        # Initalize list of lists
        self.groups = []
        self.cube = cube
        self.terms = utils.get_terms(cube)
        self.symbols = utils.get_function_symbols(cube)
        print(f"terms are: {self.terms}")
        print(f"symbols are: {self.symbols}")

    def parse_cube(self):
        for literal in self.cube:
            if literal.is_not():
                flag = False
                self.add_vars(literal, flag)
            elif literal.is_equals():
                flag = True
                self.add_vars(literal, flag)
            else:
                raise ValueError("invalid literal")
        print(f"groups are:{self.groups}")

    def solve(self):
        self.parse_cube()
        top_level_changed = True
        congruence_changed = True
        while top_level_changed or congruence_changed:
            top_level_changed = self.top_level()
            print(f"after top level groups are: {self.groups}")
            congruence_changed = self.congruence()
            print(f"after congruence groups are: {self.groups}")
    def get_groups(self):
        return self.groups

    def add_vars(self, literal, flag):
        if flag:
            var1, var2 = literal.args()
            self.groups.append([var1, var2])
        if not flag:
            literal = literal.args()[0]
            var1, var2 = literal.args()
            self.groups.append([var1])
            self.groups.append([var2])

    def top_level(self):
        for i in range(len(self.groups)):
            group1 = self.groups[i]
            for j in range(i+1, len(self.groups)):
                group2 = self.groups[j]
                common_elements = set(group1) & set(group2)
                if common_elements:
                    self.groups[i].extend(var for var in group2 if var not in group1)
                    self.groups.pop(j)
                    return True
        return False

    def map_elements_and_applications(self):
        dict_elements, dict_applications = {}, {}
        for symbol in self.symbols:
            # for element in self.terms:
            for i in range(len(self.groups)):
                for j in range(len(self.groups[i])):
                    element = self.groups[i][j]
                    if element.is_function_application() and element._content.payload == symbol:
                        if element in dict_applications:
                            dict_applications[element].add(i)
                        else:
                            dict_applications[element] = {i}
                    elif not element.is_function_application():
                        if element in dict_elements:
                            dict_elements[element].add(i)
                        else:
                            dict_elements[element] = {i}
        return dict_applications, dict_elements

    def congruence(self):
        dict_applications, dict_elements = self.map_elements_and_applications()
        # if a application is in two or more groups, we can union those groups
        for key in dict_applications:
            if len(dict_applications[key]) >= 2:
                i, j = list(dict_applications[key])[:2]
                self.groups[i].extend(element for element in self.groups[j] if element not in self.groups[i])
                self.groups.pop(j)
                return
        #print(f"dict applications: {dict_applications}")
        #print(f"dict_elements: {dict_elements}")
        # list of all applications with the symbol
        list_applications = [key for key in dict_applications.keys()]
        #print(f"list_applications: {list_applications}")

        for i in range(len(list_applications) - 1):
            args1 = [arg for arg in list_applications[i].args()]
            set1 = dict_applications[list_applications[i]]
            for j in range(i + 1, len(list_applications)):
                # check if they have a groups to union:
                set2 = dict_applications[list_applications[j]]
                if set1.symmetric_difference(set2):
                    args2 = [arg for arg in list_applications[j].args()]
                    #print(f"arg1: {args1}")
                    #print(f"arg2: {args2}")
                    # check if there exists a group contains all the arguments
                    isCommon = False
                    for arg1, arg2 in zip(args1, args2):
                        if arg1 in dict_elements and arg2 in dict_elements:
                            intersection_set = dict_elements[arg1].intersection(dict_elements[arg2])
                            if intersection_set:
                                isCommon = True
                            else:
                                isCommon = False
                    if isCommon:
                        self.groups[i].extend(element for element in self.groups[j] if element not in self.groups[i])
                        self.groups.pop(j)
                        return True
        return False
    # if len(list_of_applications) >= 2:
    #     print(list_of_applications)
    #     print(list_of_args)
