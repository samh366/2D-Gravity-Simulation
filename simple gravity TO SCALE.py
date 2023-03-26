import turtle, math

window = turtle.Screen()
window.title("A simulation of the movement of plantery bodies - Samuel Hartley")

# Sun
sun = turtle.Turtle()
sun.penup()
sun.goto(0, 0)
sun.pencolor("Yellow")
sun.shape("circle")
sun.color("yellow")


# Facts
#   F = G * m1 * m2 / (d**2)
G = 6.67428e-11
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 200 / AU
time = 24 * 3600          # 24 Hours

start_x = AU
start_y = 0

# Earth
planet = turtle.Turtle()
planet.penup()
planet.speed(10)
planet.goto(start_x*SCALE, start_y*SCALE)
pp_x, pp_y = planet.pos()
planet.pendown()
earthX = start_x
earthY = start_y


# Fun presets
#pp_x = 150
#pp_y = 50
#pv_x = 0
#pv_y = 40

p_mass = 5.9724e24
s_mass = 1.98847e30

start_pv_x, start_pv_y = 0, 29780

pv_x = start_pv_x
pv_y = start_pv_y

days = 0
years = 0

def movement():
    global pv_x, pv_y, earthX, earthY, days, years
    # Calc next coordinates to go to based on gravitational force
    s_x, s_y = sun.pos()

    d_x = (s_x - earthX)
    d_y = (s_y - earthY)

    d = math.sqrt(d_x**2 + d_y**2)

    if d == 0:
        raise ZeroDivisionError("Collision between two objects")

    F = G * p_mass * s_mass / ((d)**2)

    theta = math.degrees(math.atan2(d_y, d_x))

    f_x = round(math.cos(math.radians(theta)) * F, 12)
    f_y = round(math.sin(math.radians(theta)) * F, 12)


    # Find acceleration and add too velocity
    pv_x += f_x/p_mass * time
    pv_y += f_y/p_mass * time

    # Go to new area
    earthX += pv_x * time
    earthY += pv_y * time

    # if abs(earthX) > 1500 or (pp_y) > 1500:
    #     pp_x = 0
    #     pp_y = 0
    #     pv_x = start_pv_x
    #     pv_y = start_pv_y

    planet.goto(earthX*SCALE, earthY*SCALE)

    #print(earthX*SCALE, earthY*SCALE)

    days += 1

    if days > 365:
        days = 0
        years += 1

    print("Day: %s    Year: %s" % (days, years))




while True:
    # Loop
    movement()


    
window.mainloop()