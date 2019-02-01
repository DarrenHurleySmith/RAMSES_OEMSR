# RAMSES_OEMSR
Optimal Model of Ransomware Calculation Tool

    1. Select an appropriate directory on your machine
    2. git clone https://github.com/DarrenHurleySmith/RAMSES_OEMSR.git

As a Python 3 program, the OEMSR requires that you have Python 3.x installed. It also requires the following modules, installed using pip:

    • Flask

    • Wtforms

    • Matplotlib

    • Scipy

    • Numpy

    • python-tk

These can all be installed using the following instruction from commandline (assuming pip and Python 3 are installed):
	> py -3 -m pip install flask wtforms matplotlib scipy numpy
Once installed, you are ready for your first run of the OEMSR. 

To run the OEMSR, please ensure you have command prompt running at all times and use an appropriate browser. We recommend Firefox or Chrome, both of which have been tested with our front-end implementation. 
To start the localhost:5000 server, type the following into command prompt and hit enter:
> py -3 model_front.py
This will elicit the response:
* Restarting with stat
 * Debugger is active!
 	* Debugger PIN: 183-445-163
 	* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
This means that your OEMSR server is running. Go to your selected browser and navigate to localhost:5000. This will take you to the OEMSR homepage, the default selections page for ransomware and population definitions. You are now ready to define and analyse your first malware example. 

Consult the pdf manual for further instructions and a detailed breakdown of the tool capabilities. 
