all: _pydynamixel.so

_pydynamixel.so: dxl_hal.o dynamixel.o pydynamixel_wrap.o
	ld -shared dxl_hal.o dynamixel.o pydynamixel_wrap.o -o _pydynamixel.so

%.o: %.c
	gcc -fPIC -c $^ -I. -I/usr/include/python2.7

clean:
	rm -rf dxl_hal.o dynamixel.o pydynamixel_wrap.o _pydynamixel.so *.pyc

