import unittest
from engine import Game


class Rules(unittest.TestCase):
    def running(self):
        g = Game(seed=3)
        g.start()
        g.countdown = 0
        return g

    def test_ready_and_paused_do_not_move(self):
        g = Game()
        before = g.snapshot()
        g.step(.03, 1)
        self.assertEqual(before, g.snapshot())
        g.start(); g.pause()
        before = g.snapshot(); g.step(.03, 1)
        self.assertEqual(before, g.snapshot())

    def test_paddle_bounds(self):
        g = self.running()
        for _ in range(100): g.step(.05, -1)
        self.assertEqual(g.left, 48)
        for _ in range(100): g.step(.05, 1)
        self.assertEqual(g.left, 492)

    def test_player_scores_on_right(self):
        g = self.running(); g.x = 911; g.vx = 350
        g.step(.01)
        self.assertEqual(g.scores, [1, 0])
        self.assertEqual(g.x, 450)
        self.assertGreater(g.countdown, 0)

    def test_computer_scores_on_left(self):
        g = self.running(); g.x = -10; g.vx = -350
        g.step(.01)
        self.assertEqual(g.scores, [0, 1])

    def test_win_and_restart(self):
        g = self.running(); g.scores[0] = 6; g.x = 911
        g.step(.01)
        self.assertEqual(g.status, 'over')
        g.start()
        self.assertEqual(g.scores, [0, 0])
        self.assertEqual(g.status, 'running')

    def test_fast_ball_hits_paddle_once(self):
        g = self.running(); g.x = 70; g.y = g.left; g.vx = -760; g.vy = 0
        g.step(.05)
        self.assertGreater(g.vx, 0)
        self.assertEqual(g.rally, 1)
        self.assertEqual(g.best_rally, 1)

    def test_miss_does_not_bounce(self):
        g = self.running(); g.x = 65; g.y = 50; g.vx = -700; g.vy = 0
        g.step(.02)
        self.assertLess(g.vx, 0)
        self.assertEqual(g.rally, 0)

    def test_top_wall(self):
        g = self.running(); g.y = 10; g.vy = -300
        g.step(.02)
        self.assertGreater(g.vy, 0)
        self.assertGreaterEqual(g.y, 9)

    def test_frame_rate_independence(self):
        a, b = self.running(), self.running()
        for _ in range(60): a.step(1/60, 1)
        for _ in range(120): b.step(1/120, 1)
        self.assertAlmostEqual(a.x, b.x, places=5)
        self.assertAlmostEqual(a.y, b.y, places=5)
        self.assertAlmostEqual(a.left, b.left, places=5)

    def test_touch_target_clamped(self):
        g = self.running()
        for _ in range(80): g.step(.05, 0, 1000)
        self.assertEqual(g.left, 492)


if __name__ == '__main__': unittest.main()
