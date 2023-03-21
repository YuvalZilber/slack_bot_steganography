from impl.auth import SLACK_TOKEN, SIGNING_SECRET
from slacker import run
from impl.steganography_commands import *

run(SLACK_TOKEN, SIGNING_SECRET)
