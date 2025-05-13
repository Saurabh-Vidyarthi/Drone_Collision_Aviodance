import numpy as np

class Drone:
    def __init__(self, id, waypoints, velocity):
        self.id = id
        self.waypoints = [np.array(wp, dtype=float) for wp in waypoints]
        self.velocity = float(velocity)
        self.position = self.waypoints[0].copy()
        self.current_wp_idx = 1
        self.reached = False

        if len(self.waypoints) > 1:
            self._update_direction()
        else:
            self.direction = np.zeros(3)

    def _update_direction(self):
        target = self.waypoints[self.current_wp_idx]
        vec = target - self.position
        norm = np.linalg.norm(vec)
        self.direction = vec / norm if norm > 0 else np.zeros(3)

    def step(self, dt):
        if self.reached:
            return
        move_dist = self.velocity * dt
        target = self.waypoints[self.current_wp_idx]
        dist_to_wp = np.linalg.norm(target - self.position)

        if move_dist >= dist_to_wp:
            self.position = target.copy()
            self.current_wp_idx += 1
            if self.current_wp_idx >= len(self.waypoints):
                self.reached = True
                self.direction = np.zeros(3)
            else:
                self._update_direction()
        else:
            self.position += self.direction * move_dist