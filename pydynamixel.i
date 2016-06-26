/*
   This is the SWIG interface for creating
   Python modules (and possibly other
   languages
*/

%module pydynamixel
%{

extern int dxl_initialize(int deviceIndex, int baudnum);
extern void dxl_terminate(int jointSocket);
extern void dxl_ping(int jointSocket, int id);
extern int dxl_read_byte(int jointSocket, int id, int address);
extern void dxl_write_byte(int jointSocket, int id, int address, int value);
extern int dxl_read_word(int jointSocket, int id, int address);
extern void dxl_write_word(int jointSocket, int id, int address, int value);
extern void dxl_sync_write_word(int jointSocket, int first_address,
                                int id[], int values[], int total);
%}

extern int dxl_initialize(int deviceIndex, int baudnum);
extern void dxl_terminate(int jointSocket);
extern void dxl_ping(int jointSocket, int id);
extern int dxl_read_byte(int jointSocket, int id, int address);
extern void dxl_write_byte(int jointSocket, int id, int address, int value);
extern int dxl_read_word(int jointSocket, int id, int address);
extern void dxl_write_word(int jointSocket, int id, int address, int value);
extern void dxl_sync_write_word(int jointSocket, int first_address,
                                int id[], int values[], int total);

