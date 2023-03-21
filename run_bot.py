from auth import SLACK_TOKEN, SIGNING_SECRET
from packs.slacker import run
from steganography_commands import *

run(SLACK_TOKEN, SIGNING_SECRET)
