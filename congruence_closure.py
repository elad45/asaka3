class congruenceClosure:
    def __init__(self,cube):
        # Initalize list of lists
        self.groups = []
        self.cube = cube
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
    def solve(self):
        self.parse_cube()
        top_level_Changed = True
        #while top_level_Changed:
        top_level_Changed = self.top_level()
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
        hasChanged = True

        had_any_change = False
        while hasChanged:
            hasChanged = False
            merged_lists = []
            element_to_list_map = {}
            groups_copy = self.groups.copy()
            for inner_list in groups_copy:
                # Find common elements and merge lists
                common_elements = [element for element in inner_list if element in element_to_list_map]
                if common_elements:
                    # Merge lists with common elements
                    merged_list = sum((element_to_list_map[element] for element in common_elements), inner_list)

                    # Update element_to_list_map with merged_list
                    for element in merged_list:
                        element_to_list_map[element] = merged_list

                    # Remove old lists from element_to_list_map
                    for element in common_elements:
                        del element_to_list_map[element]
                    hasChanged = True
                    had_any_change = True
                else:
                    # Add new list to element_to_list_map
                    for element in inner_list:
                        element_to_list_map[element] = inner_list

            # Remove duplicates from merged lists
            for inner_list in element_to_list_map.values():
                unique_list = list(dict.fromkeys(inner_list))
                if unique_list not in merged_lists:
                    merged_lists.append(unique_list)
            print(merged_lists)
            self.groups = merged_lists
        return had_any_change