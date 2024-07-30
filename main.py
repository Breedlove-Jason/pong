from turtle import Turtle, Screen
import random

score1 = 0
score2 = 0

paddle1 = Turtle()
paddle2 = Turtle()

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)
screen.title("Pong Game")
screen.listen()

ball = Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)


def create_paddle(paddle, x, y):
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, y)


def move_up(paddle):
    y = paddle.ycor()
    if y < 250:  # Check if the paddle is within the top boundary
        y += 20
        paddle.sety(y)


def move_down(paddle):
    y = paddle.ycor()
    if y > -250:  # Check if the paddle is within the bottom boundary
        y -= 20
        paddle.sety(y)


scoreboard = Turtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)


def update_score():
    global scoreboard
    scoreboard.clear()
    scoreboard.write(f"{score1} {score2}", align="center",
                     font=("Courier", 24, "normal"))
    screen.update()


def draw_center_line():
    center_line = Turtle()
    center_line.color("white")
    center_line.penup()
    center_line.goto(0, 300)
    center_line.setheading(270)
    for _ in range(15):
        center_line.pendown()
        center_line.forward(20)
        center_line.penup()
        center_line.forward(20)
    screen.update()


direction = 1  # 1 for up, -1 for down
direction_x = random.choice([1, -1])
direction_y = random.choice([1, -1])


def move_ball(ball, paddle1, paddle2):
    global direction_x, direction_y, score1, score2
    x = ball.xcor()
    x += direction_x * 1.5  # Increase the speed of the ball
    y = ball.ycor()
    y += direction_y * 1.5  # Increase the speed of the ball
    ball.goto(x, y)
    # ball bounces of top and bottom
    if ball.ycor() > 290 or ball.ycor() < -290:
        direction_y *= -1

    # ball goes past paddle, other player scores
    if ball.xcor() > 300:
        score1 += 1
        ball.goto(0, 0)
        direction_x *= -1
    if ball.xcor() < -300:
        score2 += 1
        ball.goto(0, 0)
        direction_x *= -1

    # ball bounces of paddle
    # Modify the move_ball function's collision detection as follows:
    if (340 > ball.xcor() > 280 and paddle1.ycor() + 50 > ball.ycor() > paddle1.ycor() - 50) or \
            (-340 < ball.xcor() < -280 and paddle2.ycor() + 50 > ball.ycor() > paddle2.ycor() - 50):
        direction_x *= -1
    update_score()
    screen.update()


def computer_move_paddle(paddle):
    global direction
    y = paddle.ycor()
    y += direction
    paddle.sety(y)
    screen.update()
    if paddle.ycor() >= 250:
        direction = -1
    elif paddle.ycor() <= -250:
        direction = 1


update_score()
draw_center_line()
create_paddle(paddle1, 280, 0)
create_paddle(paddle2, -280, 0)
screen.update()

while True:
    screen.onkeypress(lambda: move_up(paddle2), "Up")
    screen.onkeypress(lambda: move_down(paddle2), "Down")
    move_ball(ball, paddle1, paddle2)
    computer_move_paddle(paddle1)
    screen.update()

screen.mainloop()
screen.exitonclick()
