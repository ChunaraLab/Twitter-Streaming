import tweepy,time,json, csv
import sys
import datetime
import traceback
import os


with open('config.json') as data_file:
    jsondt = json.load(data_file)

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        global con
        global cur
        global s3
        # get current hour
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H")
        old_timestamp = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y_%m_%d_%H")
        
        # write to file
        file_name = timestamp + ".json"
        old_file_name = old_timestamp + ".json"
        old_file_name_gz = old_timestamp + ".tar.gz"
        
        decoded = json.loads(data)
        
        print decoded
        
        with open(file_name,'a') as out_file:
            out_file.write(data)
            
        return True

    def on_error(self, status):
        print status

		
if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.auth.OAuthHandler(jsondt['twitter']['consumer_key'], jsondt['twitter']['consumer_secret'])
    auth.set_access_token(jsondt['twitter']['access_token_key'], jsondt['twitter']['access_token_secret'])

    print "Showing all new tweets:"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    
    
    while True:
        try:
            stream.filter(track=['zika', 'dengue'])
            #stream.filter(locations=[-127,23,-67,50])
            
        except:
            traceback.print_exc()
            print 'bad'
            continue
