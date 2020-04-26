# %%
import robin_stocks as rs

username = input("enter username here")
password = input("enter password here")

# %%
auth_info = rs.authentication.login(username = '<>', password= '<>')

# %%
if auth_info['expires_in'] > 0: 
    print("Authenticated")

# %%
auth_info

# %%
