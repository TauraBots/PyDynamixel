#!/usr/bin/env python

from pyjoints import DxlComm, Joint

lleg_port = DxlComm('/dev/ttyS6',8)
rleg_port = DxlComm('/dev/ttyS5',8)
torso_port = DxlComm('/dev/ttyS11',8)

lleg_joints = [Joint(i) for i in [12,14,16,22,24,26,28]]
lleg_port.attachJoints(lleg_joints)
rleg_joints = [Joint(i) for i in [11,13,15,21,23,25,27]]
rleg_port.attachJoints(rleg_joints)
torso_joints = [Joint(i) for i in [31,32,33,34,35,36,41,42,51,52,53,61,62]]
torso_servo_ids.attachJoints(torso_joints)

for i in range(1023):
    print 'lleg',
    for joint in lleg_joints:
        print joint.servo_id,":",joint.currValue,
    print 'rleg',
    for joint in rleg_joints:
        print joint.servo_id,":",joint.currValue,
    print 'trunk',
    for joint in trunk_joints:
        print joint.servo_id,":",joint.currValue,
    print
