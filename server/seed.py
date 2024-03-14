#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("deleting data")
        Character.query.delete()
        Player.query.delete()
        Enemy.query.delete()

        print("Data deleted. Starting seed...")
        # Seed code goes here!
        new_players = [
            Player(
                id = 1,
                name = "Aragorn",
                max_hp = 18,
                base_pwr = 4,
                base_def = 1,
                spd = 7,
                crnt_hp = 18,
                temp_pwr = 4,
                temp_def = 1,
                order = None
            )
        ]

        db.session.add_all(new_players)
        db.session.commit()

        new_enemies = [
            Enemy(
                id = 2,
                actions = "113",
                name = "Balewolf",
                max_hp = 10,
                base_pwr = 4,
                base_def = 0,
                spd = 15,
                crnt_hp = 10,
                temp_pwr = 4,
                temp_def = 0,
                order = None
            )
        ]

        db.session.add_all(new_enemies)
        db.session.commit()

        new_techs = [
            Technique(
                id = 1,
                name = "Slash",
                target = "enemy",
                duration = 0,
                stat = "hp",
                modifier = 1,
                amnt = 0 #pwr
            ),
            Technique(
                id = 2,
                name = "Snarl",
                target = "enemy",
                duration = 3,
                stat = "def",
                modifier = -1, 
                amnt = 1 #-pwr +1
            ),
            Technique(
                id = 3,
                name = "Parry",
                target = "self",
                duration = 2,
                stat = "def",
                modifier = 0,
                amnt = 2 #0pwr +2
            ),
            Technique(
                id = 4,
                name = "Recover",
                target = "self",
                duration = 0,
                stat = "hp",
                modifier = 0,
                amnt = 3 #0pwr +3
            ),
            Technique(
                id = 5,
                name = "Sprint",
                target = "self",
                duration = 0,
                stat = "order",
                modifier = 0,
                amnt = 1
            )
        ]

        db.session.add_all(new_techs)
        db.session.commit()

        new_known_techs = [
            KnownTech(
                id = 1,
                slot = 1,
                rnk = 0,
                character_id = 1,
                tech_id = 1
            ),
            KnownTech(
                id = 2,
                slot = 2,
                rnk = 0,
                character_id = 1,
                tech_id = 3
            ),
            KnownTech(
                id = 3,
                slot = 3,
                rnk = 0,
                character_id = 1,
                tech_id = 4
            ),
            KnownTech(
                id = 4,
                slot = 1,
                rnk = 0,
                character_id = 2,
                tech_id = 1
            ),
            KnownTech(
                id = 5,
                slot = 2,
                rnk = 0,
                character_id = 2,
                tech_id = 2
            ),
            KnownTech(
                id = 6,
                slot = 4,
                rnk = 0,
                character_id = 1,
                tech_id = 5
            )
        ]

        db.session.add_all(new_known_techs)
        db.session.commit()
        

        print("seeded")