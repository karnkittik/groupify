from database.database import DB

db = DB()
db.destroy_table()
db.init_table()


# class Node:
#     def __init__(self, username: str):
#         self.username = username


# me = Node('momo')

# groups = dict()  # List of group in network
# user = []  # List of node in network
