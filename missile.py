#!/usr/bin/env python

import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--cruise-missile",
        action="store_true", dest="cruise_missile", default=False,
        help="Show Cruise Missile stats")
parser.add_option("-a", "--heavy-assault-missile",
        action="store_true", dest="heavy_assault_missile", default=False,
        help="Show Heavy Assault Missile stats")
parser.add_option("-r", "--rocket",
        action="store_true", dest="rocket", default=False,
        help="Show Rocket stats")

(options, args) = parser.parse_args()

class Missile_bonus(object):
    def __init__(self):
        # Skills
        # Cruise missile damage: 5%
        self.cruise_missile = 4
        # Heavy assault missule damage: 5%
        self.heavy_assault_missile = 4
        # Signature radius factor for missile explosions: -5%
        self.guided_missile_precision = 3
        # Maximum flight time: 10%
        self.missile_bombartment = 2
        # Rate of fire: -2%
        self.missile_launcher_operation = 5
        # Maximum velocity: 10%
        self.missile_projection = 2
        # Rate of fire: -3%
        self.rapid_launch = 4
        # Velocity factor for missiles explosions: 10%
        self.target_navigation_prediction = 4
        # Missile damage: 2%
        self.warhead_upgrades = 3

        # Equipment/Modules
        #
        # Missile damage: I: 7%; II: 10%
        # Rate of fire: I: 7.5%; II: 10.5%
        self.ballistic_control_system_I = 0
        self.ballistic_control_system_II = 3
        #
        #
        # Rigs
        #
        # Rate of fire: I: -10%; II: -15%; Stacking penalty
        self.large_bay_loading_accelerator_I = 0
        self.large_bay_loading_accelerator_II = 0
        # Missile velocity: I: 15%; II: 20%; Stacking penalty
        self.large_hydralic_bay_thrusters_I = 0
        self.large_hydralic_bay_thrusters_II = 0
        # Flight time: I: 15%; II: 20%
        self.large_rocket_fuel_cache_partition_I = 0
        self.large_rocket_fuel_cache_partition_II = 0
        # Missile damage: I: 10%; II: 15%; Stacking penalty
        self.large_warhead_calefaction_catalyst_I = 0
        self.large_warhead_calefaction_catalyst_II = 0
        # Explosion velocity: I: 15%; II: 20%
        self.large_warhead_flare_catalyst_I = 0
        self.large_warhead_flare_catalyst_II = 0
        # Explosion radius: I: -15%; II: -20%
        self.large_warhead_rigor_catalyst_I = 0
        self.large_warhead_rigor_catalyst_II = 0

    def stacking_penalty(self, n):
        # Bonus penalty for stacking equipment that affects the same attribute
        return 0.5 ** (((n - 1) / 2.22292081) ** 2)

    def damage_bonus(self):
        dmg_bonus = 1 + self.cruise_missile * 0.05
        dmg_bonus = dmg_bonus * (1 + self.warhead_upgrades * 0.02)
        dmg_bonus = dmg_bonus * (1.1 ** self.large_warhead_calefaction_catalyst_I)
        for i in range(self.ballistic_control_system_II):
            dmg_bonus = dmg_bonus * (1 + (10 * self.stacking_penalty(i)) / 100)
        return dmg_bonus

    def radius_bonus(self):
        rad_bonus = 1 - self.guided_missile_precision * 0.05
        rad_bonus = rad_bonus * (0.85 ** self.large_warhead_rigor_catalyst_I)
        return rad_bonus

    def velocity_bonus(self):
        vel_bonus = 1 + self.target_navigation_prediction * 0.1
        vel_bonus = vel_bonus * (1.15 ** self.large_warhead_flare_catalyst_I)
        return vel_bonus

