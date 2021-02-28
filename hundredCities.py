import tkinter as tk


def create_dictionary(file):
    dictionary = {}
    with open(file, "r") as f:
        index = 0
        for line in f:
            city = line[:line.find("\t")]
            population = line[line.find("\t") + 1: -1]
            dictionary[city] = [int(population), False]
            index += 1
    return dictionary


us_cities = create_dictionary("UScities.txt")
world_cities = create_dictionary("Worldcities.txt")

score = 0
cities = None

position = [0, 0]

intro_stage = True
outro_stage = False

user_input = None
input_space = None

scored_cities = [["New York City", 54465]]


def make_guess(guess, city_list):
    global score
    if guess.title() in city_list:
        if not city_list[guess.title()][1]:
            city_list[guess.title()][1] = True
            score += city_list[guess.title()][0]
            return city_list[guess.title()][0]
        else:
            return 1
    else:
        return 2


window = tk.Tk()
window.title("100 Cities")
window.geometry("1920x1080")

intro_text = tk.Label(window, text="100 Cities", font=("Courier", 100,), justify="center")
intro_text.place(x=560, y=150)

us_text = tk.Label(window, text="  USA  ", font=("Courier", 50,), justify="center", foreground="white", bg="blue")
us_text.place(x=600, y=600)

world_text = tk.Label(window, text=" World ", font=("Courier", 50,), justify="center", foreground="white", bg="green")
world_text.place(x=1020, y=600)


def add_interface():
    global score, input_space
    title_text = tk.Label(window, text="100 Cities", font=("Courier", 50,), justify="center")
    title_text.place(x=30, y=20)

    score_text = tk.Label(window, text="Score:", font=("Courier", 30,), justify="center", foreground="red")
    score_text.place(x=1750, y=865)

    input_space = tk.Entry(window, font=("Courier", 50))
    input_space.place(x=30, y=900)
    input_space.bind("<Return>", call_guess)

    display_score()


def call_guess(event):
    global input_space, cities, scored_cities
    result = make_guess(input_space.get(), cities)
    if result > 2:
        scored_cities.append([input_space.get().title(), result])
        display_score()
        add_city()
    elif result == 1:
        print("Already guessed!")
    else:
        print("Not a top 100 city!")
    input_space.delete(0, "end")


def display_score():
    global score
    if len(str(score)) == 1:
        offset = 0
    elif len(str(score)) == 6:
        offset = 240
    elif len(str(score)) == 7:
        offset = 320
    elif len(str(score)) == 8:
        offset = 360
    else:
        offset = 400
    print(len(str(score)))
    score_count = tk.Label(window, text=str(f"{score:,d}"), font=("Courier", 50,), justify="right", foreground="red")
    score_count.place(x=1850-offset, y=920)


def add_city():
    global scored_cities
    count = len(scored_cities)

    if count >= 38:
        return

    city_to_add = scored_cities[-1][0]
    population_to_add = scored_cities[-1][1]
    multiplier = 60

    if city_to_add == "Colorado Springs":
        city_to_add = "CO Springs"

    if city_to_add == "Ho Chi Minh City":
        city_to_add = "HCM City"

    offset = 0
    if count < 14:
        start_pos = [38, 5]
    elif count < 26:
        start_pos = [638, 125]
    else:
        start_pos = [1233, 5]
        offset = 4

    spacing = ""
    if len(city_to_add) < 8:
        spacing = "\t"
    city_info = city_to_add + "\t" + spacing + str(f"{population_to_add:,d}")

    scored_city = tk.Label(window, text=city_info, font=("Courier", 25,), foreground="blue")
    scored_city.place(x=start_pos[0], y=start_pos[1] + ((count + offset) % 14) * multiplier)


def click(event):
    if intro_stage:
        global cities, us_cities, world_cities, intro_text, us_text, world_text
        next_stage = False
        if 680 < position[0] < 900 and 600 < position[1] < 680:
            cities = us_cities
            next_stage = True
        elif 1020 < position[0] < 1240 and 600 < position[1] < 680:
            cities = world_cities
            next_stage = True
        if next_stage:
            intro_text.destroy()
            us_text.destroy()
            world_text.destroy()
            add_interface()


def motion(event):
    global position
    position[0] = window.winfo_pointerx() - window.winfo_rootx()
    position[1] = window.winfo_pointery() - window.winfo_rooty()


window.bind("<Button-1>", click)
window.bind("<Motion>", motion)

window.mainloop()