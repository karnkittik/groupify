from show_group import * 
from friend_list import *

##import logic part
all_group = all_group()
g1 = group("test1",2)
g1.add_member("a")
g1.add_member("b")
g2 = group("test2",2)
g2.add_member("x")
g2.add_member("y")
all_group.add_group(g1)
all_group.add_group(g2)


##inintial ui part
window =  Tk()
window.option_add("*Font", "helvetica 16")
top_frame = Frame()
top_frame.pack(side = LEFT)

second_frame = Frame()
second_frame.pack(side = LEFT)


# window.geometry('500x500')
window.title("GUI")

main_window = show_all_group(top_frame,all_group)
second_window = freind_list(second_frame)


while True:
    if main_window.all_group.is_change_to_view == True:
        main_window.refresh_list()
    window.update_idletasks()
    window.update()