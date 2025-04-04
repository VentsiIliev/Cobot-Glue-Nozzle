from API.shared.user.User import UserField
from API.shared.database.repositories.csvRepository.BaseCSVRepository import BaseCSVRepository
from API.shared.user.User import AbstractUser
import traceback


class CSVUsersRepository(BaseCSVRepository):
    def __init__(self, filepath, userFields, user_class):
        """
        Initialize CSV repository with dynamic user fields and user class type.
        :param filepath: Path to the CSV file
        :param userFields: List of fields (from UserField enum)
        :param user_class: The user class to use for creating users
        """

        if not issubclass(user_class, AbstractUser):
            raise ValueError("The user_class must be a subclass of AbstractUser")

        self.userFields = {}
        for field in userFields:
            self.userFields[field.name] = field.value

        # Store the user class type for later use
        self.user_class = user_class

        # Ensure column names passed to the base class are the enum names (upper case)
        super().__init__(filepath, list(self.userFields.keys()))  # Use enum names (uppercase names)

    def get_all(self):
        users = []
        df = self.get_data()

        if df.empty:
            return users

        for _, row in df.iterrows():
            # Dynamically map CSV columns to user attributes using the userFields dictionary
            user_data = {self.userFields[key]: row[key] for key in self.userFields}

            # Use the passed user class type to create the user instance
            users.append(self.user_class(**user_data))

        return users

    def get(self, user_id):
        df = self.get_data()
        print(f"Columns in CSV: {df.columns}")  # Debugging

        # Dynamically get the ID column using the UserField enum (dynamically)
        id_column = self.userFields[UserField.ID.name].upper()  # Make sure it's uppercase to match CSV
        print(f"ID column: {id_column}")  # Debugging
        row = df[df[id_column] == user_id]

        if not row.empty:
            row = row.iloc[0]
            # Dynamically map userData based on enum names
            user_data = {self.userFields[key]: row[key] for key in self.userFields}
            print(f"User data: {user_data}")  # Debugging

            # Use the passed user class type to create the user instance
            return self.user_class(**user_data)

        return None

    def insert(self, user):
        print(f"Inserting user: {user}")
        try:
            if self.get(user.id) is None:
                # Dynamically map user data using the userFields mapping
                user_data = {key: getattr(user, self.userFields[key]) for key in self.userFields}

                # Ensure that all fields are in the userData dictionary
                print(f"User data to insert: {user_data}")  # Debugging

                # Ensure that all required fields are in the CSV file
                for field in self.userFields:
                    if field not in user_data:
                        raise ValueError(f"Missing required field: {field}")

                # Map back to the enum names
                user_data = {field: user_data[field] for field in self.userFields}
                print(f"User data to insert after mapping: {user_data}")  # Debugging

                super().insert(**user_data)
                return True
            else:
                print(f"User {user.id} already exists.")
                return False
        except Exception as e:
            print(f"Error inserting user: {e}")
            traceback.print_exc()
            return False

    def delete(self, user_id):
        super().delete(user_id)

    def update(self, updated_users):
        df = self._read_rows()
        id_column = self.userFields[UserField.ID.name]  # Dynamically getting the column name based on enum

        for index, row in df.iterrows():
            for updated_user in updated_users:
                if row[id_column] == updated_user.id:
                    for key in self.userFields:
                        df.at[index, key] = getattr(updated_user, self.userFields[key])

        super().update(df)

    def get_data(self, filters=None):
        """Retrieve filtered data based on given criteria."""
        return super().get_data(filters)
