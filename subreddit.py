#!/usr/bin/python
import praw
import re
import datetime
import sys
import boto3
import json
import time
import logging
import pandas as pd
import time
from datetime import datetime, timedelta

def process_or_store(subreddit):
    try:
        response = firehose_client.put_record(
            DeliveryStreamName='<insert-delivery-stream-name>',
            Record={
                'Data': (json.dumps(subreddit, ensure_ascii=False) + '\n').encode('utf8')
                    }
            )
        logging.info(response)
    except Exception:
        logging.exception("Problem pushing to firehose")


firehose_client = boto3.client('firehose', region_name="us-east-1")
LOG_FILENAME = '/tmp/reddit-stream.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

if len(sys.argv) >= 2:
    try:
        r = praw.Reddit('bot1')
        num_subreddits_collected = 0

        # build stream. add first subreddit to start.
        subreddits = sys.argv[1]
        for sr in sys.argv[2:]:
            subreddits = subreddits + "+" + sr

        subreddit_stream = r.subreddit('posts').hot(limit=100)

        for post in subreddit_stream():
            submissionsLast24 = []
        ml_subreddit = reddit.subreddit('posts')
        for post in ml_subreddit.hot(limit=100):
            # Used same utc standard for post time, and reference time that's checked when run.

            utcPostTime = submission.created
            submissionDate = datetime.utcfromtimestamp(utcPostTime)
            submissionDateTuple = submissionDate.timetuple()

            currentTime = datetime.utcnow()

        # How long ago it was posted.
        submissionDelta = currentTime - submissionDate
        submissionDelta = str(currentTime - submissionDate)
            
            
		subredditjson = {
            			  '@timestamp' : submissionDelta,
                          'subreddit_id': subreddit.id,
                          'subreddit _url': subreddit.url,
                          'subreddit _ selftext': subreddit.selftext,
                          'subreddit_upvote_ratio': subreddit.upvote_ratio,
                          'subreddit_author': subreddit.author,
                          'subreddit_author_premium': subreddit.author_premium,
                          'subreddit_over_18': subreddit.over_18,
		         'subreddit_treatment_tags': subreddit.treatment_tags
                           }
            print("==================================")
            num_subreddits_collected = num_subreddits_collected + 1
            print(num_subreddits_collected)
            print(subredditjson)
            process_or_store(subredditjson)
    except Exception as e:
        print(e)
else:
    print("please enter subreddit.")
