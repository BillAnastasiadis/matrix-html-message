import json
import os
from datetime import datetime, timedelta
from inspect import getmembers, isfunction

steps = os.environ['step_context']
job = os.environ['job']
repo_url = "https://github.com/" + os.environ['gh_repo']
run_url = "https://github.com/" + os.environ['gh_repo'] + "/actions/runs/" + os.environ['run_id']
steps = json.loads(steps)
results = ""
for step, values in steps.items():
    if values['outcome'] == "failure":
        if results == "":
            results += "<p><b>There are failures in the Github Actions pipeline for repo " + \
                       "<a href=\"" + repo_url + "\">" + os.environ['gh_repo'] + "</a></b></p>"
            results += "<table><tr><th>Job</th><th>Step</th><th>Country</th></tr>"
        results += "<tr><td><a href=\"" + run_url + "\">" + job + \
                   "</td><td>" + step + " </td><td>FAILED</td></tr>"
if not results or len(results) < 1:
    print("Backlog is cool, yo")
    exit(0)
print(results)
exit(0)
