The modules that this project uses that must be installed consist of django and scikit. Additionally, this project encourages the use of a virtual environment. Finally, this readme assumes you are using OSX, or a mac.

First make sure you are able to use pip. This is the fastest and easiest way to install all three modules.

To set up a virtual environment, go to terminal and type in "sudo pip install virtualenv". This will hopefully install the virtual environment for you. To set up a virtual environment, type "virtualenv ENV" followed by your desired environment name. To enter your virtual environment, type "source envname/bin/activate".

Within your environment, install django and scikit. Django can be installed with the command "pip install Django". Scikit can be installed with the command "pip install -U scikit-learn"

Finally, to set up the database. The database comes pre-installed, but if you wish you can wipe the data and input your own.
 If you have your own anime list, export it, and put it ideally within the source folder, but it doesn't matter as long as you have the path file. In get list.py, replace listname (line 26) with your own list. If you have an AniDB account, please replace username and password (lines 41 and 42 respectively with your own). Note that there is a probability that the default password will not work, as I will change it to my actual password shortly after term project. Next, go to admin -> users, and change "SACCFFT" to your own name, and replace your password WITH THE SAME ONE USED TO ACCESS ANIDB. Save, and you should be ready to go. If for any reason get list.py crashes, uncomment the last line of updatevector.py, run that, recomment the last line, and you should be good to go.

 Warning: Run get list.py sparingly. Not only does it take a long time bc 1 request every 2 seconds, I may get banned.
