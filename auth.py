# %%
import robin_stocks as rs

# %%
auth_info = rs.authentication.login(username = '<>', password= '<>')

# %%
if auth_info['expires_in'] > 0: 
    print("Authenticated")

# %%
auth_info

# %%
