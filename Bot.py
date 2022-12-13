from time import sleep

import RPi.GPIO as GPIO


class Bot:
    # Config bot
    configs = (
        # X-axis
        {"STEP": 23,
         "DIR": 24,
         "SPEED": 0.002,
         "STEPPING_TIME": 0.001,
         "RATIO": 67.75  # Steps to inch ratio
         },

        # Y-axis
        {"STEP": 10,
         "DIR": 12,
         "SPEED": 0.001,
         "STEPPING_TIME": 0.0001,
         "RATIO": 275
         },

        # Z-axis
        {"STEP": 11,
         "DIR": 13,
         "SPEED": 0.0005,
         "STEPPING_TIME": 0.001,
         "RATIO": 160
         })

    CLOCK_WISE = 1
    COUNTER_CLOCK_WISE = 0
    curr = [0, 0, 0]

    GPIO.setmode(GPIO.BOARD)

    for config in configs:
        GPIO.setup(config["DIR"], GPIO.OUT)
        GPIO.setup(config["STEP"], GPIO.OUT)
        GPIO.output(config["DIR"], COUNTER_CLOCK_WISE)
        GPIO.output(config["DIR"], CLOCK_WISE)

    @staticmethod
    def origin():
        Bot.move_to(0, 0, 0)

    @staticmethod
    def move_to(x, y, z):
        """
        Move bot hand to a given coordinate

        :param x: number of inches from origin in the x-axis
        :param y: number of inches from origin in the y-axis
        :param z: number of inches from origin in the z-axis
        """

        Bot.move_by((0, 0, -Bot.curr[2]))  # Go up to avoid knocking over
        Bot.move_by((x - Bot.curr[0], y - Bot.curr[1], z))

    @staticmethod
    def move_by(vector_tup: tuple[int, int, int]):
        """
        Move bot hand by a given number of inches in different directions

        :param vector_tup: a 3D-space distance vector (x, y, z) to travel in
        """
        for i, coord in enumerate(vector_tup):
            direction = Bot.CLOCK_WISE if coord < 0 else Bot.COUNTER_CLOCK_WISE
            sleep(1)
            config = Bot.configs[i]
            GPIO.output(config["DIR"], direction)

            for _ in range(int(abs(coord) * config["RATIO"])):
                GPIO.output(config["STEP"], GPIO.HIGH)
                sleep(config["STEPPING_TIME"])
                GPIO.output(config["STEP"], GPIO.LOW)
                sleep(config["SPEED"])
            Bot.curr[i] += coord

    @staticmethod
    def magnet_off(time_seconds):
        """
        Omar. This is where you do your thing!
        """
        pass
