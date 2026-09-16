"""Pong rules shared by the desktop and WebAssembly renderers (no GUI dependencies)."""
import json
import math
import random


class Game:
    width, height = 900, 540
    paddle_height, paddle_width, radius = 96, 14, 9
    target = 7

    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        self.left = self.right = self.height / 2
        self.scores = [0, 0]
        self.rally = self.best_rally = 0
        self.status = 'ready'
        self.serve(1)

    def serve(self, direction):
        self.x, self.y = self.width / 2, self.height / 2
        angle = self.rng.uniform(-0.45, 0.45)
        self.vx = direction * 350 * math.cos(angle)
        self.vy = 350 * math.sin(angle)
        self.countdown = 0.8
        self.rally = 0

    def start(self):
        if self.status == 'over':
            self.reset()
        self.status = 'running'

    def pause(self):
        if self.status == 'running':
            self.status = 'paused'

    def step(self, dt, axis=0, pointer=-1):
        if self.status != 'running':
            return
        dt = max(0, min(float(dt), 0.05))
        # Small substeps prevent tunnelling through a paddle at the fastest speed.
        steps = max(1, math.ceil(dt / (1 / 240)))
        for _ in range(steps):
            self._step(dt / steps, axis, pointer)
            if self.status != 'running':
                break

    def _step(self, dt, axis, pointer):
        half = self.paddle_height / 2
        if pointer >= 0:
            movement = max(-520 * dt, min(520 * dt, pointer - self.left))
        else:
            movement = max(-1, min(1, axis)) * 520 * dt
        self.left = max(half, min(self.height - half, self.left + movement))
        # A bounded opponent follows the ball, but cannot instantly intercept it.
        target = self.y if self.vx > 0 else self.height / 2
        delta = target - self.right
        if abs(delta) > 16:
            self.right += max(-285 * dt, min(285 * dt, delta))
        self.right = max(half, min(self.height - half, self.right))
        if self.countdown > 0:
            self.countdown = max(0, self.countdown - dt)
            return
        old_x = self.x
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.vy = abs(self.vy)
        elif self.y > self.height - self.radius:
            self.y = 2 * (self.height - self.radius) - self.y
            self.vy = -abs(self.vy)
        for plane, paddle, direction in ((50 + self.radius, self.left, 1),
                                           (850 - self.radius, self.right, -1)):
            approaching = self.vx * direction < 0
            crossed = (old_x - plane) * direction >= 0 and (self.x - plane) * direction <= 0
            if approaching and crossed and abs(self.y - paddle) <= half + self.radius:
                self.x = plane
                offset = max(-1, min(1, (self.y - paddle) / half))
                angle = offset * math.pi / 3
                speed = min(760, math.hypot(self.vx, self.vy) * 1.055)
                self.vx = direction * speed * math.cos(angle)
                self.vy = speed * math.sin(angle)
                self.rally += 1
                self.best_rally = max(self.best_rally, self.rally)
        if self.x < -self.radius or self.x > self.width + self.radius:
            scorer = 1 if self.x < 0 else 0
            self.scores[scorer] += 1
            if self.scores[scorer] >= self.target:
                self.status = 'over'
            else:
                self.serve(-1 if scorer == 1 else 1)

    def snapshot(self):
        return json.dumps({key: getattr(self, key) for key in
                           ('x', 'y', 'left', 'right', 'scores', 'rally', 'best_rally', 'status', 'countdown')})
