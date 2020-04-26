# %%
import robin_stocks as rs
username = input("Enter your RH username")
password = input("Enter your RH password")
# %%
auth_info = rs.authentication.login(username = '<>', password= '<>')

# %%
if auth_info['expires_in'] > 0: 
    print("Authenticated")

# %%
auth_info

# %%
