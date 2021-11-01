from sense_hat import SenseHat
import time
from mypi import get_ip, get_eth_name, get_model, make_printable

# https://github.com/raspberrypilearning/astro-pi-guide

red = (144, 0, 0)
yellow = (144, 144, 0)
green = (0, 144, 0)
cyan = (0, 144, 144)
blue = (0, 0, 144)
purple = (144, 0, 144)
white = (144, 144, 144)
black = (0, 0, 0)


def flash_sense_hat(message="Raspberry Pi 3B+",
                    flash_repeats=3,
                    flash_duration=0.5,
                    flash_ratio=0.75,
                    colours=None,
                    message_delay=1.0):
    if colours is None:
        colours = [[(144, 144, 144), (0, 0, 0)]]
    if flash_ratio > 1 or flash_ratio < 0:
        flash_ratio = 0.5
    num_colours = len(colours)
    for flash in range(flash_repeats):
        fg_colour = colours[flash % num_colours][0]
        bg_colour = colours[flash % num_colours][1]
        for letter in message:
            sense.show_letter(letter, fg_colour)
            time.sleep(flash_duration * flash_ratio)
            sense.show_letter(letter, bg_colour)
            time.sleep(flash_duration * (1 - flash_ratio))
        # pause between message repeats
        time.sleep(message_delay)


def get_ip_parts(ip_address="0.0.0.0", separator="."):
    parts = []
    quartet = ip_address.split(".")
    counter = 0
    for part in quartet:
        parts.append(part)
        counter += 1
        if counter < 4:
            parts.append(separator)
    return parts


if __name__ == '__main__':
    sense = SenseHat()
    sense.clear(black)

    model = make_printable(get_model())
    flash_sense_hat(message=model,
                    colours=[[white, black]],
                    flash_repeats=1,
                    flash_ratio=0.975,
                    flash_duration=0.2,
                    message_delay=0.5)

    net_interfaces = [get_eth_name(), get_eth_name('w')]

    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                display_colours = [
                    [white, black],
                    [red, black], [yellow, black],
                    [green, black], [yellow, black],
                    [blue, black], [yellow, black],
                    [purple, black]
                ]
                num_colours = len(display_colours)

                for interface in net_interfaces:
                    ip = get_ip(interface=interface)
                    count = 0
                    message_parts = [f"{interface:>5}: "]
                    message_parts.extend(get_ip_parts(ip, "."))
                    print(message_parts)

                    for part in message_parts:
                        flash_sense_hat(
                            message=part,
                            colours=[display_colours[count % num_colours]],
                            flash_repeats=1,
                            flash_ratio=0.95,
                            flash_duration=0.5,
                            message_delay=0.1)
                        count += 1
                    time.sleep(1)
        time.sleep(5)
