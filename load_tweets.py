import twitter
import json
import os.path

def update_tweet_data(config, existing_data):
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    access_token_key = config['access_token_key']
    access_token_secret = config['access_token_secret']
    user_id = config['user_id']
    exclude_replies = config['exclude_replies']
    include_rts = config['include_rts']

    api = twitter.Api(consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret)

    data = existing_data

    if os.path.isfile(out_file):
        with open(out_file, 'r') as f:
            data = json.load(f)
        old_count = len(data)

    current_max_id = 0
    if data:
        current_max_id = data[-1][0] - 1

    done = False
    j = 0
    while not done:
        j+=1
        result = api.GetUserTimeline(user_id=user_id, exclude_replies=exclude_replies, include_rts=include_rts, max_id=current_max_id, count=200)
        if result:
            for i, status in enumerate(result):
                data.append((status.id, status.text))
                current_max_id = status.id - 1
        else:
            done = True
        if j == 170:
            print("Max. requests reached")
            done = True

    current_since_id = 0
    if data:
        current_since_id = data[0][0]

    done = False
    j = 0
    while not done:
        j+=1
        result = api.GetUserTimeline(user_id=user_id, exclude_replies=exclude_replies, include_rts=include_rts, since_id=current_since_id, count=200)
        if result:
            for i, status in enumerate(result):
                data.insert(0, (status.id, status.text))
                current_since_id = status.id + 1
        else:
            done = True
        if j == 10:
            print("Max. requests reached")
            done = True

    return data

if __name__ == '__main__':
    config = {}
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)

    out_file = "tweets_%s.json" % config['user_id']

    print("Loading data for twitter user %d" % config['user_id'])

    data = []
    old_count = 0

    if os.path.isfile(out_file):
        with open(out_file, 'r') as f:
            data = json.load(f)
        old_count = len(data)

    data = update_tweet_data(config, data)

    with open(out_file, 'w') as f:
        json.dump(data, f)

    print("Done!")
    print("%d new tweets have been saved." % (len(data) - old_count))
    print("%d total tweets" % len(data))
