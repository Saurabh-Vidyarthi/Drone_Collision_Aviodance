import json, math
import numpy as np
from drone import Drone
from collision_avoidance import CollisionAvoidance
from visualization import create_interactive_figure

def load_config(path="drone_config.json"):
    with open(path) as f:
        return json.load(f)

def remaining_distance(drone):
    """Euclidean distance from current pos through all remaining waypoints."""
    if drone.reached:
        return 0.0
    pts = [drone.position] + drone.waypoints[drone.current_wp_idx:]
    return sum(np.linalg.norm(pts[i+1]-pts[i]) for i in range(len(pts)-1))

def main():
    cfg = load_config()
    dt = 0.1

    # build primary drone (I am only controlling primary drone velocity)
    p = cfg["primary"]
    primary = Drone(p["id"], p["waypoints"], velocity=1.0)
    t_end = p["end_time"]

    # build others
    others = [
        Drone(o["id"], o["waypoints"], o["velocity"])
        for o in cfg["others"]
    ]

    # prep simulate
    drones = [primary] + others
    avoid = CollisionAvoidance(threshold=1.5, buffer_steps=5, pause_time=2.0)

    positions = {d.id: [] for d in drones}
    velocities = {d.id: [] for d in drones}
    collisions = {}   # frame_idx -> list of (x,y,z)
    pause_log = []    # tuples of (sim_t, other_id, frame_idx)

    sim_t, frame = 0.0, 0
    print("Starting simulation: --> ")

    while not all(d.reached for d in drones):
        # dynamic primary speed control
        time_left = t_end - sim_t
        dist_left = remaining_distance(primary)
        if time_left > 0:
            primary.velocity = dist_left / time_left

        # collision check for primary
        pause, info = avoid.should_pause(primary, others, dt)
        if pause and info:
            other_id, pos = info
            pause_log.append((sim_t, other_id, frame))
            collisions.setdefault(frame, []).append(tuple(pos))
            print(f"[t={sim_t:.2f}s] PAUSE primary Drone due to Drone {other_id}")

        # step everyone
        for d in drones:
            if d.id == primary.id and pause:
                v = 0.0
            else:
                d.step(dt)
                v = d.velocity
            positions[d.id].append(d.position.copy())
            velocities[d.id].append(v)

        sim_t += dt
        frame += 1

    # print full pause log
    print("\nPause events (time, other drone):")
    for t, oid, fr in pause_log:
        print(f"  • t={t:.2f}s  paused by colliding with Drone {oid}")

    
    fig = create_interactive_figure(positions, velocities, collisions, pause_log, dt)
    fig.show()

if __name__=="__main__":
    main()