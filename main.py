import setup
import GUI_ALL.gui as ui


from services.user import UserService
from services.group import GroupService


# get mac address from pawin
mac_address = setup.mac


# UserService.initMe(mac_address, '', '', '', 1)
# UserService.addUser('mac address2', 'Pawin', 'Piemthai', 'Eng', 4)
# UserService.addUser('mac address3', 'Nathawan', 'Siripokasupkul', 'Eng', 4)

# print(UserService.getAvailableUser())


# Set up UI
ui.initUI()
