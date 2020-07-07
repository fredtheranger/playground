#!/usr/bin/env python3

from aws_cdk import core

from playground.playground_stack import PlaygroundStack

app = core.App()
PlaygroundStack(app, "playground", env=core.Environment(region='us-west-1'))

app.synth()
