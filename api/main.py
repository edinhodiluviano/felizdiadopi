import random

from fastapi import FastAPI

from .model import Result
from . import db


app = FastAPI()


@app.get("/")
def root():
    return {}


@app.post("/input")
def input(result: Result):
    db.save(result)
    return {"Thank you ^.^": random_phrase()}


def random_phrase():
    phrases = [
        "Have a wonderful day!",
        "You make the world a better place.",
        "How are you so utterly fabulous?",
        "I hope you feel as good as you look!",
        "We’re all made of stardust, but your’s is extra sparkly.",
        "Today is already extra good.",
        "You raise everyone’s vibrations!",
        "You are #1!",
        "In case no one said it yet today, you’re great!",
        "Wow! You are doing a great job!",
        "If you ever sell your secret mojo recipe, I’ll buy a copy.",
        "Live loudly!",
        "You can start your day over whenever you want.",
        "Thank you for all that you do.",
        "The world is still beautiful.",
        "Love wildly!",
        "I’m so glad you were born!",
        "Wow! You look stunning today!",
        "In case of emergency: DANCE!",
        "You matter. A lot.",
        "Today will be fabulous.",
        "I was waiting for you.",
        "Don’t forget the little things!",
        "I can’t believe how amazing you already are.",
        "Caution: Contains Magic",
        "I’m so glad we get to be alive at the same time.",
        "This is a good week to have a good week.",
        "Smiling at strangers never goes out of style.",
        "Create your own happy place.",
        "You are beautiful.",
        "You do an amazing job of being you.",
        "Stop to take a minute and breathe.",
        "Throw kindness around like confetti.",
        "PERSIST!",
        "You’ve totally got this!",
        "Hello! Is it me you’re looking for?",
        "Love yourself first.",
        "Your weirdness is your super power.",
        "Keep searching for silver linings.",
        "You are always the best at something.",
        "Make magic everywhere.",
        "Do what you love more often.",
        "Kindness looks great on you!",
        "You’re a rock star!",
    ]
    return random.choice(phrases)
