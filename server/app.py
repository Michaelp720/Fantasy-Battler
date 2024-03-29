#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, make_response, jsonify, request, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import Combat, Status, Character, Player, KnownTech, Technique, Enemy
from gameplay_methods import *


# Views go here!


@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Login(Resource):
    def post(self):
        player = Player.query.filter(
            Player.name == request.get_json()['name']
        ).first()
        if player:
            session['player_id'] = player.id
            response = make_response(player.to_dict(), 200)
        else:
            response = make_response({}, 404)
        
        return response

class Logout(Resource):
    def delete(self):
        session['player_id'] = None
        response = make_response({}, 204)
        return response

class CheckSession(Resource):

    def get(self):
        player = Player.query.filter(Player.id == session.get('player_id')).first()
        if player:
            response = make_response(player.to_dict(), 200)
        else:
            response = make_response({}, 401)
        return response

########GET CHARACTER INFO########

class GetCharacter(Resource):
    def get(self, id):
        character = Character.query.filter(Character.id == id).first()
        if character:
            response = make_response(character.to_dict(), 200)
        else:
            response = make_response({}, 404)

        return response

class CharsKnownTechs(Resource):
    def get(self, char_id):
        chars_known_techs = KnownTech.query.filter(KnownTech.character_id == char_id).all()
        known_techs_dict = [known_tech.to_dict() for known_tech in chars_known_techs]
        response = make_response(known_techs_dict, 200)
        return response

class CharsStatuses(Resource):
    def get(self, char_id):
        chars_statuses = Status.query.filter(Status.character_id == char_id).all()
        statuses_dict = [status.to_dict() for status in chars_statuses]
        response = make_response(statuses_dict, 200)
        return response

class GetTech(Resource):
    def get(self, id):
        tech = Technique.query.filter(Technique.id == id).first()
        if tech:
            response = make_response(tech.to_dict(), 200)
        else:
            response = make_response({}, 404)

        return response 

class CurrentCombat(Resource):
    def get(self):
        combat = Combat.query.first()
        response = make_response(combat.to_dict(), 200)
        return response

class StartCombat(Resource):
    def post(self, player_id, enemy_id):
        Combat.query.delete()
        db.session.commit()
        new_combat = Combat(
            player_id = player_id,
            enemy_id = enemy_id,
            rnd = 1,
            turn = 1
        )
        db.session.add(new_combat)
        db.session.commit()
        this_combat = begin_combat()
        response = make_response(this_combat.to_dict(), 201)
        return response

class Monsters(Resource):
    def get(self):
        monsters = Enemy.query.all()
        monsters_dict = [monster.to_dict() for monster in monsters]
        response = make_response(monsters_dict, 200)
        return response


# class GetMonster(Resource):
#     def get(self, id):
#         monster = Enemy.query.filer(Enemy.id == id).first()
#         response = make_response(monster.to_dict, 200)
#         return response

#######GAMEPLAY########
class PlayerAction(Resource):
    def patch(self, tech_id):
        data = request.get_json()
        #tech_id = data['techId']
        combat = get_player_action(tech_id)
        if combat:
            response = make_response(combat.to_dict(), 200)
        else:
            response = make_response({} , 200)
        return response

class EnemyAction(Resource):
    def get(self):
        combat = get_enemy_action()
        if combat:
            response = make_response(combat.to_dict(), 200)
        else:
            response = make_response({} , 200)
        return response

#####ADVANCEMENT#####

class AdvStat(Resource):
    def patch(self, id):
        data = request.get_json()
        stat = data['stat']
        player = Player.query.filter(Player.id == id).first()
        previous_stat_value = getattr(player, stat)
        if stat == 'max_hp':
            increase = 3
            temp_stat = 'crnt_hp'
        elif stat == 'base_pwr':
            increase = 1
            temp_stat = 'temp_pwr'
        elif stat == 'base_def':
            increase = 1
            temp_stat = 'temp_def'
        elif stat == 'spd':
            increase = 2
            temp_stat = None
        setattr(player, stat, previous_stat_value+increase)
        if temp_stat:
            setattr(player, temp_stat, previous_stat_value+increase)
        setattr(player, 'adv_points', player.adv_points - 1)
        db.session.commit()
        updated_player = Player.query.filter(Player.id == id).first()
        response = make_response(updated_player.to_dict(), 200)
        return response
     
class UnlockedTechs(Resource):
    def get(self, char_id):
        unlocked_techs = Technique.query.filter(Technique.unlocked == True).all()
        display_techs = []
        for unlocked_tech in unlocked_techs:
            known = False
            for known_tech in unlocked_tech.known_techs:
                if known_tech.character_id == char_id:
                    known = True
            if not known:
                display_techs.append(unlocked_tech)
        display_techs_dict = [display_tech.to_dict() for display_tech in display_techs]
        response = make_response(display_techs_dict, 200)
        return response

class LearnTech(Resource):
    def post(self):
        data = request.get_json()
        player_id = data['playerId']
        tech_id = data['techId']
        new_known_tech = KnownTech(
            rnk = 1,
            character_id = player_id,
            tech_id = tech_id
        )
        player = Player.query.filter(Player.id == player_id).first()
        new_points = player.adv_points - 2
        setattr(player, 'adv_points', new_points)
        db.session.add(new_known_tech)
        db.session.commit()

        updated_player = Player.query.filter(Player.id == player_id).first()
        response = make_response(updated_player.to_dict(), 200)
        return response


api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

###Character Info###
api.add_resource(GetCharacter, '/character/<int:id>')
api.add_resource(CharsKnownTechs, '/known_techs/<int:char_id>')
api.add_resource(CharsStatuses, '/statuses/<int:char_id>')

###Tech###
api.add_resource(GetTech, '/tech/<int:id>')

###Combat###
api.add_resource(CurrentCombat, '/combat')
api.add_resource(StartCombat, '/combat/<int:player_id>/<int:enemy_id>')

api.add_resource(Monsters, '/monsters')
#api.add_resource(GetMonster, '/monsters/<int:id>')

###Action###
api.add_resource(PlayerAction, '/playeraction/<int:tech_id>')
api.add_resource(EnemyAction, '/enemyaction')

##Advancement###
api.add_resource(AdvStat, '/advstat/<int:id>')
api.add_resource(UnlockedTechs, '/unlockedtechs/<int:char_id>')
api.add_resource(LearnTech, '/learntech')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

