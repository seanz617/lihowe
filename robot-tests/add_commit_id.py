import os,sys,datetime
from bs4 import BeautifulSoup

branch = sys.argv[1]
commit_id = sys.argv[2] 

soup = None
with open("./report.html", 'r') as html_doc:
    soup = BeautifulSoup(html_doc, "html.parser")

if soup != None:
    summary = soup.find(attrs={"id":"summaryTableTemplate"})
    summary_info = summary.string
    commit_id_info = "<table class=\"details\"> <tr><th>Branch:</th> <td>{}</td></tr> <tr><th>Commit ID:</th><td>{}</td></tr>".format(branch,commit_id)
    summary.string = summary_info.replace("<table class=\"details\">",commit_id_info)

    with open("./report.html", 'w') as html_doc:
        html_doc.write(soup.prettify())
