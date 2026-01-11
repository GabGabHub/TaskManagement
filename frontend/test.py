USERS = [
  {
    "id": "694ac1a3bfaf84e156136e00",
    "username": "Gab",
    "role": "admin",
    "joinedAt": "2025-12-23T16:21:55.173000"
  },
  {
    "id": "694ac1a3bfaf84e156136e01",
    "username": "Alex",
    "role": "user",
    "joinedAt": "2025-12-23T16:21:55.173000"
  },
  {
    "id": "694ae0f74d7a1d551f6b58a1",
    "username": "string",
    "role": "user",
    "joinedAt": "2025-12-23T18:35:35.097000"
  }
]

username = "Gab"

# if not username:
#     print("Username cannot be empty.")

# if username in [x['username'] for x in USERS]:
#     user = USERS['username']
#     print(f"Welcome back, {user['username']} ({user['role']})!", user)
# else:
#     user = {"username": username, "role": "user"}
#     USERS.append(user)
#     print(f"User {user['username']} created with role '{user['role']}'.", user)

if username in [x['username'] for x in USERS]:
    for user in USERS:
        if user['username'] == username:
            pula = user

print(pula)