import os
# import pygst
import json
import threading
import pprint
from flask import Flask, jsonify, request, redirect, url_for
from flask import render_template, abort
from flask import request
import requests
import time
import threading

DB_JSON_FILE = r'/var/www/spyfall/back/db.json'

class SpyfallApp(Flask):

    def __init__(self, arg):
        super(SpyfallApp, self).__init__(arg)
        self.route("/")(self.index)
        self.route("/debug/<command>")(self.debug)
        self.route("/dump_db/")(self.dump_db)
        self.route("/new_game/<game_name>")(self.new_game)
        self.route("/game_exists/<game_name>")(self.game_exists)
        self.route("/list_games/")(self.list_games)
        self.route("/join_game/<game_name>/<player_name>/")(self.join_game)
        self.route("/list_players_in_game/<game_name>/")(self.list_players_in_game)

    def allow_cross(self, return_value, code=200):
        return return_value, code, {'Access-Control-Allow-Origin': '*'}

    def load_db_file(self):
        with open(DB_JSON_FILE) as fp:
            jsonificated = json.load(fp)
        return jsonificated

    def overwrite_db(self, new_contents):
        with open(DB_JSON_FILE, 'w') as wfp:
            json.dump(new_contents, wfp)
        return "success"

    def index(self):
        return "<h1>Spyfall backend</h1>"

    def debug(self, command):
        return str(eval(command))

    def dump_db(self):
        return jsonify(self.load_db_file())

    def new_game(self, game_name):
        db = self.load_db_file()
        db['games'][game_name] = {}
        db['games'][game_name]['players'] = {}
        self.overwrite_db(db)
        return self.allow_cross(jsonify({"Success: ",game_name}))

    def join_game(self, game_name, player_name):
        db_file = self.load_db_file()
        db_file['games'][game_name]['players'][player_name] = {'role':None}
        self.overwrite_db(db_file)
        return self.allow_cross(jsonify({'success':True}))

    def list_players_in_game(self, game_name):
        db = self.load_db_file()
        return self.allow_cross(jsonify({'players':db['games'][game_name]['players'].keys()}))

    def list_games(self):
        db_file = self.load_db_file()
        return self.allow_cross(jsonify({'games':db_file['games'].keys()}))

    def game_exists(self, game_name):
        db_file = self.load_db_file()
        games_list = db_file['games'].keys()
        if game_name in games_list:
            success = True
        else:
            success = False
        return self.allow_cross(jsonify({'result':success}))

app = SpyfallApp(__name__)

if __name__ == "__main__":
    app.run(debug = "True")
