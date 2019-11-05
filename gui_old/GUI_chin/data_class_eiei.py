class group:

    def  __init__(self, group_name,group_limit):
        self.group_name = group_name
        self.group_limit = group_limit
        self.group_member = list()

    def add_member(self,name):
       self.group_member.append(name)



class all_group:

    def __init__(self):
        self.list_of_all_group = list()
        self.is_change_to_view = False

    def get_alL_group_name(self):
        out = []
        for i in self.list_of_all_group:
            out.append(i.group_name)
        return out

    def get_group(self,index):
        return self.list_of_all_group[index]

    def add_group(self,group):
        self.list_of_all_group.append(group)
        self.is_change_to_view = True

    def del_group(self,group_index):
        self.list_of_all_group.pop(group_index)
        self.is_change_to_view = True
        

    def find_group(self,name):
        i = self.list_of_all_group.index(name)
        return i  
