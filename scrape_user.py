#!/usr/bin/env python3

import requests
import json
import cloudscraper # need to use cloudscraper because the APIs are protected by cloudflare
import sys

def get_data(username):
    output = {"username": username, "error": 0, "errormsg": ""}

    # get the main data blob
    url = "https://kick.com/api/v1/channels/" + username
    scraper = cloudscraper.create_scraper()
    html = scraper.get(url)
    if html.status_code != 200:
        output['error'] = html.status_code
        output["errormsg"] = "unable to retrieve user data"
        return output
    data = json.loads(html.text)
    userid = data['id'] # get the numeric userid from kick that we need to build other URLs
    slug = data['slug']

    # get live count of followers of stream live_followers
    url = f"https://api.kick.com/channels/{userid}/followers-count"
    html = scraper.get(url)
    if html.status_code != 200:
        # if the request failed, use the followers count in the main data blob
        live_followers = data['followersCount']
    else:
        # parse live statistics from API
        temp = json.loads(html.text)
        live_followers = temp['data']['count']
    output["followers"] = live_followers

    # get live viewers count live_viewers
    url = f"https://api.kick.com/private/v0/channels/{userid}/viewer-count"
    html = scraper.get(url)
    if html.status_code != 200:
        # this endpoints returns 400 if they are not streaming
        live_viewers = 0
    else:
        temp = json.loads(html.text)
        live_viewers = temp['data']['viewer_count']

    output['username'] = data['user']['username']
    output['streaming'] = (data['livestream'] != None) # streaming status, true or false
    output['profile_bio'] = data['user']['bio']
    output['profile_banner'] = data['banner_image']['url']
    output['profile_pic'] = data['user']['profile_pic']
    # socials
    output['socials'] = {
            "twitter" : data['user']['twitter'],
            "discord" : data['user']['discord'],
            "tiktok" : data['user']['tiktok'],
            "youtube" : data['user']['youtube'],
            "instagram" : data['user']['instagram'],
            "facebook" : data['user']['facebook']
    }

    # user recent videos
    # TODO: should get all videos from video page?
    vods = []
    for s in data['previous_livestreams']:
        vod = {"slug": s['slug'], "title": s['session_title'], "thumbnail": s['thumbnail']['src'], "viewer_count": s['viewer_count']}
        vods.append(vod)
    output['recent_videos'] = vods

    # get clips
    clips = []
    # if there are too many to return, can this cursor value be used to retrieve more?
    url = f"https://kick.com/api/v2/channels/{slug}/clips?cursor=0"
    html = scraper.get(url)
    if (html.status_code == 200):
        clipdata = json.loads(html.text)
        for c in clipdata['clips']:
            clip = { 'title': c['title'], 'url': c['clip_url'], 'thumbnail_url': c['thumbnail_url'] }
            clips.append(clip)
    output['clips'] = clips

    return output

if __name__ == '__main__':
    input_username = sys.argv[1]
    # if the script fails then it should return a json object with a descriptive error
    print(json.dumps(get_data(input_username)))
