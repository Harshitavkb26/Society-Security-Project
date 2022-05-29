from flask import Flask, render_template, request, redirect,send_from_directory
import main as pro
import importlib as il
import json
from fpdf import FPDF
import pdfkit
import cv2
from datetime import datetime

app = Flask(__name__)
securityApp = pro.FaceID()
wg="winga"
counter=0
fix=0
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/winga", methods=["GET", "POST"])
def wingsA():
    wg="winga"
    securityApp.main(1,"winga")
@app.route("/wingb", methods=["GET", "POST"])
def wingsB():
    wg="wingb"
    securityApp.main(1,"wingb")

@app.route("/wingc", methods=["GET", "POST"])
def wingsC():
    wg="wingc"
    securityApp.main(1,"wingc")



@app.route("/createPDF")
def generatePDF():
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-bottom': '0.75in',
        'margin-right': '0.75in',
        'margin-left': '0.75in',
    }

    result_wingA = securityApp.fetchSQLData("winga")

    result_wingB = securityApp.fetchSQLData("wingb")

    result_wingC = securityApp.fetchSQLData("wingc")

    result_knownmembers = securityApp.fetchSQLData("knownmembers")
    
    # header = """
    #     <html>
    #         <head>
    #             <style>
    #                 table, th, td {
    #                     border: 1px solid black;
    #                 }
    #                 th, td {
    #                     padding-left: 10px;
    #                 }
    #                 body {
    #                     width: 100%;
    #                 }
    #                 table {
    #                     width: 98%;
    #                 }
    #                  h2   {text-align: center;}
    #             </style>
    #         </head>
    #          <body>


    #             <p id="date"></p>
    # <script>
    # document.getElementById("date").innerHTML = Date();
    # </script>
    # <h2>Society Record</h2>
    #  <h2>Wing A</h2>
    #                 <table>
    #                     <tr>
    #                         <th>Sr no.</th>
    #                         <th>Flatnumber</th>
    #                         <th>Name</th>
    #                         <th>Contact Number</th>
    #                         <th>Entry Time</th>

    #                     </tr>
    #     """
    # footer = """

    #             </table>
    #         </body>
    #     </html>
    #     <footer>
    #       <br>
    #       <br>
    #       <br>
    #       <br>
    #       <br>
    #       <br>
    #       <br>
           
    #     </footer>
    # """
    # body = ''
    # counter=0
    # for i in result_wingA:
    #     counter=counter+1
    #     body = body + f'<tr><td>{counter}</td><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>'

    # pdfkit.from_string(header+body+footer, 'WingA_record.pdf', configuration=config, options=options)
    # return render_template("index.html")





    
    if result_wingA:
        header = """
            <html>
                <head>
                    <style>
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding-left: 10px;
                        }
                        body {
                            width: 100%;
                        }
                        table {
                            width: 98%;
                        }
                        h2   {text-align: center;}
                    </style>
                </head>
                <body>


                    <p id="date"></p>
        <script>
        document.getElementById("date").innerHTML = Date();
        </script>
        <h2>Society Record</h2>
        <h2>Wing A</h2>
                        <table>
                            <tr>
                                <th>Sr no.</th>
                                <th>Flatnumber</th>
                                <th>Name</th>
                                <th>Contact Number</th>
                                <th>Entry Time</th>

                            </tr>
            """
        footer = """

                    </table>
                </body>
            </html>
            <footer>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
           
            </footer>
        """
        body = ''
        counter=0
        for i in result_wingA:
            counter=counter+1
            body = body + f'<tr><td>{counter}</td><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>'

        pdfkit.from_string(header+body+footer, 'WingA_record.pdf', configuration=config, options=options)
        return render_template("index.html")
    if result_wingB:
        header = """
            <html>
                <head>
                    <style>
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding-left: 10px;
                        }
                        body {
                            width: 100%;
                        }
                        table {
                            width: 98%;
                        }
                        h2   {text-align: center;}
                    </style>
                </head>
                <body>


                    <p id="date"></p>
        <script>
        document.getElementById("date").innerHTML = Date();
        </script>
        <h2>Society Record</h2>
        <h2>Wing B</h2>
                        <table>
                            <tr>
                                <th>Sr no.</th>
                                <th>Flatnumber</th>
                                <th>Name</th>
                                <th>Contact Number</th>
                                <th>Entry Time</th>

                            </tr>
            """
        footer = """

                    </table>
                </body>
            </html>
            <footer>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
           
            </footer>
        """
        body = ''
        counter=0
        for i in result_wingB:
            counter=counter+1
            body = body + f'<tr><td>{counter}</td><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>'

        pdfkit.from_string(header+body+footer, 'WingB_record.pdf', configuration=config, options=options)
        return render_template("index.html")
    if result_wingC:
        header = """
            <html>
                <head>
                    <style>
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding-left: 10px;
                        }
                        body {
                            width: 100%;
                        }
                        table {
                            width: 98%;
                        }
                        h2   {text-align: center;}
                    </style>
                </head>
                <body>


                    <p id="date"></p>
        <script>
        document.getElementById("date").innerHTML = Date();
        </script>
        <h2>Society Record</h2>
        <h2>Wing C</h2>
                        <table>
                            <tr>
                                <th>Sr no.</th>
                                <th>Flatnumber</th>
                                <th>Name</th>
                                <th>Contact Number</th>
                                <th>Entry Time</th>

                            </tr>
            """
        footer = """

                    </table>
                </body>
            </html>
            <footer>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
           
            </footer>
        """
        body = ''
        counter=0
        for i in result_wingC:
            counter=counter+1
            body = body + f'<tr><td>{counter}</td><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>'

        pdfkit.from_string(header+body+footer, 'WingC_record.pdf', configuration=config, options=options)
        return render_template("index.html")
    if result_knownmembers:
        header = """
            <html>
                <head>
                    <style>
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding-left: 10px;
                        }
                        body {
                            width: 100%;
                        }
                        table {
                            width: 98%;
                        }
                        h2   {text-align: center;}
                    </style>
                </head>
                <body>


                    <p id="date"></p>
        <script>
        document.getElementById("date").innerHTML = Date();
        </script>
        <h2>Society Record</h2>
        <h2>Known Members</h2>
                        <table>
                            <tr>
                                <th>Sr no.</th>
                                <th>Flatnumber</th>
                                <th>Name</th>
                                <th>Contact Number</th>
                                <th>Entry Time</th>

                            </tr>
            """
        footer = """

                    </table>
                </body>
            </html>
            <footer>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
              <br>
           
            </footer>
        """
        body = ''
        counter=0
        for i in result_knownmembers:
            counter=counter+1
            body = body + f'<tr><td>{counter}</td><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>'

        pdfkit.from_string(header+body+footer, 'Known_Members_record.pdf', configuration=config, options=options)
        return render_template("index.html")
   

if __name__ == '__main__':
    app.run(debug=True)
