import pydynamixel as dxl
from math import pi

TORQUE_ADDR = 0x18 # Address for torque enable
CURRPOS_ADDR = 0x24 # Address for the current position
GOALPOS_ADDR = 0x1E # Address for goal position
MAXTORQUE_ADDR = 0x0E # Address for maximum torque
MAXTORQUELIMIT = 767 # Maximum torque possible

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

    def attachJoints(self, joints):
        
        ''' This method attaches several joints
        so that the communication can be
        handled by this class
        '''

        for joint in joints:
            self.attachJoint(joint)

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

    def sendMaxTorques(self, maxTorque = None):

        ''' Communicates the max torques for all
        servos connected to this port. Optionally
        the argument maxTorque can be provided.
        If provided, the same maxTorque will be
        set to all attached joints.
        '''

        if maxTorque:
            for j in self.joints:
                j.setMaxTorque(maxTorque)

        values = [j.maxTorque for j in self.joints]
        dxl.sync_write_word(self.socket, MAXTORQUE_ADDR,
                self.joint_ids, values, self.total)

    def _syncWrite(self, socket, addr, ids, values):
        total = len(ids)
        if total <= 20:
            print "_syncWrite <= 20", socket, addr, ids, values
            dxl.sync_write_word(socket, addr,\
                  ids, values, total)
        else:
            print "_syncWrite > 20", socket, addr, ids[:20], values[:20]
            print "_syncWrite > 20", socket, addr, ids[20:], values[20:]
            dxl.sync_write_word(socket, addr,\
                  ids[:20], values[:20], 20)
            dxl.sync_write_word(socket, addr,\
                  ids[20:], values[20:], total - 20)

    def enableTorques(self):

        ''' Enable torque for all motors connected
        in this port.
        '''

        values = [1]*self.total
	self._syncWrite(self.socket, TORQUE_ADDR, \
                self.joint_ids, values)

    def disableTorques(self):

        ''' Disables torque for all motors connected
        to this port
        '''

        values = [0]*self.total
	self._syncWrite(self.socket, TORQUE_ADDR, \
                self.joint_ids, values)

    def receiveCurrAngles(self):

        ''' This method read the current angle
        of all servos attached to this channel
        (This is sequential, not sync_read!)
        '''

        for joint in self.joints:
            joint.receiveCurrAngle()

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
    centerValue = 0
    maxTorque = 767 # This is the maximum

    def __init__(self, servo_id, centerValue = 0):

        ''' The constructor takes the servo id
        as the argument. Argument centerValue
        can be set to calibrate the zero
        position of the servo.
        '''

        self.servo_id = servo_id
        self.centerValue = centerValue

    def setCenterValue(self, centerValue):

        ''' Sets the calibration of the zero
        for the joint. This can also be passed
        in the constructor.
        '''

        self.centerValue = centerValue

    def setSocket(self, socket):

        ''' Stores the socket number for later
        reference. This is called by DxlComm
        when the method attachJoint() is used
        '''

        self.socket = socket

    def setMaxTorque(self, maxTorque):

        ''' Sets the maximum torque (does not
        send it yet!). To send it the method
        sendMaxTorque() must be called.
        '''

        self.maxTorque = min(int(maxTorque), MAXTORQUELIMIT)

    def sendMaxTorque(self, maxTorque = None):

        ''' Sends a command to this specific
        servomotor to set its maximum torque.
        If the argument maxTorque is not
        provided, then it sends the last
        value set using setMaxTorque().
        '''

        if maxTorque:
            self.setMaxTorque(maxTorque)
        dxl.write_word(self.socket, self.servo_id, \
                MAXTORQUE_ADDR, self.maxTorque)

    def setGoalAngle(self, angle):

        self.goalAngle = float(angle)
        self.goalValue = int(2048.0*angle/pi) \
                + self.centerValue

    def sendGoalAngle(self, goalAngle = None):
        ''' Sends a command to this specific
        servomotor to set its goal angle.
        If no parameter is passed then it
        sends the goal angle that was set
        via setGoalAngle()
        '''

        if goalAngle:
            self.setGoalAngle(goalAngle)
        dxl.write_word(self.socket, self.servo_id, \
                GOALPOS_ADDR, self.goalValue)

    def receiveCurrAngle(self):

        ''' Reads the current position of this
        servomotor alone. The read position is
        stored and can be accessed via method
        getAngle()
        '''

        self.currValue = dxl.read_word(self.socket, self.servo_id, \
                CURRPOS_ADDR) - self.centerValue
        self.currAngle = pi*float(self.currValue)/2048.0
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

