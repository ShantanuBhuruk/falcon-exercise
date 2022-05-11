import falcon


class UserRepository:
    user_accounts = {
        "shantanu": "password"
    }

    user_ids = {
        "shantanu": 2
    }

    def is_user_valid(self, username, password):
        print("Username: {} and Password: {}".format(username, password))
        if username not in self.user_accounts or self.user_accounts[username] != password:
            return False
        else:
            return True

    def get_user_id(self, username):
        return self.user_ids[username]

    def get_user_by_id(self, user_id):
        user = None
        for k, v in self.user_ids.items():
            if v == user_id:
                user = k
                break
        if user:
            return user
        else:
            raise falcon.HTTPUnauthorized("Unauthorized", "User Not Found... :(")


def main():
    pass


if __name__ == "__main__": main()
