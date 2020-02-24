import datetime
from psychopy import clock, core, event, logging, visual
from pandas import read_csv

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define useful functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def QuitTask():
    """Close PsychoPy and associated windows."""
    W.mouseVisible = True
    W.close()
    core.quit()

def CheckForEscape():
    """Check for 'escape' key."""
    KeyPress = event.getKeys(keyList=['escape'])
    if KeyPress: QuitTask()
    event.clearEvents()

def TextTrial(stimulus, text, time, keyList):
    """Present text to participant."""

    ## Update text.
    stimulus.setText(text)
    stimulus.draw()

    ## Draw text.
    W.logOnFlip(level=logging.EXP, msg='Stimulus: '+text)
    TimeStamp = W.flip()

    ## Wait for response.
    timer = clock.CountdownTimer(time)

    KeyPress = None
    while timer.getTime() > 0:

        if not KeyPress:

            KeyPress = event.getKeys(keyList=keyList)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load experiment data from CSV.
experiment = read_csv('msit.csv')

## Define valid key presses.
keyList = ['escape', '1', '2', '3']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Request subject ID.
msg = 'Initializing MSIT task.\n\nPlease enter subject ID.\n'
f = input(msg)

## Open window.
W = visual.Window(fullscr=False, units='norm', color=[-1,-1,-1], autoLog=False)
W.mouseVisible = False

## Initialize text.
stimulus = visual.TextStim(W, "+", color='#FFFFFF')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Wait for scanner.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## Before advancing to task, wait for scanner to
## send TTL pulse. To abort task, hit 'escape' key.

waiting = visual.TextStim(W, text='Waiting for scanner...', autoLog=False)
waiting.draw()
W.flip()

KeyPress, = event.waitKeys(keyList=['equal','escape'])
if KeyPress == 'escape': QuitTask()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Task.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## Run the task. To abort task, hit 'escape' key.

## Initialize logging.
dt = datetime.datetime.now().strftime('%Y_%m_%d_%H%M')
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
logging.LogFile('%s-MSIT-%s.log' % (f, dt), level=logging.EXP, filemode='w')

## Run task.
for _, trial in experiment.iterrows():

    TextTrial(stimulus, trial.text, trial.time, keyList)

## Quit.
logging.log(level=logging.EXP, msg='Done')
QuitTask()
