#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from JustWatchAPI.justwatch import JustWatch

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

my_conf = ['Netflix', 'Amazon Prime Video']


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


def new_on_netflix(hermes, intentMessage, conf):
    hermes.publish_end_session(intentMessage.session_id, "Zurzeit ist nichts neu bei netflix")


def action_wrapper(hermes, intentMessage, conf):
    """
    :param hermes:
    :param intentMessage:
    :param conf:
    :return:
    """
    if len(intentMessage.slots.movie) > 0:
        movie = intentMessage.slots.movie.first().value
        msg = ""
        for s in trigger_api(movie):
            for k in my_conf:
                if s.__contains__(k):
                    msg += s + "\n"
        hermes.publish_end_session(intentMessage.session_id, msg)
    else:
        hermes.publish_end_session(intentMessage.session_id, "Error")


def trigger_api(movie):
    jw = JustWatch(country='DE')
    r = jw.search_for_item(query=movie)
    message = set()
    try:
        for i in range(0, len(r)):
            for j in range(0, len(r['items'][i]['offers'])):
                if r['items'][i]['offers'][j]['monetization_type'].__contains__('flatrate'):
                    titel = r['items'][i]['title']
                    provider_id = r['items'][i]['offers'][j]['provider_id']
                    message.add("{} kann auf {} kostenlos angesehen werden\n".format(titel, id_to_name(provider_id)))
    except KeyError:
        pass
    return message


def id_to_name(id):
    if (id == 8):
        return "Netflix"
    if (id == 9):
        return "Amazon Prime Video"
    return str(id)


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
