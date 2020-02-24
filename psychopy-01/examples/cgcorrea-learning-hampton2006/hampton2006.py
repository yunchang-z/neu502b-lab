import os
import sys
import random
from psychopy import clock, core, event, logging, visual
from datetime import datetime


script_dir = os.path.dirname(os.path.abspath(__file__))


class Hampton2006(object):
    '''
    >>> env = Hampton2006(deterministic_reward=True, deterministic_reversal=True)
    >>> env.reset()
    >>> env.state = 0
    >>> env.seed(42)
    >>> env.step(0)
    (1, 0.25, False, {})
    >>> env.step(1)
    (0, -0.25, False, {})
    >>> [env.step(0) for _ in range(3)]
    [(1, 0.25, False, {}), (1, 0.25, False, {}), (1, 0.25, False, {})]
    >>> env.state
    0
    >>> env.step(0)
    (1, 0.25, False, {})
    >>> env.state
    1
    '''
    def __init__(self, logging=None, deterministic_reward=False, deterministic_reversal=False):
        self.action_space = range(2)
        # Observations: 0: Failure, 1: Success
        self.observation_space = range(2)
        # States: 0: Rewarded action is 0, 1: Rewarded action is 1
        self.state_space = range(2)
        self.rnd = random.Random()
        self.logging = logging
        self.deterministic_reward = deterministic_reward
        self.deterministic_reversal = deterministic_reversal
        self.num_reversals = 0

    def log(self, msg):
        if self.logging is not None:
            self.logging.log(level=self.logging.EXP, msg='Hampton2006: ' + msg)

    def seed(self, seed):
        self.rnd.seed(seed)

    def reset(self):
        self.state = self.rnd.choice(self.state_space)
        self.correct_count = 0
        self.num_reversals = 0
        return None

    def step(self, action):
        assert action in self.action_space
        # One stimulus was designated the correct stimulus in that choice of that stimulus
        # lead to a monetary reward (winning 25 cents) on 70% of occasions and a monetary
        # loss (losing 25 cents) 30% of the time.
        if action == self.state:
            self.correct_count += 1
            prob_reward = 0.7
        # The other stimulus was incorrect in that choice of that stimulus lead to a
        # reward 40% of the time and a punishment 60% of the time, thus leading to a
        # cumulative monetary loss.
        else:
            self.correct_count = 0
            prob_reward = 0.4

        if self.deterministic_reward:
            rewarded = action == self.state
        else:
            rewarded = self.rnd.random() < prob_reward

        if rewarded:
            observation = 1
            reward = +0.25
        else:
            observation = 0
            reward = -0.25

        self.log('Action={} State={} Rewarded={} CorrectCount={}'.format(
            action, self.state, rewarded, self.correct_count))

        # After having chosen the correct stimulus on four consecutive occasions,
        # the contingencies reversed with a probability of 0.25 on each successive trial.
        if self.correct_count >= 4 and (
            self.deterministic_reversal or
            self.rnd.random() < 0.25
        ):
            self.state = 1 if self.state == 0 else 0
            self.correct_count = 0
            self.num_reversals += 1
            self.log('Reversal')

        return observation, reward, False, {}


