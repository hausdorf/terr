# CS 5340 NLP Final project

*Authors:* Vishay Vanjani, Alex Clemmer

## Running the Project

This should happen in 3 steps. We've tested it on CADE machine 1-11, using Python 2.6.

1. **GET DATA.** The first thing you need to do is to move NLTK's data into your `~/nltk_data/` folder. This is *VERY IMPORTANT*, because it must be in that EXACT DIRECTORY for the chunker and pos taggers to run. Unfortunately, the CADE machines do not come with it by default, so we've set up a script for you:

    ./nltk_data.sh

Once you execute this script, a GUI will pop up. It will give you options about which package to download. Choose the option that downloads all the stuff mentioned in the book. THIS WILL AUTOMATICALLY DUMP THIS DATA INTO YOUR `~/nltk_data/` DIRECTORY.

2. **RUN OUR SYSTEM.** This take A LONG TIME --- maybe 30 minutes. We've set up a script for you that does this automatically for the test data:

    ./run_test.sh

This script runs PYTHON 2.6. THIS IS REQUIRED. NO OTHER PYTHON VERSION WILL DO. The data is run over the file `test_aggregate`. If you would like to run it over your own data, run:

    python26 infoextract2.py [filename]

In general, this will produce a trace file called `$FILENAME.templates`, which contains our outputted answers. This can be used directly with the grading script.

3. GRADE OUR SYSTEM. If you've run our system over the default data, get the results by running:

    ./eval_test.sh

This just runs the class perl script over the default output files made by our system. However, if you'd like to run it over the output of some data other than the given data, simply execute the perl script as usual.


