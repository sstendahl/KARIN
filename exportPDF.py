from __future__ import print_function
import pandas as pd
import helpfunctions
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def exportcsvtoPDF(self):
    path = helpfunctions.saveFileDialog(self)
    filename = path[0]
    if filename[-4:] != ".pdf":
        filename = filename + ".pdf"
    df = pd.read_csv("samplelist.csv")
    df.head()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("PDFtemplate.html")
    sample_list = df
    template_vars = {"sample_table": sample_list.to_html()}
    print(filename)
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(filename, stylesheets=["style.css"])