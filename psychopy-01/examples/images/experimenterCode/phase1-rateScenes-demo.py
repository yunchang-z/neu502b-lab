#!/usr/bin/env python

''' phase1-rateScenes.py
------------------------------------
Updated: 11/27/2018, Paula P. Brooks
------------------------------------

Takes input (subject name) and "masterSceneList.xlsx" to launch phase 1 of TNT fMRI experiment.
Participants are asked to rate scenes on a 9-point SAM valence scale.

- 11/27/2018 = add variable to know running room number
- 11/27/2018 = make code more efficient (aka take away things we don't need) 
- 01/18/2019 = took away room number because running rooms have same screens!
- 01/31/2019 = made mouse invisible

'''

##############################################
###        SETUP FOR THE EXPERIMENT        ###
##############################################

#from time import time
import time
from psychopy import core, visual, data, logging, event
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
import pandas as pd
import os  # handy system and path functions
import sys  # to get file system encoding
import openpyxl # to interact with excel
import numpy as np

# Info about the experiment session & important variables
expName = 'phase1-rateScenes'
expInfo = {'subjName':sys.argv[1]}
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
time_ITI = 0.5
time_showScene = 5
ratingKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# Change working directory, and tell where things are
os.chdir("..")
filename = u'data/%s/%s_%s' % (expInfo['subjName'], expInfo['subjName'], expName) # check wd using os.getcwd()

# An ExperimentHandler that helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# Save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='pix')

win.mouseVisible = False

# Store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
    print('could get frameRate')
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
scene = visual.ImageStim(
    win=win, name='scene',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(381,381),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
valenceRating = visual.ImageStim(
    win=win, name='valenceRating',
    image='stim/valenceRatingScale.png', mask=None,
    ori=0, pos=(0, -400), size=(1089.36,163.02),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Set up how to do fixation
fixation = visual.TextStim(win=win, name='cross',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=100, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

##############################################
###             INSTRUCTIONS               ###
##############################################

## wait for participant keypress to start experiment
waiting = visual.TextStim(win, pos=[0, 0], text="Press any key to begin!",
                          name="Waiting",height=50,wrapWidth=1000,alignHoriz='center',alignVert='center')
waiting.draw()
win.flip()

wait = True
while wait:
    theseKeys = event.getKeys()
    # check for quit:
    if "escape" in theseKeys:
        win.close()
        core.quit()
    elif len(theseKeys) > 0:
        wait = False
            
##############################################
###             RATE THE SCENES            ###
##############################################

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('masterSceneList.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec('{} = thisTrial[paramName]'.format(paramName)) #exec(paramName + '= thisTrial.' + paramName)
        
for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec('{} = thisTrial[paramName]'.format(paramName)) # exec(paramName + '= thisTrial.' + paramName)

    # update component parameters for each repeat
    scene.setImage(sceneFile)
    response = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [scene, valenceRating, response]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
            
    ### ITI
    waitingOnset = time.time()
    while (time.time() - waitingOnset < time_ITI):
        fixation.draw()
        win.flip()
        # check for escape
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            endExpNow = True
            win.close()
            core.quit()
    
    ### Show the scene and rating scale
    scene.draw()
    valenceRating.draw()
    win.flip()
    actualOnset = time.time()
    
    noResponse = True
    while (time.time() - actualOnset < time_showScene) and noResponse == True:
        scene.draw()
        valenceRating.draw()
        win.flip()
        # check for escape
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            endExpNow = True
            win.close()
            core.quit()
        # check for rating response
        if len(np.intersect1d(theseKeys,ratingKeys)):
            response = theseKeys[-1]
            resp_rt = time.time() - actualOnset
            noResponse = False
            
    # if a response wasn't given in allotted time
    while noResponse == True:
        valenceRating.draw()
        win.flip()
        # check for escape
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            endExpNow = True
            win.close()
        # check for rating response
        if len(np.intersect1d(theseKeys,ratingKeys)):
            response = theseKeys[-1]
            resp_rt = time.time() - actualOnset
            noResponse = False
            win.flip()

    ### Ending routine for trial
    trials.addData('response',response)
    trials.addData('resp_rt',resp_rt)
    thisExp.nextEntry()
       
        
##############################################
###           WRAPPING THINGS UP           ###
##############################################

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