if __name__ == '__main__xxx':
    args = sys.argv[1:]

    if args[0] == 'test':
        import doctest
        doctest.testmod()
        print('Tests completed.')
        sys.exit(0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Define useful functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def getKeysOrQuit():
    keyPress = event.getKeys(keyList=keyList)
    if 'escape' in keyPress:
        QuitTask()
    return keyPress


def QuitTask():
    """Close PsychoPy and associated windows."""
    W.mouseVisible = True
    W.close()
    core.quit()


def CheckForEscape():
    """Check for 'escape' key."""
    keyPress = event.getKeys(keyList=['escape'])
    if keyPress:
        QuitTask()
    event.clearEvents()


def FixationBlock(sec):
    """Present fixation cross."""

    # Draw/log fixation cross.
    fix.draw()
    W.logOnFlip(level=logging.EXP, msg='Fixation cross')
    W.flip()

    # Wait.
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:

        # Check keys.
        CheckForEscape()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Define experiment.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Define valid key presses.
keyList = ['escape', '1', '2']

# Define practice variable.
is_practice = '--practice' in sys.argv

# Define RNG used for stim ordering
stim_order_rnd = random.Random()
seed = 54
stim_order_rnd.seed(seed)

# Initialize task
env = Hampton2006(
    logging=logging,
    deterministic_reward='--deterministic_reward' in sys.argv,
    deterministic_reversal='--deterministic_reversal' in sys.argv,
)
env.reset()
# Initialize task seed
env_seed = 43
env.seed(env_seed)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Preprations.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Request subject ID.
msg = 'Initializing Hampton2006 task.\n\nPlease enter subject ID.\n'
subject_id = input(msg)

# Open window.
W = visual.Window(
    size=(1920, 1080),
    fullscr=True,
    units='norm', color=[-1, -1, -1], autoLog=False)
W.mouseVisible = False

white = [1, 1, 1]
black = [-1, -1, -1]
blue = '#023EFF'  # [-1, -1, 1]
yellow = '#FFC400'  # [1, 1, -1]
green = '#1AC938'
red = '#E8000B'

leftpos = (-0.4, 0)
rightpos = (+0.4, 0)

rect_width, rect_height = 0.25, 0.25 * W.size[0] / W.size[1]

# Initialize fixation cross (used in FixationBlock).
fix = visual.GratingStim(
    W, mask='cross', pos=(0, 0), sf=0,
    size=(0.1, 0.1 * W.size[0] / W.size[1]),
    color=white)

# Initialize stimuli
stim0 = visual.Rect(
    win=W,
    units='norm',
    width=rect_width,
    height=rect_height,
    pos=leftpos,
    fillColor=blue,
    lineColor=black,
    lineWidth=30,
)

stim1 = visual.Rect(
    win=W,
    units='norm',
    width=rect_width,
    height=rect_height,
    pos=rightpos,
    fillColor=yellow,
    lineColor=black,
    lineWidth=30,
)

# Initialize text.
feedback_positive = visual.TextStim(
    W, "\u2713", color=green, height=1,
    pos=(0, 0))
feedback_negative = visual.TextStim(
    W, "\u00D7", color=red, height=1,
    pos=(0, 0))

cumulative_rew = 0.0
reward_text = visual.TextStim(
    W, text='', autoLog=False,
    pos=(0, 0.8))


def update_reward_text():
    reward_text.setText('${:.02f}'.format(cumulative_rew))


update_reward_text()

# Initialize logging.
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
logging.LogFile('Hampton2006-{}-{}.log'.format(datetime.now().isoformat(), subject_id), level=logging.EXP, filemode='w')

# Logging various details about experiment
logging.log(level=logging.EXP, msg='CLI args {}, ordering seed {}, task seed {}'.format(
    sys.argv, seed, env_seed,
))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Wait for scanner.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Before advancing to task, wait for scanner to
# send TTL pulse. To abort task, hit 'escape' key.

waiting = visual.TextStim(W, text='Waiting for scanner...', autoLog=False)
waiting.draw()
W.flip()

keyPress, = event.waitKeys(keyList=['equal', 'escape'])
if keyPress == 'escape':
    QuitTask()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Task.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Run the task. To abort task, hit 'escape' key.

FixationBlock(2)


def render(msg, leftmost, rewarded=None, action_selected=None):
    if leftmost == 0:
        stim0.pos = leftpos
        stim1.pos = rightpos
    elif leftmost == 1:
        stim1.pos = leftpos
        stim0.pos = rightpos

    if action_selected == 0:
        stim0.lineColor = white
        stim1.lineColor = black
    elif action_selected == 1:
        stim1.lineColor = white
        stim0.lineColor = black
    else:
        stim0.lineColor = black
        stim1.lineColor = black

    if rewarded is None:
        fix.draw()
    elif rewarded:
        reward_text.draw()
        feedback_positive.draw()
    else:
        reward_text.draw()
        feedback_negative.draw()

    if leftmost is not None:
        stim0.draw()
        stim1.draw()

    W.logOnFlip(level=logging.EXP, msg=msg)
    W.flip()


key_and_leftmost_to_action = {
    ('1', 0): 0,
    ('2', 0): 1,
    ('1', 1): 1,
    ('2', 1): 0,
}
actions = [0, 1]

num_trials = 100

# Run task.
for _ in range(num_trials):
    '''
    Each trial takes 5 seconds on average.
    - Display stimuli for [1, 2, or 3] seconds.
        - Highlight selected stimuli.
    - Display feedback for [2, 3, or 4] seconds.

    For 100 trials, we expect 500 seconds.
    With a TR of 1, this corresponds to 500 volumes.
    '''
    leftmost = stim_order_rnd.choice(actions)
    # Average of 2.0s
    stimulus_duration = stim_order_rnd.choice([1, 2, 3])
    # Average of 3.0s
    feedback_duration = stim_order_rnd.choice([2, 3, 4])

    # Render stimus
    render('stim presentation for duration {:.03f}. feedback duration {:.03f}'.format(
        stimulus_duration, feedback_duration), leftmost)
    keyPress = None
    action = None
    timer = clock.CountdownTimer(stimulus_duration)
    while timer.getTime() > 0:
        keyPress = getKeysOrQuit()
        if '1' in keyPress or '2' in keyPress:
            action = key_and_leftmost_to_action[keyPress[0], leftmost]
            render('stim select', leftmost, action_selected=action)
            break
    while timer.getTime() > 0:
        keyPress = getKeysOrQuit()

    # Render feedback
    if action is None:
        render('no response', leftmost=None)
    else:
        observation, reward, _, _ = env.step(action)
        cumulative_rew += reward
        update_reward_text()
        render('feedback', leftmost, action_selected=action, rewarded=observation == 1)

    timer = clock.CountdownTimer(feedback_duration)
    while timer.getTime() > 0:
        keyPress = getKeysOrQuit()

    '''
    # Render fixation for a blank screen
    render('only fixation', leftmost=None)

    timer = clock.CountdownTimer(1.0)
    while timer.getTime() > 0:
        keyPress = getKeysOrQuit()
    '''

    # End condition for practice rounds.
    if is_practice and env.num_reversals >= 3:
        logging.log(level=logging.EXP, msg='Ending practice due to {} reversals'.format(env.num_reversals))
        break

# Quit.
logging.log(level=logging.EXP, msg='Done. Final reward ${:0.2f}'.format(cumulative_rew))
QuitTask()
