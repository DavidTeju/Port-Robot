# Cargo Offloading Robot

## Overview

This project involves the development of software and hardware integration for a cargo-offloading robot. The robot is designed to autonomously offload cargo based on a prioritization algorithm, with performance optimization through iterative testing and weight adjustments on a cargo-priority function.

## Hardware Requirements

- Raspberry Pi
- Stepper motors for X, Y, and Z axes
- Motor drivers for controlling stepper motors
- Magnetic gripper for cargo handling

## Software Components

### Bot.py

The `Bot` class defines the robot's behavior and movement capabilities. It utilizes the RPi.GPIO library for Raspberry Pi GPIO control and includes methods for moving to specific coordinates, moving by a given vector, and managing the magnet.

### main.py

The `main.py` script orchestrates the cargo offloading process. It loads cargo manifest and coordinates from CSV files, calculates cargo worth based on a prioritization algorithm, and determines an optimal offloading sequence. The script utilizes the `Bot` class to move the robot to designated locations and control the magnetic gripper.

## Project Structure

- **Bot.py**: Contains the `Bot` class responsible for robot movement and control.
- **main.py**: Orchestrates the cargo offloading process using the `Bot` class and implements the cargo prioritization algorithm.
- **manifest.csv**: CSV file containing cargo manifest information (level, row, column, group).
- **coordinates.csv**: CSV file containing spatial coordinates and dimensions for the cargo grid.

## Configuration

Adjustments to the robot's movement parameters, such as speed and stepping time, can be made in the `Bot` class within `Bot.py`. Cargo prioritization weights and other parameters can be fine-tuned in the `calc_worth` function within `main.py`.
