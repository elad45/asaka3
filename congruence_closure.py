import utils


class congruenceClosure:
    def __init__(self, cube):
        # Initalize list of lists
        self.terms = utils.get_terms(cube)
        self.groups = [[element] for element in self.terms]
        self.cube = cube
        self.symbols = utils.get_function_symbols(cube)
        self.core_lit = []
        self.core_ans = []
        self.core_var = []
        #print(f"groups are: {self.groups}")
        #print(f"symbols are: {self.symbols}")

    def top_level(self):
        for var1, var2 in self.core_var:
            for i in range(len(self.groups)):
                group1 = self.groups[i]
                for j in range(i + 1, len(self.groups)):
                    group2 = self.groups[j]
                    #split vars into var1 and var2
                    #common_elements = set(group1) & set(group2)
                    if (var1 in group1 and var2 in group2) or (var1 in group2 and var2 in group1):
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
        # print(f"dict applications: {dict_applications}")
        # print(f"dict_elements: {dict_elements}")
        # list of all applications with the symbol
        list_applications = [key for key in dict_applications.keys()]
        # print(f"list_applications: {list_applications}")

        for i in range(len(list_applications) - 1):
            args1 = [arg for arg in list_applications[i].args()]
            set1 = dict_applications[list_applications[i]]
            for j in range(i + 1, len(list_applications)):
                # TODO check if  i,j apply the same function
                if list_applications[i]._content.payload != list_applications[j]._content.payload:
                    continue
                # check if they have a groups to union:
                set2 = dict_applications[list_applications[j]]
                if set1.symmetric_difference(set2):
                    args2 = [arg for arg in list_applications[j].args()]
                    # print(f"arg1: {args1}")
                    # print(f"arg2: {args2}")
                    # check if there exists a group contains all the arguments
                    isCommon = False
                    for arg1, arg2 in zip(args1, args2):
                        if arg1 in dict_elements and arg2 in dict_elements:
                            intersection_set = dict_elements[arg1].intersection(dict_elements[arg2])
                            if intersection_set:
                                isCommon = True
                                break
                            else:
                                isCommon = False
                    if isCommon:
                        set1list = list(set1)
                        set1inx = set1list[0]
                        set2list = list(set2)
                        set2inx = set2list[0]
                        self.groups[set1inx].extend(
                            element for element in self.groups[set2inx] if element not in self.groups[set1inx])
                        self.groups.pop(set2inx)
                        return True
        return False

    def fail(self):
        for lit in self.cube:
            if lit.is_not():
                lit_parsed = lit.args()[0]
                var1, var2 = lit_parsed.args()
                for group in self.groups:
                    if var1 in group and var2 in group:
                        if lit not in self.core_lit:
                            self.core_lit.append(lit)
                        if lit not in self.core_ans:
                            self.core_ans.append(lit)
                        return True  # unsat
        return False  # sat

    def add_literal(self,literal):
        self.core_lit.append(literal)
        if literal.is_equals():
            var1, var2 = literal.args()
            self.core_var.append([var1, var2])
            self.core_ans.append(literal)
    def solve(self):
        for i in range(len(self.cube)):
            self.add_literal(self.cube[i])
            top_level_changed = True
            congruence_changed = True
            while top_level_changed or congruence_changed:
                top_level_changed = self.top_level()
                #if top_level_changed:
                    #print(f"after top level groups are:  {self.groups}")
                congruence_changed = self.congruence()
                #print(f"after congruence groups are: {self.groups}")
                #TODO it has to be inside the while block
                is_unsat = self.fail()
                if is_unsat:
                    return False, self.core_ans
        is_unsat = self.fail()
        if is_unsat:
            return False, self.core_ans
        return True, None