class Missile(object):
    def __init__(self, name, damage, radius, velocity, reduction, rate_of_fire):
        self.name = name
        self.damage = damage
        self.radius = radius
        self.velocity = velocity
        self.reduction = reduction
        self.rate_of_fire = rate_of_fire

    def __str__(self):
        base = "{0.name:<30}{0.damage} / {0.radius} / {0.velocity} {0.reduction}"
        return base.format(self)

    def calculate_damage(self, signature, vt, dmg_bonus=1, rad_bonus=1, vel_bonus=1):
        # Signature Damage Factor
        sdf = signature / (self.radius * rad_bonus)
        # Velocity Damage Factor
        vdf = (sdf * ((self.velocity * vel_bonus) / vt)) ** (math.log(self.reduction) / math.log(5.5))
        damage = math.floor(
            self.damage * dmg_bonus * min(
                1,
                (sdf),
                (vdf)
            )
        )
        effect = (damage / math.floor(self.damage * dmg_bonus)) * 100
        dps = (damage / self.rate_of_fire)
        return damage, effect, sdf, vdf, dps

bonus = Missile_bonus()
missiles = []

if parser.values.cruise_missile:
    missiles.append(Missile("Cruise Missile", 375, 330, 69, 4.5, 16.55))
    missiles.append(Missile("Caldari Navy Cruise Missile", 431, 330, 69, 4.5, 16.55))
    missiles.append(Missile("Precision Cruise Missile", 375, 297, 83, 3.5, 16.55))
    missiles.append(Missile("Fury Cruise Missile", 525, 567, 58, 4.7, 16.55))

if parser.values.heavy_assault_missile:
    missiles.append(Missile("Heavy Assault Missile", 100, 125, 101, 4.5, 6.4))
    missiles.append(Missile("Caldari Navy Heavy Assault Missile", 115, 125, 101, 4.5, 6.4))
    missiles.append(Missile("Javelin Heavy Assault Missile", 90, 125, 101, 4.6, 6.4))
    missiles.append(Missile("Rage Heavy Assault Missile", 135, 215, 87, 4.8, 6.4))

if parser.values.rocket:
    missiles.append(Missile("Rocket", 33, 20, 150, 3, 4))
    missiles.append(Missile("Caldari Navy Rocket", 37, 20, 150, 3, 4))
    missiles.append(Missile("Javelin Heavy Assault Missile", 29.7, 20, 150, 3, 4))
    missiles.append(Missile("Rage Heavy Assault Missile", 44.6, 34, 129, 3, 4))


for missile in missiles:
    print(missile)

print()


def damage_matrix(ship, signature, vt):
    print("{0:<30}{1}m, {2}m/s".format(ship, signature, vt))

    for missile in missiles:
        damage, effect, sdf, vdf, dps = missile.calculate_damage(signature, vt)
        print(
                "{0:<30}{1:>3} hp ({2:>6.2f}%) (SigF: {3:.2f}, VelF: {4:.2f}, DPS: {5:>5.2f})".format(
                missile.name, damage, effect, sdf, vdf, dps
            )
        )

        damage, effect, sdf, vdf, dps = missile.calculate_damage(
            signature,
            vt,
            bonus.damage_bonus(),
            bonus.radius_bonus(),
            bonus.velocity_bonus()
        )
        print(
            "{0:<3}{1:<27}{2:>3} hp ({3:>6.2f}%) (SigF: {4:.2f}, VelF: {5:.2f}, DPS: {6:>5.2f})".format(
                "", "with bonus:", damage, effect, sdf, vdf, dps
            )
        )

    print()

damage_matrix("Frigate Atron", 35, 420)
damage_matrix("Destroyer Catalyst", 68, 265)
damage_matrix("Cruiser Thorax", 120, 240)
damage_matrix("Battlecruiser Brutix", 305, 155)
damage_matrix("Battlecruiser Hurricane", 250, 165)
damage_matrix("Battleship Raven", 460, 113)
#damage_matrix("Testship", 320, 113)
damage_matrix("Battleship Typhoon", 320, 130)
