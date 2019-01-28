#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from JustWatchAPI.justwatch import JustWatch

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name: option for option_name, option in self.items(section)} for section in
                self.sections()}

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
    if len(intentMessage.slots.movie) > 0:
        messages = set()
        jw = JustWatch(country='DE')
        movie = intentMessage.slots.movie.first().value
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
        msg = ""
        for s in messages:
            # say(intentMessage.sesession_id, s)
            msg += s + "\n"
        hermes.publish_end_session(intentMessage.session_id, msg)
    else:
        hermes.publish_end_session(intentMessage.session_id, "Error")


    hermes.publish_end_session(intentMessage.session_id, "nächster track")


def id_to_name(id):
    if (id == 8):
        return "Netflix"
    if (id == 9):
        return "Amazon Prime Video"
    return str(id)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("TetrisIQ:WhoStreamMovie", subscribe_intent_callback) \
         .start()
