""" Zever solar integration """

VERSION = '0.1.0'

from datetime import date, datetime, timedelta
import logging
import requests

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

#DEFAULT_NAME = ''
#DOMAIN = ''
ICON = 'mdi:wb_sunny'
#SENSOR_PREFIX = ''

CONST_USERNAME = 'username'
CONST_PASSWORD = 'password'

SCAN_INTERVAL = timedelta(seconds=30)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3600)
PARALLEL_UPDATES = 1

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONST_USERNAME): cv.string,
    vol.Required(CONST_PASSWORD): cv.string,
})

import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    username = config.get(CONST_USERNAME)
    password = config.get(CONST_PASSWORD)

    #_LOGGER.debug("Username = %s", username)

    # Setup sensors
    sensors = []
    for name in trashTypesDefault:
        sensors.append(TrashSensor(hass, name, fetch_trash_data, afvaldienst, config))
    async_add_entities(sensors)

    #_LOGGER.debug("Sensors = %s", sensors)

class ZeversolarSensor(Entity):
    def __init__(self, text_state):
        self._state = None
        self._description = None
        self._text_state = text_state
        self.update()

    def update(self):
        
        cookie = 'stationId=; acw_tc=; user=; JSESSIONID='

        now = datetime.datetime.now()
        month = now.month - 1

        data = fetchForYear(cookie, now.year)

        if data == False:
          print('unknown')
        else:
          productionInMonth = float(data[month]['value'][0])
          print(productionInMonth)

        if False:
            self._description = 'There is a problem with your power supply or system.'
            if self._text_state:
                self._state = self._description
                self._attribute = {'value': _throttled}
            else:
                self._state = _throttled
                self._attribute = {'description': self._description}
            
    def fetchForYear(cookie, year):
      headers = {'cookie': cookie}
      r = requests.get('https://www.zevercloud.com/data/energy/amounty/' + str(year) + '?sid=' + sid + '&isno=' + isno, headers=headers)
      body = r.content.decode("utf-8")
      if 'forbidden' in body:
        return False
      elif r.status_code == requests.codes.ok:
        return r.json()[0]['dataset']

    @property
    def name(self):
        return 'ZeverSolar'

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._attribute
