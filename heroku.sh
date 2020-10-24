#!/bin/bash
gunicorn app:color-cone/app --daemon
python color-cone/worker.py