#!/bin/bash

#EAGER_CELERY=false celery -A quizitive  worker -B -E -l DEBUG
#EAGER_CELERY=false celery -A binocularslive  worker -E -l DEBUG
EAGER_CELERY=false celery -A binocularslive  worker -E -l DEBUG -Q serial
