import pydynamixel as dxl
from math import pi

TORQUE_ADDR = 0x18 # Address for torque enable
CURRPOS_ADDR = 0x24 # Address for the current position
GOALPOS_ADDR = 0x1E # Address for goal position

class DxlComm(object):
    ''' This class implements low level
    communication with the dynamixel
    protocol.
    '''

    commPort = None # path to default serial port
    baudnum = None # baudrate=2Mbps/(baudnum+1)
    socket = None # stores the socket number
    joints = [] # Database of attached joints
    joint_ids = [] # Database of servomotor ids
    total = 0 # Total number of attached joints

    def __init__(self, commPort, baudnum = 8):

        ''' The argument commPort should be
        the path to the serial device.
        The constructor optionally takes
        a baudnum argument:
           baudrate = 2Mbps / (baudnum + 1)
        If no baudnum is provided, then the
        default is 8, resulting 222.22kbps
        '''

        self.commPort = commPort
        self.baudnum = baudnum
        self.socket = dxl.initialize(commPort, baudnum)

    def attachJoint(self, joint):

        ''' This method attaches a joint so
        that the communication can be handled
        by this class
        '''

        # Registers the joint in the database
        # and sets its socket
        self.joints.append(joint)
        self.joint_ids.append(joint.servo_id)
        joint.setSocket(self.socket)
        self.total = self.total + 1

    def release(self):

        ''' This method should be called for
        the class to explicitly close the
        open socket
        '''

        dxl.terminate(self.socket)

    def sendGoalAngles(self):

        ''' Communicates the goal position for all
        servos connected to this port
        '''

        values = [j.goalValue for j in self.joints]
        dxl.sync_write_word(self.socket, GOALPOS_ADDR,
                self.joint_ids, values, self.total)

    def enableTorques(self):

        ''' Enable torque for all motors connected
        in this port.
        '''

        values = [1 for i in range(self.total)]
        dxl.sync_write_word(self.socket, TORQUE_ADDR,
                self.joint_ids, values, self.total)

    def disableTorques(self):

        ''' Disables torque for all motors connected
        to this port
        '''

        values = [0 for i in range(self.total)]
        dxl.sync_write_word(self.socket, TORQUE_ADDR,
                self.servo_ids, values, self.total)
    
    def receiveAngles(self):

        ''' This method read the current angle
        of all servos attached to this channel
        (This is sequential, not sync_read!)
        '''

        for joint in self.joints:
            joint.receiveAngle()


class Joint(object):

    ''' This class represents a Dynamixel
    servo motor.
    '''

    servo_id = None # This is the servo id
    socket = None # This stores socket number
    goalAngle = 0.0
    goalValue = 0
    currAngle = 0.0
    currValue = 0

    def __init__(self, servo_id):

        ''' The constructor takes the servo id
        as the argument.
        '''

        self.servo_id = servo_id

    def setSocket(self, socket):

        ''' Stores the socket number for later
        reference. This is called by DxlComm
        when the method attachJoint() is used
        '''

        self.socket = socket

    def setGoalAngle(self, angle):

        self.goalAngle = float(angle)
        self.goalValue = int(4096.0*angle/(2*pi))

    def sendGoalAngle(self, goalAngle = None):
        ''' Sends a command to this specific
        servomotor alone. If no parameter is
        passed then it sends the goal angle
        that was set via setGoalAngle()
        '''

        if goalAngle:
            self.setGoalAngle(goalAngle)
        dxl.write_word(self.socket, self.servo_id, \
                GOALPOS_ADDR, self.goalValue)

    def receiveAngle(self):

        ''' Reads the current position of this
        servomotor alone. The read position is
        stored and can be accessed via method
        getAngle()
        '''

        self.currValue = dxl.read_word(self.socket, self.servo_id, \
                GOALPOS_ADDR)
        self.currAngle = 2*pi*float(self.currValue)/4096.0
        return self.currAngle

    def getAngle(self):

        ''' Returns the current angle last read
        '''

        return self.currAngle

    def enableTorque(self):
        ''' Enables torque in this joint
        '''

        dxl.write_byte(self.socket, self.servo_id, \
                TORQUE_ADDR, 1)

    def disableTorque(self):
        ''' Disables torque in this joint
        '''

        dxl.write_byte(self.socket, self.servo_id, \
                TORQUE_ADDR, 0)

