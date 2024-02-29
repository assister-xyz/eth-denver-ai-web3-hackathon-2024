class Contributor:
    def __init__(self, stackoverflow_account_link):
        self.stackoverflow_account_link = stackoverflow_account_link
        self.unique_code = None
        self.verified = False

    def set_unique_code(self, unique_code):
        self.unique_code = unique_code

    def get_unique_code(self):
        return self.unique_code

    def get_verified(self):
        return self.verified

    def set_verified(self, verified):
        self.verified = verified

    def __str__(self):
        return f"StackOverflow Account Link: {self.stackoverflow_account_link}, Unique Code: {self.unique_code}, Verified: {self.verified}"