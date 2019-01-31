from flask import Flask, jsonify, render_template, request, send_file, json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from ransom_calc import ransom_calc
from utilities import csv_parser,to_list,output_parser,theta
import os
import matplotlib.pyplot as plt
import uuid
import base64
import numpy as np
import pdb, datetime

DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
unique = uuid.uuid1()


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route('/', methods = ['GET','POST'])
def my_page():                
    return render_template('_layout.html')

@app.route('/submit_form', methods = ['GET','POST'])
def submit_form():
    
    if request.method == 'POST':
        
        example = []
        
        if 'upload-1' in request.files:
            usr_def_ind = csv_parser(request.files['upload-1'].read())
        else:
            usr_def_ind = ['']
        if 'upload-2' in request.files:
            usr_def_biz = csv_parser(request.files['upload-2'].read())
        else:
            usr_def_biz = ['']
        
        population = request.form['targetPopulation']
        ransom_type = request.form['ransomType']
        discrim_method = request.form['priceDiscriminationType']
        ransom = to_list(request.form['ransomValues'])
        price_brackets = to_list(request.form['priceBrackets'])
        fixed_costs = to_list(request.form['fixedCosts'])
        handling_costs = to_list(request.form['handlingCosts'])
        
        example.append(request.form['example1'])
        example.append(request.form['example2'])
        example.append(request.form['example3'])
        example.append(request.form['example4'])
        example.append(request.form['example5'])        
        
        if fixed_costs == None:
            fixed_costs = [0]  
			
        print(discrim_method)

        if discrim_method == 'pop_type' and population != 'all':
            discrim_method = 'no_choice'	

        print(discrim_method)			

        if handling_costs == None:
            handling_costs = [0]

        for i in ransom:
            if i == '':
                i = 0
            
        # if no errors, run ransom_calc.py and push vars to results page/frame
        n,TR,qp,optTR,oqp,opt_r,e_n,e_TR,e_qp,example_mal_names,mal_name,e_r,e_c,e_tm,e_pm,e_dm,e_optTR,e_oqp,e_opt_r = ransom_calc(usr_def_ind,usr_def_biz,population,ransom_type,
                                                                                         discrim_method,ransom,price_brackets,fixed_costs[0],
                                                                                         handling_costs[0],example)

        e_results = []
        yourMal = []

        if ransom_type == 'fixed':
            PR = TR-fixed_costs
            optPR = optTR-fixed_costs
            score = (PR/n)*(1-qp)
            optScore = (optPR/n)*(1-oqp)
        elif ransom_type == 'discriminatory':
            PR = sum(TR)-fixed_costs
            optPR = sum(optTR)-fixed_costs
            score = (PR/sum(n))*(1-(sum(qp)/len(qp)))
            optScore = (optPR/sum(n))*(1-(sum(oqp)/len(oqp)))        

        optimality = PR/optPR

        yourMal.append('Malware = ' + mal_name)
        yourMal.append('Population = ' + population)
        yourMal.append('Pop Size = ' + str(n))
        yourMal.append('Ransom Value(s) = ' + str(ransom))
        yourMal.append('Ransom Type = ' + ransom_type)
        yourMal.append('Discrimination Type = ' + discrim_method)
        yourMal.append('Cost = ' + str(fixed_costs))
        yourMal.append('Revenue = ' + str(TR))
        yourMal.append('Total Profit = ' + str('%.2f' % PR))
        yourMal.append('Size of paying pop (proportional) = ' + str(qp))
        yourMal.append('Optimality = ' + str(optimality))
        yourMal.append('Threat-level = ' + str(score))
        yourMal.append('Optimal Revenue = ' + str(optTR))
        yourMal.append('Optimal Profit = ' + str('%.2f' % optPR))
        yourMal.append('Size of optimal paying pop (proportional) = ' + str(oqp))
        yourMal.append('Optimal Ransom(s) = ' + str(opt_r))
        yourMal.append('Threat-level of Optimal Ransom = ' + str(optScore))

        for i in range (0,len(example_mal_names)):                     
            e_results = output_parser(e_n[i],e_TR[i],e_qp[i],example_mal_names[i],e_r[i],e_c[i],e_tm[i],e_pm[i],e_dm[i],e_optTR[i],e_oqp[i],e_opt_r[i])
            yourMal.append('------------------------------------------------------')
            for j in e_results:
                yourMal.append(j)

        # output graph, which is used in the localhost:5000 client to populate the results modal
        unique = uuid.uuid1()
        now = datetime.datetime.now()
        prepend = (str(now.year) + '_' + str(now.month) + '_' + str(now.day) +
                   '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second) + '_')
        image = prepend+str(unique)+'.png'
        img_directory = "static/results/graphs/"
        plt.savefig(img_directory+image)
        plt.close()

        # output report.txt
        txt_directory = "static/results/reports/"
        file_name = txt_directory+prepend+str(unique)+'.txt'
        report = open(file_name,'w')
        for i in yourMal:
            report.write(i+'\n')
        report.close()

        with open(img_directory+image, "rb") as image_file:
            decoded_string = base64.b64encode(image_file.read()).decode()
                
    return jsonify(success=True,imageName=decoded_string,myResultsString=yourMal)

if __name__ == "__main__":
    app.run()
