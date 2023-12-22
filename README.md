# KickScraper

This program requests data from the unpublished kick.com API.
The input of the program is the user's slug name on kick.com, which is an indentifier used to create URLs within kick's API.
Additionally, APIs are called to retrieve a list of clips and return live statistics for viewer and follower counts.
Example output json from this program has been included for reference.

The output of the program is JSON data representing the current state of the user including:
- Username
- User profile pic
- User profile bio
- User profile banner
- User socials
- User videos
- User’s streaming status (offline vs. live)
- User followers
- User clips


The API is protected by cloudflare.
To get around cloudflare's protection of the API endpoints, I used the `cloudscraper` library.

The `cloudscraper` library is intended for bypassing cloudflare challenges, but updates to cloudflare could mean that it starts failing.
Since it may not remain a stable and permanent solution for bypassing cloudflare, it might be worth looking into other options for scraping.
Here is a cloudflare web scraper utility service that could be a more permanent solution: https://www.scraperapi.com/blog/scrape-cloudflare-protected-websites-with-python/

In order to maximize the compatibility of the distribution and ensure all library dependencies install correctly, this script should be run from within a docker environment.
I have created a dockerfile to build and install the dependencies.

## Building the Docker
It is important to build it with `no-cache` enabled to make sure that the latest cutting-edge versions of all libraries are installed.
```bash
docker build --no-cache . -t kickscraper
```

## Running the Docker
- example of running to request data for the streamer nickmercs
```bash
docker run --rm kickscraper nickmercs
```

# Scraping Subscriptions
In addition to scraping the user APIs, it would be nice to scrape the following:
- User subscribers
- User gifted subscriptions

This information is retrieved dynamically by the client and displayed in the chat windows.
The client subscribes to a pusher channel, called `channel.1234`, where 1234 is the user ID number returned from the API calls.
- pusher pubsub event service: https://pusher.com/
- pusher CLI installation <https://pusher.com/docs/channels/pusher_cli/installation/>

The way to retrieve subscriptions for users and channels would be to subscribe to the pusher channels of relevant streamers with the same app ID used by the client.
Then, this data can be followed in real-time by a service which can record subscription events.

```javascript
// connect to pusher with same API key, app key, and cluster settings as browser client
var channel = pusher.subscribe("channel.1249505"); // example: process subscriptions to j9streams
channel.bind('App\\Events\\ChannelSubscriptionEvent', function(data){
  console.log(data); // process subscription and send to database
});
```
