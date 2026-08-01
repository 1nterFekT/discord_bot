from database.registration import *
from database.transactions import *
from database.user import User

# register_server(1)
# register_user(222, 1)
# register_user(333, 1)

user_1 = User(222, 1)
user_2 = User(333, 1)

user_1.set_currency(15499)
user_2.set_currency(15499)

print("222 balance", user_1.get_balance())
print("333 balance", user_2.get_balance())

print("trying to transfer", transfer(1, 222, 333, 15499, "test"))
