from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import hashlib
from copy import deepcopy
from client import Client
from character import Character
from enemy import Enemy
from mission import Mission
import random
from array import array
import os
import sys
import jsonpickle

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['characters'] = {}

def init_nl():
    global characters

    data = request.json
    if data == None or "username" not in data or "password" not in data or "profile_id" not in data:
        return jsonify(
            success = False,
            message = "username, password, and profile_id required"
        )
    if data["username"] == "" or data["password"] == "" or data["profile_id"] == "":
        return jsonify(
            success = False,
            message = "username, password, and profile_id must not empty"
        )

    client = Client()
    if data['username'] in app.config['characters']:
        character = app.config['characters'][data['username']]
        character.set_client(client)
    else:
        character = Character()
        character.set_client(client)
        character.login(data["profile_id"], data["username"], data["password"])
        app.config['characters'][data['username']] = character

    enemy = Enemy(character)
    mission = Mission(enemy, client, character)

    return {
        client: client,
        character: character,
        enemy: enemy,
        mission: mission
    }


@app.route('/mission', methods=['POST'])
@cross_origin()
def instant_mission():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "mission_id" not in data:
        return jsonify(
            success = False,
            message = "mission_id required"
        )
    if data["mission_id"] == "":
        return jsonify(
            success = False,
            message = "mission_id must not empty"
        )

    uid = data['profile_id']
    mission_id = int(data['mission_id'])

    return mission.instant_mission(uid, mission_id)



@app.route('/hunting_house', methods=['POST'])
@cross_origin()
def hunting_house():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "boss_num" not in data:
        return jsonify(
            success = False,
            message = "boss_num required"
        )
    if data["boss_num"] == "":
        return jsonify(
            success = False,
            message = "boss_num must not empty"
        )

    uid = data['profile_id']
    boss_num = int(data['boss_num'])

    # start hunting house
    r_msg = client.send_remoting_amf(
        target="HuntingHouse.startHunting", 
        body=[[f"{uid}", f"{boss_num}", character.session_key]]
    )

    battle_code = r_msg.bodies[0][1].body

    # finish mission
    h = hashlib.sha256(f"{boss_num}{uid}{battle_code}".encode())
    r_msg = client.send_remoting_amf(
        target="HuntingHouse.finishHunting", 
        body=[[f"{uid}", f"{boss_num}", battle_code, h.hexdigest(), character.session_key]]
    )

    results = r_msg.bodies[0][1].body
    return results

@app.route('/hallowen', methods=['POST'])
@cross_origin()
def hallowen():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    agi = "10"
    data = request.json
    ene = "ene572"
    eneid = "1"
    uid = data['profile_id']
    boss_num = int(data['boss_num'])
    _loc6_ = "id:ene572|hp:6660|agility:30";
    h2 = hashlib.sha256(f"'ene_572'{_loc6_}{10}".encode())
    # start hunting house
    r_msg = client.send_remoting_amf(
        target="HalloweenEvent2023.startEvent", 
        body=[[f"{uid}", f"{eneid}", f"{ene}", _loc6_, f"{agi}", h2.hexdigest(), character.session_key]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return jsonpickle.encode(battle_code)
    h3 = hashlib.sha256(f"'ene_572'{uid}{battle_code}'6660'".encode())
    r_msg = client.send_remoting_amf(
        target="HalloweenEvent2023.finishEvent", 
        #body=[[Character.char_id,Character.christmas_boss_num,Character.battle_code,_loc2_,this.getTotalDamageDoneToEnemies(),Character.sessionkey]]
        body=[[f"{uid}", "ene_572", battle_code, h3.hexdigest(),"6660", character.session_key]]
    )
    results = r_msg.bodies[0][1].body
    #print(r_msg)
    return jsonpickle.encode(results)
    #return jsonpickle.encode(r_msg.bodies[0][1].body)
    #print(h2.hexdigest())
    
@app.route('/eudemon', methods=['POST'])
@cross_origin()
def eudemon():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "boss_num" not in data:
        return jsonify(
            success = False,
            message = "boss_num required"
        )
    if data["boss_num"] == "":
        return jsonify(
            success = False,
            message = "boss_num must not empty"
        )

    uid = data['profile_id']
    boss_num = int(data['boss_num'])

    # start hunting house
    r_msg = client.send_remoting_amf(
        target="EudemonGarden.startHunting", 
        body=[[f"{uid}", f"{boss_num}", character.session_key]]
    )

    battle_code = r_msg.bodies[0][1].body

    # finish mission
    h = hashlib.sha256(f"{boss_num}{uid}{battle_code}".encode())
    r_msg = client.send_remoting_amf(
        target="EudemonGarden.finishHunting", 
        body=[[f"{uid}", f"{boss_num}", battle_code, h.hexdigest(), character.session_key]]
    )

    results = r_msg.bodies[0][1].body
    return results
    
@app.route('/clanwar', methods=['POST'])
@cross_origin()
def clanwar():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "clanid" not in data:
        return jsonify(
            success = False,
            message = "clanid"
        )
    if data["clanid"] == "":
        return jsonify(
            success = False,
            message = "clanid"
        )

    uid = data['profile_id']
    clanid = data['clanid']
    clanidd = data['clanidd']
    quickAttack = "quickAttack"
    def generate_random_string(length):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(characters) for _ in range(length))
    _loc2_ = generate_random_string(20)
    _loc4_ = [uid, character.session_key, clanid, _loc2_]
        
    r_msg = client.send_remoting_amf(
        target="ClanService.executeService", 
        body=[[f"{quickAttack}", _loc4_, character.session_key]]
    )

    results = r_msg.bodies[0][1].body
    return results

@app.route('/stam', methods=['POST'])
@cross_origin()
def stam():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    restoreStamina = "restoreStamina"
    def generate_random_string(length):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(characters) for _ in range(length))
    _loc2_ = generate_random_string(25)
    _loc4_ = [uid, character.session_key, _loc2_]
        
    r_msg = client.send_remoting_amf(
        target="ClanService.executeService", 
        body=[[f"{restoreStamina}", _loc4_]]
    )

    results = r_msg.bodies[0][1].body
    return results



@app.route('/debug', methods=['GET'])
@cross_origin()
def debug():
    return 'debug'
    
@app.route('/logout', methods=['GET'])
@cross_origin()
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
