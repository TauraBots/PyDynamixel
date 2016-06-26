import pydynamixel as dx
from time import sleep
from sys import exit

PORT = 4       # Port /dev/ttyS4
BAUDNUM = 8    # 222kbps baudrate
TORQUE_ADDR = 0x18 # Address for torque enable
GOALPOS_ADDR = 0x1E # Address for goal position

# Initialize the socket
socket = dx.dxl_initialize(PORT, BAUDNUM)
if not socket:
    exit("Failed to open socket")

# Define the target servos
servo_ids = [25,28,29,34,33]

# Enable torque
for servo_id in servo_ids:
    dx.dxl_read_word(socket, servo_id, TORQUE_ADDR, 1)

# Set goal positions
for i in range(4095):
    for servo_id in servo_ids:
        dx.dxl_write_word(socket, servo_id, GOALPOS_ADDR, i)
        sleep(0.05)

# Finish the connection with the socket
dx.dxl_terminate(socket)

