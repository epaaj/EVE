import math

class Skills(object):
    def __init__(self):
        self.cruise_missile = 4
        self.guided_missile_precision = 3
        self.missile_bombartment = 2
        self.missile_launcher_operation = 5
        self.missile_projection = 2
        self.rapid_launch = 4
        self.target_navigation_prediction = 4
        self.warhead_upgrades = 3

    def damage_bonus(self):
        dmg_bonus = self.cruise_missile * 5 + self.warhead_upgrades * 2
        return dmg_bonus / 100 + 1

    def radius_bonus(self):
        rad_bonus = self.guided_missile_precision * 5
        return 1 - (rad_bonus / 100)

    def velocity_bonus(self):
        vel_bonus = self.target_navigation_prediction * 10
        return vel_bonus / 100 + 1

class Missile(object):
    def __init__(self, name, damage, radius, velocity, reduction):
        self.name = name
        self.damage = damage
        self.radius = radius
        self.velocity = velocity
        self.reduction = reduction

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
        return damage, effect, sdf, vdf

skill = Skills()
missiles = []
missiles.append(Missile("Cruise Missile", 300, 300, 69, 4.5))
missiles.append(Missile("Caldari Navy Cruise Missile", 345, 300, 69, 4.5))
missiles.append(Missile("Precision Cruise Missile", 260, 270, 71, 3.5))
missiles.append(Missile("Fury Cruise Missile", 384, 550, 58, 4.7))

for missile in missiles:
    print(missile)

print()


def damage_matrix(ship, signature, vt):
    print("{0:<30}{1}m, {2}m/s".format(ship, signature, vt))

    for missile in missiles:
        damage, effect, sdf, vdf = missile.calculate_damage(signature, vt)
        print(
            "{0:<30}{1:>3} hp ({2:>6.2f}%) (SigF: {3:.2f}, VelF: {4:.2f})".format(
                missile.name, damage, effect, sdf, vdf
            )
        )

        damage, effect, sdf, vdf = missile.calculate_damage(
            signature,
            vt,
            skill.damage_bonus(),
            skill.radius_bonus(),
            skill.velocity_bonus()
        )
        print(
            "{0:<3}{1:<27}{2:>3} hp ({3:>6.2f}%) (SigF: {4:.2f}, VelF: {5:.2f})".format(
                "", "with skills:", damage, effect, sdf, vdf
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
