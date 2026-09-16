"""Desktop Turtle renderer; run `python app.py`. Browser uses the same Game rules."""
import time
import turtle
from engine import Game


def main():
    screen = turtle.Screen()
    screen.setup(940, 620)
    screen.bgcolor('#101323')
    screen.title('Pong · The Arcade')
    screen.tracer(0)
    game = Game()
    keys = set()

    def sprite(shape, color):
        item = turtle.Turtle(shape)
        item.penup()
        item.color(color)
        return item

    left, right = sprite('square', '#9cf1e2'), sprite('square', '#eb96be')
    for paddle in (left, right):
        paddle.shapesize(4.8, .7)
    ball = sprite('circle', 'white')
    ball.shapesize(.9, .9)
    label = sprite('classic', 'white')
    label.hideturtle()
    label.goto(0, 278)
    last_label = None
    last_time = time.perf_counter()

    def toggle():
        game.pause() if game.status == 'running' else game.start()

    for key in ('Up', 'Down', 'w', 's'):
        screen.onkeypress(lambda k=key: keys.add(k), key)
        screen.onkeyrelease(lambda k=key: keys.discard(k), key)
    screen.onkey(toggle, 'space')
    screen.onkey(game.reset, 'r')
    screen.listen()

    def tick():
        nonlocal last_time, last_label
        now = time.perf_counter()
        axis = int(bool(keys & {'Down', 's'})) - int(bool(keys & {'Up', 'w'}))
        game.step(now - last_time, axis)
        last_time = now
        left.goto(-407, 270 - game.left)
        right.goto(407, 270 - game.right)
        ball.goto(game.x - 450, 270 - game.y)
        text = f'YOU {game.scores[0]}  :  {game.scores[1]} CPU   |   {game.status.upper()}   |   Space: start/pause · R: reset'
        if text != last_label:
            label.clear()
            label.write(text, align='center', font=('Courier', 12, 'normal'))
            last_label = text
        screen.update()
        screen.ontimer(tick, 8)
    tick()
    screen.mainloop()


if __name__ == '__main__':
    main()
