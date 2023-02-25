#!/usr/bin/env python3

import aws_cdk as cdk

from the_better_gifter_api.the_better_gifter_api_stack import TheBetterGifterApiStack


app = cdk.App()
TheBetterGifterApiStack(app, "the-better-gifter-api")

app.synth()
