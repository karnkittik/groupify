import setup
import GUI_ALL.gui as ui
from database.database import DB

from services.user import UserService
from services.group import GroupService


# get mac address from pawin
mac_address = setup.mac

DB.destroy_table()
DB.init_table()

UserService.initMe(mac_address, '', '', '', 1)
# UserService.addUser('mac address2', 'Pawin', 'Piemthai', 'Eng', 4)
# UserService.addUser('mac address3', 'Nathawan', 'Siripokasupkul', 'Eng', 4)

print(UserService.getAvailableUser())


# Set up UI
ui.initUI()
