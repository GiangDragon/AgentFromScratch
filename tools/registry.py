from tools.calculator import *
from tools.dateandtime import *
from tools.filesystem import * 


TOOL_REGISTRY = {
    "calculate" : calculate,
    "current_date_and_time" : current_date_and_time,
    "read_file" : read_file,
    "write_file" : write_file
}