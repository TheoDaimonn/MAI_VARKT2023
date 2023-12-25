import configparser
import math
import matplotlib.pyplot as plt

#D
class CurrentConditions:
    def __init__(self, mm, r, ts, l, ps, td):
        self.molary_mass = mm
        self.R = r
        self.t_start = ts
        self.l = l
        self.p_start = ps
        self.t_distorsion = td
        self.ttime = 0
        self.g = 9.80665
        self.fuel_getting_out_speed = 4500


class Rocket:
    def __init__(self, name, d, r, smf, smnf, mmnf, fdp, fgos):
        self.name = name
        self.square = math.pi * d * d / 4
        self.resistance = r
        self.starting_mass_fuel = smf
        self.starting_mass_no_fuel = smnf
        self.middle_mass_no_fuel = mmnf
        self.fuel_distorsion_power = fdp
        self.fuel_getting_out_speed = fgos

    def predication(self, t: int, cond: CurrentConditions) -> float:
        if t == 100:
            self.starting_mass_no_fuel = self.middle_mass_no_fuel
        res = - (self.resistance * self.square * self.fuel_getting_out_speed ** 2 / 2) *cond.p_start * (1 + cond.l * self.fuel_getting_out_speed ** 2 * math.cos(
                          math.pi * (t / cond.t_distorsion)) / (2 * cond.t_start * cond.g)) ** (
                                      cond.g * cond.molary_mass / (cond.R * cond.l)) * cond.molary_mass / (
                              cond.R * (cond.t_start + cond.l * self.fuel_getting_out_speed ** 2 * math.cos(
                          math.pi * (t / cond.t_distorsion)) / (2 * cond.g)) * (self.starting_mass_fuel - (
                          self.starting_mass_fuel - self.starting_mass_no_fuel) * (
                                                                                       t / cond.t_distorsion)) * math.cos(
                          (math.pi / 2) * (t / cond.t_distorsion)))
        current_speed = (self.fuel_distorsion_power / (self.starting_mass_fuel - t * (
                self.starting_mass_fuel - self.starting_mass_no_fuel) / cond.t_distorsion) - cond.g / math.cos(
            (math.pi * t) / (2 * cond.t_distorsion)) )
        if t != 97 and t != 98 and t != 99 and t != 96:
            current_speed -= res
        return current_speed


def predicted_graph(rocket: Rocket, conditions: CurrentConditions):
    plt.title('Venera-8 takeoff speed|time plot')
    ys = []
    xs = []
    for t in range(1, 200):
        xs.append(t)
        speed = rocket.predication(t, conditions)
        ys.append(speed)
        try:
            speed = speed.real
        except Exception:
            pass
        print(t, speed)
    plt.xlabel('time')
    plt.ylabel('speed')
    plt.axis([0, 199, 0, 2000])
    plt.plot(xs, ys, linewidth=2.0)
    plt.show()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.sections()
    config.read('vars.ini')
    rocket = Rocket(config['SPACESHIP']['name'], float(config['SPACESHIP']['diameter']),
                    float(config['SPACESHIP']['resistance']),
                    float(config['SPACESHIP']['starting_mass_fuel']),
                    float(config['SPACESHIP']['starting_mass_no_fuel']),
                    float(config['SPACESHIP']['middle_mass_no_fuel']),
                    float(config['SPACESHIP']['fuel_distorsion_power']),
                    float(config['SPACESHIP']['fuel_getting_out_speed']))
    conditions = CurrentConditions(float(config['CONDITIONS']['molary_mass']), float(config['CONDITIONS']['R']),
                                   float(config['CONDITIONS']['t_start']), float(config['CONDITIONS']['l']),
                                   float(config['CONDITIONS']['p_start']), float(config['CONDITIONS']['t_distorsion']))
    print(rocket.predication(97, conditions))

    predicted_graph(rocket, conditions)
