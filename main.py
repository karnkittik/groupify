from database.database import DB

from services.user import UserService
# from services.group import GroupService


# get mac address from pawin
mac_address = 'mac address'

db = DB()
db.destroy_table()
db.init_table()

UserService.initMe(mac_address, 'Firstname', 'Lastname', 'Engineering', 1)

print(UserService.getProfile())
UserService.updateProfile('Me', 'LastMe', 'Engineering', 1)
print(UserService.getProfile())
print(UserService.getAvailableUser())
