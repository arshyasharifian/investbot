# Day Trading Bot
automating day trading with Python and a Robinhood API wrapper

**DISCLAIMER:
This algorithm WILL EXECUTE TRADES on your robinhood account. There are significant finanicial and tax implications. By using this github repo, users assume all risks associated with the trades made by this algorithm. We are not liable for any consequences related to or caused by the code in this repository.**

Before using this repository, please read the following medium articles which describes the issues and risks associated with this project.

Steps:

1. Pip install the dependencies which are listed at the top of *main.ipynb* (these are always changing so that is why I am referring to the main).
2. Enter your robinhood credentials here (note: you may have to enter an authenication code sent to you by Robinhood):
  ```
  get_header = rh_auth(username='', password='')
  ```
3. Since I am filtering stocks by "recent news" and recent news is timestamped in UTC, I subtract 7 hours for the time because I am in PST. You should subtract the time accordingly.

**The code assumes there is a $25K in the user's Robinhood account.** By default, the algorithm uses the difference between your buying power and $25K. For example, if a user has $26K in their Robinhood account, this algorithm will trade with $26K-$25K = $1K. To day trade legally, robinhood users must have $25K at the close of each trade day. You can read more about the rules for day trading [here](https://robinhood.com/us/en/support/articles/pattern-day-trading/). 

Ignore any cloud references made in the functions or print statements. We were using cloud as storage for the file outputs, but now the stock purchase list is a local CSV file. 

Also there are still bugs in the code. You should be able to see all the outstanding issues we are actively working to fix in the projects tab of this repository. 

Main Contributors:
- Arshya "Ary" Sharifian
- Gabriel Jai



