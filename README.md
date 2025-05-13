# Drone Collision Avoidance Simulation

A Python project that simulates multiple drones flying through 3D waypoints with collision‐prediction and avoidance for a primary (user-controlled) drone. The primary drone dynamically adjusts its speed to meet a specified end time and pauses when an imminent collision with any other (fixed-velocity) drone is detected.


## 📂 Repository Structure
.├── README.md

 ├── drones_config.json # JSON file defining primary & other drone waypoints, velocities, schedule
 
 ├── drone.py # Drone class: follows waypoint list at constant velocity
 
 ├── collision_avoidance.py # CollisionAvoidance: predicts and enforces pause on primary
 
 ├── visualization.py # Plotly figure builder: 3D trails, markers, collisions, annotations
 
 └── main.py # loading config, simulation loop, logging & shows UI

## ⚙️ Prerequisites

- Python 3.9+  
- `numpy`  
- `plotly`

Install dependencies in a virtual environment:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
pip install numpy plotly
```


1. Edit drones_config.json

Set the primary drone’s start_time, end_time and its list of 12 waypoints.

Define each other drone’s id, fixed velocity, and its 12 waypoints.

2.Launch: python main.py

🎥 Simulation Demo
<video width="640" controls loop> <source src="demo.mp4" type="video/mp4"> Your browser does not support the video tag. </video>




