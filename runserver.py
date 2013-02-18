#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
from flask import Flask, Response


app = Flask(__name__)


def webcam_video_stream():
    command = ("gst-launch v4l2src device=/dev/video0 !"
               "'video/x-raw-yuv,width=640,height=480,framerate=30/1'"
               " ! jpegenc ! multipartmux boundary=spionisto ! "
               "filesink location=/dev/stdout")
    p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=-1,
                         shell=True)
    print("starting polling loop.")
    while(p.poll() is None):
        yield p.stdout.read(1024)


@app.route('/', methods=["GET"])
def index():
    return '<h1>Webcam with GStreamer+Flask</h1><img src="/webcam"/>'


@app.route('/webcam')
def webcam():
    return Response(webcam_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=--spionisto')

if __name__ == "__main__":
    app.debug = True
    app.run(port=9090)
