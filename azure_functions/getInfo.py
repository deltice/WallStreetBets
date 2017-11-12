import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'venv/Lib/site-packages')))

import ita
import json
from credentials import credentials

# postreqdata = json.loads(open(os.environ['req']).read())

client = ita.Account(credentials["invest_email"], credentials["invest_password"])
status = client.get_portfolio_status()
portfolio = client.get_current_securities()

values = {}
values["account value"] = status.account_val
values["annual return"] = status.annual_return
values["bought"] = portfolio.bought
values["short"] = portfolio.shorted

response = open(os.environ['res'], 'w')
response.write(json.dumps(values))
response.close()