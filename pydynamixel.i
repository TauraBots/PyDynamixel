/*
   This is the SWIG interface for creating
   Python modules (and possibly other
   languages
*/

%module pydynamixel
%include "carrays.i"

%typemap(in) int * {
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (int *)malloc((size)*sizeof(int));
    for (i = 0 ; i < size ; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyInt_Check(o))
        $1[i] = (int)PyInt_AsLong(PyList_GetItem($input, i));
      else {
        PyErr_SetString(PyExc_TypeError, "list must contain integers");
        free($1);
        return NULL;
      }
    }
  } else {
    PyErr_SetString(PyExc_TypeError, "not a list");
    return NULL;
  }
}

%typemap(freearg) int * {
  free($1);
}


%{

extern int dxl_initialize(char *dev_name, int baudnum);
extern void dxl_terminate(int jointSocket);
extern void dxl_ping(int jointSocket, int id);
extern int dxl_read_byte(int jointSocket, int id, int address);
extern void dxl_write_byte(int jointSocket, int id, int address, int value);
extern int dxl_read_word(int jointSocket, int id, int address);
extern void dxl_write_word(int jointSocket, int id, int address, int value);
extern void dxl_sync_write_word(int jointSocket, int first_address,
                                int *ids, int *values, int total);
%}

extern int dxl_initialize(char *dev_name, int baudnum);
extern void dxl_terminate(int jointSocket);
extern void dxl_ping(int jointSocket, int id);
extern int dxl_read_byte(int jointSocket, int id, int address);
extern void dxl_write_byte(int jointSocket, int id, int address, int value);
extern int dxl_read_word(int jointSocket, int id, int address);
extern void dxl_write_word(int jointSocket, int id, int address, int value);
extern void dxl_sync_write_word(int jointSocket, int first_address,
                                int *ids, int *values, int total);

