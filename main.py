import requests
token = 'user_token'
username = 'marciocl'
class User:
    def __init__(self, user: str) -> None:
        self.user = user

    def _get_user_from_api(self) -> dict:
        return requests.get(f'https://api.github.com/users/{self.user}/followers', auth=(username,token)).json()

    def list_users(self) -> list:
        return [user['login'] for user in self._get_user_from_api()]


class UserFriendRepositories:
    friends_of_friends = []

    def __init__(self, friends_list):
        self.friends_list = friends_list

    def get_friends(self):
        for friend in self.friends_list:
            url = f'https://api.github.com/users/{friend}/followers'
            [self.friends_of_friends.append(i['login']) for i in requests.get(url, auth=(username, token)).json()]


    def get_friend_of_friends_list(self):
        lista = self.friends_of_friends
        for i in lista:
            yield i


    def get_friends_repositories(self, friend):
        repos_url = f'https://api.github.com/users/{friend}/repos'
        for i in requests.get(repos_url, auth=(username, token)).json():
            print(i['name'])

user  = User('marciocl')
user_list = user.list_users()

friends = UserFriendRepositories(user_list)
friends.get_friends()
friend = friends.get_friend_of_friends_list()
for i in range(5):
    friends.get_friends_repositories(next(friend))
