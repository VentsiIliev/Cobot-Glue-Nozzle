from enum import Enum
from abc import ABC, abstractmethod

class Role(Enum):
    ADMIN = "Admin"
    OPERATOR = "Operator"

class UserField(Enum):
    ID = "id"
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"
    PASSWORD = "password"
    ROLE = "role"

# Abstract class to ensure all users have an 'id' field
class AbstractUser(ABC):
    def __init__(self, id):
        """
        Enforces that all subclasses must have an 'id' field.
        """
        if not id:
            raise ValueError("ID must be provided")
        self.id = id

    @abstractmethod
    def __eq__(self, other):
        pass

class BaseUser(AbstractUser):
    def __init__(self, id):
        super().__init__(id)

    def __eq__(self, other):
        return self.id == other.id

# Subclass User must call super().__init__(id) to ensure 'id' is set
class User(BaseUser):
    def __init__(self, id, firstName, lastName, password, role):
        # Enforce 'id' by calling the AbstractUser's constructor
        super().__init__(id)
        self.firstName = firstName
        self.lastName = lastName
        self.password = password  # TODO: Hash password before storing
        self.role = role

    def __str__(self):
        return f"ID: {self.id} {self.firstName} {self.lastName} ({self.role})"

    def __eq__(self, other):
        return self.id == other.id

# NewUser class also inherits from AbstractUser, so 'id' must be passed and enforced
class NewUser(BaseUser):
    def __init__(self, id, firstName):
        # Enforce 'id' by calling the AbstractUser's constructor
        super().__init__(id)
        self.firstName = firstName
        # self.lastName = lastName
        # self.password = password
        # self.role = role

    # def __str__(self):
    #     return f"ID: {self.id} {self.firstName} {self.lastName} ({self.role})"

    def __eq__(self, other):
        return self.id == other.id
