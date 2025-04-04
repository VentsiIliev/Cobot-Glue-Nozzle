from API.shared.user.UserService import UserService
from API.shared.user.CSVUsersRepository import CSVUsersRepository
from API.shared.user.User import User, Role, UserField
import os

filePath = os.path.join(os.path.dirname(__file__), "GlueDispensingApplication", "storage", "users.csv")
userFileds = [UserField.ID, UserField.FIRST_NAME, UserField.LAST_NAME, UserField.PASSWORD, UserField.ROLE]
userRepository = CSVUsersRepository(filePath, userFileds, User)
userService = UserService(userRepository)
user = User(2, "Name1", "Name2", "password", Role.ADMIN)
result = userService.addUser(user)
if result:
    print(f"User {user} added successfully.")
else:
    print(f"User {user} could not be added.")
user = userService.getUserById(2)
print(f"User: {user}")

# newUserfilePath = os.path.join(os.path.dirname(__file__), "GlueDispensingApplication", "storage", "newUsers.csv")
# newUserFields = [UserField.ID, UserField.FIRST_NAME]
# newUserRepository = CSVUsersRepository(newUserfilePath, newUserFields, NewUser)
# newUserService = UserService(newUserRepository)
# newUser = NewUser(2, "Name")
# newResult = newUserService.addUser(newUser)
# if newResult:
#     print(f"User {newUser} added successfully.")
# else:
#     print(f"User {newUser} could not be added.")
