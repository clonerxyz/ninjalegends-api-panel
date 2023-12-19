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
import json

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

@app.route('/xdata', methods=['POST'])
@cross_origin()
def xdata():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    eneid = "1"
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="Xmas2023.executeService", 
        body=[["getData",[f"{uid}",character.session_key]]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code



@app.route('/xmas', methods=['POST'])
@cross_origin()
def xmas():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    agi = "89"
    data = request.json
    ene = "ene_564"
    eneid = "0"
    hp = "26640"
    hp2 = "9999999"
    uid = data['profile_id']
    boss_num = int(data['boss_num'])
    _loc6_ = "id:ene_564|hp:26640|agility:114";
    #h2 = hashlib.sha256(f"{ene}{_loc6_}{89}".encode())
    h2 = hashlib.sha256(f"{ene}{_loc6_}{agi}".encode())
    r_msg = client.send_remoting_amf(
        target="Xmas2023.executeService", 
        body=[["startFight",[f"{uid}",character.session_key, f"{eneid}", f"{ene}", _loc6_, f"{agi}", h2.hexdigest()]]]
    )
    
    battle_code = r_msg.bodies[0][1].body

    h3 = hashlib.sha256(f"{eneid}{uid}{battle_code}{hp}".encode())
    r_msg2 = client.send_remoting_amf(
        target="Xmas2023.finishEvent", 
        #body=[[Character.char_id,Character.christmas_boss_num,Character.battle_code,_loc2_,this.getTotalDamageDoneToEnemies(),Character.sessionkey]]
        body=[[f"{uid}", f"{eneid}", battle_code, h3.hexdigest(),f"{hp}", character.session_key]]
    )
    results = r_msg2.bodies[0][1].body

    return results

@app.route('/xmas2', methods=['POST'])
@cross_origin()
def xmas2():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    agi = "89"
    data = request.json
    ene = "ene_565"
    eneid = "1"
    hp = "26640"
    hp2 = "9999999"
    uid = data['profile_id']
    boss_num = int(data['boss_num'])
    _loc6_ = "id:ene_565|hp:26640|agility:114";
    #h2 = hashlib.sha256(f"{ene}{_loc6_}{89}".encode())
    h2 = hashlib.sha256(f"{ene}{_loc6_}{agi}".encode())
    r_msg = client.send_remoting_amf(
        target="Xmas2023.executeService", 
        body=[["startFight",[f"{uid}",character.session_key, f"{eneid}", f"{ene}", _loc6_, f"{agi}", h2.hexdigest()]]]
    )
    
    battle_code = r_msg.bodies[0][1].body

    h3 = hashlib.sha256(f"{eneid}{uid}{battle_code}{hp}".encode())
    r_msg2 = client.send_remoting_amf(
        target="Xmas2023.finishEvent", 
        #body=[[Character.char_id,Character.christmas_boss_num,Character.battle_code,_loc2_,this.getTotalDamageDoneToEnemies(),Character.sessionkey]]
        body=[[f"{uid}", f"{eneid}", battle_code, h3.hexdigest(),f"{hp}", character.session_key]]
    )
    results = r_msg2.bodies[0][1].body

    return results

@app.route('/xmas3', methods=['POST'])
@cross_origin()
def xmas3():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    agi = "89"
    data = request.json
    ene = "ene_566"
    eneid = "2"
    hp = "26640"
    hp2 = "9999999"
    uid = data['profile_id']
    boss_num = int(data['boss_num'])
    _loc6_ = "id:ene_566|hp:26640|agility:114";
    #h2 = hashlib.sha256(f"{ene}{_loc6_}{89}".encode())
    h2 = hashlib.sha256(f"{ene}{_loc6_}{agi}".encode())
    r_msg = client.send_remoting_amf(
        target="Xmas2023.executeService", 
        body=[["startFight",[f"{uid}",character.session_key, f"{eneid}", f"{ene}", _loc6_, f"{agi}", h2.hexdigest()]]]
    )
    
    battle_code = r_msg.bodies[0][1].body

    h3 = hashlib.sha256(f"{eneid}{uid}{battle_code}{hp}".encode())
    r_msg2 = client.send_remoting_amf(
        target="Xmas2023.finishEvent", 
        #body=[[Character.char_id,Character.christmas_boss_num,Character.battle_code,_loc2_,this.getTotalDamageDoneToEnemies(),Character.sessionkey]]
        body=[[f"{uid}", f"{eneid}", battle_code, h3.hexdigest(),f"{hp}", character.session_key]]
    )
    results = r_msg2.bodies[0][1].body

    return results
    
@app.route('/xmas4', methods=['POST'])
@cross_origin()
def xmas4():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    agi = "89"
    data = request.json
    ene = "ene_268"
    eneid = "3"
    hp = "26640"
    hp2 = "9999999"
    uid = data['profile_id']
    boss_num = int(data['boss_num'])
    _loc6_ = "id:ene_566|hp:26640|agility:114";
    #h2 = hashlib.sha256(f"{ene}{_loc6_}{89}".encode())
    h2 = hashlib.sha256(f"{ene}{_loc6_}{agi}".encode())
    r_msg = client.send_remoting_amf(
        target="Xmas2023.executeService", 
        body=[["startFight",[f"{uid}",character.session_key, f"{eneid}", f"{ene}", _loc6_, f"{agi}", h2.hexdigest()]]]
    )
    
    battle_code = r_msg.bodies[0][1].body

    h3 = hashlib.sha256(f"{eneid}{uid}{battle_code}{hp}".encode())
    r_msg2 = client.send_remoting_amf(
        target="Xmas2023.finishEvent", 
        #body=[[Character.char_id,Character.christmas_boss_num,Character.battle_code,_loc2_,this.getTotalDamageDoneToEnemies(),Character.sessionkey]]
        body=[[f"{uid}", f"{eneid}", battle_code, h3.hexdigest(),f"{hp}", character.session_key]]
    )
    results = r_msg2.bodies[0][1].body

    return results
    
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

@app.route('/chudata', methods=['POST'])
@cross_origin()
def chudata():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="ChuninExam.getData", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
    
@app.route('/chunin', methods=['POST'])
@cross_origin()
def chunin():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="ChuninExam.promoteToChunin", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
   
@app.route('/chuninexam', methods=['POST'])
@cross_origin()
def chuninexam():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    stg = data['stg']
    total_ene_hp = "100"
    r_msg = client.send_remoting_amf(
        target="ChuninExam.startStage", 
        body=[[character.session_key,f"{uid}",f"{stg}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    #return battle_code
    r_msg = client.send_remoting_amf(
        target="ChuninExam.finishStage", 
        body=[[character.session_key,f"{uid}",f"{stg}","2","9","2"]]
    )

    results = r_msg.bodies[0][1].body
    #ress = jsonpickle.encode(results)
    return results

@app.route('/jodata', methods=['POST'])
@cross_origin()
def jodata():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="JouninExam.getData", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
    
@app.route('/jounin', methods=['POST'])
@cross_origin()
def jounin():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="JouninExam.promoteToJounin", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
   
@app.route('/jouninexam', methods=['POST'])
@cross_origin()
def jouninexam():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    stg = data['stg']
    total_ene_hp = "100"
    r_msg = client.send_remoting_amf(
        target="JouninExam.startStage", 
        body=[[character.session_key,f"{uid}",f"{stg}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    #return battle_code
    r_msg = client.send_remoting_amf(
        target="JouninExam.finishStage", 
        body=[[character.session_key,f"{uid}",f"{stg}","2","9","2"]]
    )

    results = r_msg.bodies[0][1].body
    #ress = jsonpickle.encode(results)
    return results
    
@app.route('/ssjodata', methods=['POST'])
@cross_origin()
def ssjodata():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="SpecialJouninExam.getData", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
    
@app.route('/ssjounin', methods=['POST'])
@cross_origin()
def ssjounin():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="SpecialJouninExam.promoteToSpecialJounin", 
        body=[[character.session_key,f"{uid}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    return battle_code
   
@app.route('/ssjoexam', methods=['POST'])
@cross_origin()
def SpecialJouninExam():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    uid = data['profile_id']
    stg = data['stg']
    #stg2 = data['stg2']
    total_ene_hp = "100"
    r_msg = client.send_remoting_amf(
        target="SpecialJouninExam.startStage", 
        body=[[character.session_key,f"{uid}",f"{stg}"]]
    )
    
    battle_code = r_msg.bodies[0][1].body
    #return battle_code
    r_msg = client.send_remoting_amf(
        target="SpecialJouninExam.finishStage", 
        body=[[character.session_key,f"{uid}",f"{stg}","2","9","2"]]
    )

    results = r_msg.bodies[0][1].body
    #ress = jsonpickle.encode(results)
    return results

@app.route('/pvp', methods=['POST'])
@cross_origin()
def pvp():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()
    data = request.json
    hp = int('4000')
    uid = data['profile_id']
    r_msg = client.send_remoting_amf(
        target="ArenaService.executeService", 
        body=[["startBattle",[f"{uid}",character.session_key]]]
    )
    
    battle_code = r_msg.bodies[0][1].body['battle_code']
    #h3 = hashlib.sha256(f"{battle_code},{hp}".encode()).hexdigest()
    h3 = hashlib.sha256(f"{battle_code},{hp}".encode())
    r_msg2 = client.send_remoting_amf(
        target="ArenaService.executeService", 
        
        body=[["endBattle",[f"{uid}", character.session_key , battle_code , hp, h3.hexdigest()]]]
    )
    results = r_msg2.bodies[0][1].body

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
