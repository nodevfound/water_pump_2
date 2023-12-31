input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    start_operation = 1
    serial.writeString("Start Operation with ")
    serial.writeString("" + ("" + water_delay))
    serial.writeLine("s")
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    start_operation = 0
    serial.writeString("Operation Stop - Status ")
    serial.writeNumber(start_operation)
    serial.writeLine("")
})
serial.onDataReceived(serial.delimiters(Delimiters.CarriageReturn), function on_data_received() {
    
    command_recv = serial.readString()
    cmd = command_recv.substr(0, command_recv.length - 1)
    if (start_operation) {
        if (cmd == "topup") {
            basic.showString(cmd)
            rekabit.runMotor(MotorChannel.M2, MotorDirection.Forward, 200)
            basic.pause(water_delay)
            rekabit.brakeMotor(MotorChannel.M2)
            serial.writeLine("Water Pumped!")
        } else if (cmd == "off") {
            start_operation = 0
            serial.writeString("Operation Stop - Status ")
            serial.writeNumber(start_operation)
            serial.writeLine("")
        } else if (cmd == "status") {
            serial.writeNumber(start_operation)
            serial.writeLine("")
        } else if (cmd == "test") {
            start_operation = 2
            water_delay = 1000
            serial.writeString("Test Mode ")
            serial.writeString("" + ("" + water_delay))
            serial.writeLine("")
        } else if (cmd == "on") {
            start_operation = 1
            water_delay = 5000
            serial.writeString("Start Operation with ")
            serial.writeString("" + ("" + water_delay))
            serial.writeLine("s")
        } else if (cmd == "plant") {
            basic.showString(cmd)
            rekabit.runMotor(MotorChannel.M1, MotorDirection.Forward, 200)
            basic.pause(2000)
            rekabit.brakeMotor(MotorChannel.M1)
            serial.writeLine("Water Plant!")
        } else {
            serial.writeString(cmd)
            serial.writeLine(" Invalid ! [Command - on, off, topup, status, test]")
        }
        
    }
    
})
let cmd = ""
let command_recv = ""
let water_delay = 0
let start_operation = 0
basic.showString("Init")
start_operation = 0
water_delay = 5000
led.setBrightness(10)
basic.forever(function on_forever() {
    if (start_operation == 1) {
        basic.showIcon(IconNames.Heart)
        basic.showIcon(IconNames.SmallHeart)
    } else if (start_operation == 2) {
        basic.showLeds(`
            # # # # #
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            `)
    } else {
        basic.showIcon(IconNames.Chessboard)
    }
    
})
