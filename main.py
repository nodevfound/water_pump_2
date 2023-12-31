def on_button_pressed_a():
    global start_operation
    start_operation = 1
    serial.write_string("Start Operation with ")
    serial.write_string("" + str((water_delay)))
    serial.write_line("s")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global start_operation
    start_operation = 0
    serial.write_string("Operation Stop - Status ")
    serial.write_number(start_operation)
    serial.write_line("")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_data_received():
    global command_recv, cmd, start_operation, water_delay
    command_recv = serial.read_string()
    cmd = command_recv.substr(0, len(command_recv) - 1)
    if start_operation:
        if cmd == "topup":
            basic.show_string(cmd)
            rekabit.run_motor(MotorChannel.M2, MotorDirection.FORWARD, 200)
            basic.pause(water_delay)
            rekabit.brake_motor(MotorChannel.M2)
            serial.write_line("Water Pumped!")
        elif cmd == "off":
            start_operation = 0
            serial.write_string("Operation Stop - Status ")
            serial.write_number(start_operation)
            serial.write_line("")
        elif cmd == "status":
            serial.write_number(start_operation)
            serial.write_line("")
        elif cmd == "test":
            start_operation = 2
            water_delay = 1000
            serial.write_string("Test Mode ")
            serial.write_string("" + str((water_delay)))
            serial.write_line("")
        elif cmd == "on":
            start_operation = 1
            water_delay = 5000
            serial.write_string("Start Operation with ")
            serial.write_string("" + str((water_delay)))
            serial.write_line("s")
        elif cmd == "plant":
            basic.show_string(cmd)
            rekabit.run_motor(MotorChannel.M1, MotorDirection.FORWARD, 200)
            basic.pause(2000)
            rekabit.brake_motor(MotorChannel.M1)
            serial.write_line("Water Plant!")
        else:
            serial.write_string(cmd)
            serial.write_line(" Invalid ! [Command - on, off, topup, status, test]")
serial.on_data_received(serial.delimiters(Delimiters.CARRIAGE_RETURN),
    on_data_received)

cmd = ""
command_recv = ""
water_delay = 0
start_operation = 0
basic.show_string("Init")
start_operation = 0
water_delay = 5000
led.set_brightness(10)

def on_forever():
    if start_operation == 1:
        basic.show_icon(IconNames.HEART)
        basic.show_icon(IconNames.SMALL_HEART)
    elif start_operation == 2:
        basic.show_leds("""
            # # # # #
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            """)
    else:
        basic.show_icon(IconNames.CHESSBOARD)
basic.forever(on_forever)
