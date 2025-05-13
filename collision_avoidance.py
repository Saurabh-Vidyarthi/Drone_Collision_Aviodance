
import numpy as np

class CollisionAvoidance:
    def __init__(self, threshold=1.5, buffer_steps=5, pause_time=2.0):
        self.threshold = threshold
        self.buffer_steps = buffer_steps
        self.pause_time = pause_time
        self.pause_remaining = 0.0

    def should_pause(self, primary, others, dt):
        # continue an existing pause
        if self.pause_remaining > 0:
            self.pause_remaining -= dt
            return True, None

        # look ahead
        for o in others:
            for step in range(1, self.buffer_steps + 1):
                t = dt * step
                p_fut = primary.position + primary.direction * primary.velocity * t
                o_fut = o.position + o.direction * o.velocity * t
                if np.linalg.norm(p_fut - o_fut) < self.threshold:
                    self.pause_remaining = self.pause_time
                    return True, (o.id, p_fut)
        return False, None