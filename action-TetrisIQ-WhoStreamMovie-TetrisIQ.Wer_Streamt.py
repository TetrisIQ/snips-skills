#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import json
from datetime import datetime
from datetime import timedelta
import requests
from babel import Locale
import paho.mqtt.client as mqtt

HEADER = {'User-Agent': 'JustWatch Python client (github.com/dawoudt/JustWatchAPI)'}

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class JustWatch:
    def __init__(self, country='AU', use_sessions=True, **kwargs):
        self.kwargs = kwargs
        self.country = country
        self.language = Locale.parse('und_{}'.format(self.country)).language
        self.locale = self.language + '_' + self.country
        self.kwargs_cinema = []
        if use_sessions:
            self.requests = requests.Session()
        else:
            self.requests = requests

    def search_for_item(self, **kwargs):
        if kwargs:
            self.kwargs = kwargs
        null = None
        payload = {
            "age_certifications": null,
            "content_types": null,
            "presentation_types": null,
            "providers": null,
            "genres": null,
            "languages": null,
            "release_year_from": null,
            "release_year_until": null,
            "monetization_types": null,
            "min_price": null,
            "max_price": null,
            "nationwide_cinema_releases_only": null,
            "scoring_filter_types": null,
            "cinema_release": null,
            "query": null,
            "page": null,
            "page_size": null,
            "timeline_type": null
        }
        for key, value in self.kwargs.items():
            if key in payload.keys():
                payload[key] = value
            else:
                print('{} is not a valid keyword'.format(key))
        header = HEADER
        api_url = 'https://api.justwatch.com/titles/{}/popular'.format(self.locale)
        r = self.requests.post(api_url, json=payload, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_providers(self):

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/providers/locale/{}'.format(self.locale)
        r = self.requests.get(api_url, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_genres(self):

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/genres/locale/{}'.format(self.locale)
        r = self.requests.get(api_url, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_title(self, title_id, content_type='movie'):

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/titles/{}/{}/locale/{}'.format(content_type, title_id,
                                                                                     self.locale)
        r = self.requests.get(api_url, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_season(self, season_id):

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/titles/show_season/{}/locale/{}'.format(season_id, self.locale)
        r = self.requests.get(api_url, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_cinema_times(self, title_id, content_type='movie', **kwargs):

        if kwargs:
            self.kwargs_cinema = kwargs

        null = None
        payload = {
            "date": null,
            "latitude": null,
            "longitude": null,
            "radius": 20000
        }
        for key, value in self.kwargs_cinema.items():
            if key in payload.keys():
                payload[key] = value
            else:
                print('{} is not a valid keyword'.format(key))

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/titles/{}/{}/showtimes'.format(content_type, title_id)
        r = self.requests.get(api_url, params=payload, headers=header)

        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_cinema_details(self, **kwargs):

        if kwargs:
            self.kwargs_cinema = kwargs

        null = None
        payload = {
            "latitude": null,
            "longitude": null,
            "radius": 20000
        }
        for key, value in self.kwargs_cinema.items():
            if key in payload.keys():
                payload[key] = value
            elif key == 'date':
                # ignore the date value if passed
                pass
            else:
                print('{} is not a valid keyword'.format(key))

        header = HEADER
        api_url = 'https://apis.justwatch.com/content/cinemas/{}'.format(self.locale)
        r = self.requests.get(api_url, params=payload, headers=header)

        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

        return r.json()

    def get_upcoming_cinema(self, weeks_offset, nationwide_cinema_releases_only=True):

        header = HEADER
        payload = {'nationwide_cinema_releases_only': nationwide_cinema_releases_only,
                   'body': {}}
        now_date = datetime.now()
        td = timedelta(weeks=weeks_offset)
        year_month_day = (now_date + td).isocalendar()
        api_url = 'https://apis.justwatch.com/content/titles/movie/upcoming/{}/{}/locale/{}'
        api_url = api_url.format(year_month_day[0], year_month_day[1], self.locale)

        # this throws an error if you go too many weeks forward, so return a blank payload if we hit an error
        try:
            r = self.requests.get(api_url, params=payload, headers=header)

            # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
            r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200

            return r.json()
        except:
            return {'page': 0, 'page_size': 0, 'total_pages': 1, 'total_results': 0, 'items': []}

    def get_certifications(self, content_type='movie'):

        header = HEADER
        payload = {'country': self.country, 'object_type': content_type}
        api_url = 'https://apis.justwatch.com/content/age_certifications'
        r = self.requests.get(api_url, params=payload, headers=header)

        # Client should deal with rate-limiting. JustWatch may send a 429 Too Many Requests response.
        r.raise_for_status()  # Raises requests.exceptions.HTTPError if r.status_code != 200



        return r.json()


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
        """
        :param hermes:
        :param intentMessage:
        :param conf:
        :return:
        """
        messages = set()
        if len(intentMessage.slots.movie) > 0:
            movie = intentMessage.slots.movie.first().value

            jw = JustWatch(country='DE')
            r = jw.search_for_item(query=movie)
            try:
                for i in range(0, len(r)):
                    for j in range(0, len(r['items'][i]['offers'])):
                        if r['items'][i]['offers'][j]['monetization_type'].__contains__('flatrate'):
                            titel = r['items'][i]['title']
                            provider_id = r['items'][i]['offers'][j]['provider_id']
                            messages.add("{} kann auf {} kostenlos angesehen werden".format(titel, id_to_name(provider_id)))
            except KeyError:
                pass
            print(messages)
            msg = ""
            for s in messages:
                #say(intentMessage.sesession_id, s)
                msg += s + "\n"
            hermes.publish_end_session(intentMessage.session_id, msg)
        else:
            hermes.publish_end_session(intentMessage.session_id, "Error")
    

def id_to_name(id):
    if (id == 8):
        return "Netflix"
    if (id == 9):
        return "Amazon Prime Video"
    return str(id)

def say(session_id, text):
    mqtt.Client().publish('hermes/dialogueManager/endSession', json.dumps({'text': text,'sessionId': session_id}))



if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("TetrisIQ:WhoStreamMovie", subscribe_intent_callback) \
         .start()
