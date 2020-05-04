import os
import subprocess
import re
import enum
from typing import Dict, List

# Regex to match the output of nm for functions: hex address, "T", function name, newline
NM_FUNC_PATTERN = re.compile(r"[a-fA-F0-9]+ T (.*)$", flags=re.MULTILINE)
FUNC_NAME_PATTERN = re.compile(r"([a-zA-Z_][a-zA-Z0-9])*\(.*\)")
WHITESPACE_PATTERN = re.compile(r"\s+")

class ObjCopier:
    '''
    Parses mangled and demangled symbols out of an object file found at the given filepath
    Provides objcopy interface for weakening and removing symbols
    '''

    class SymbolMarker(enum.Enum):
        WEAKEN = enum.auto()
        REMOVE = enum.auto()

    def __init__(self, obj_filepath: str):
        self.obj_filepath = obj_filepath # full path to object file managed by this
        self.mangle_map: Dict[str, str] = dict() # maps from symbol name to mangled symbol name
        self.symbol_attrs: Dict[str, self.SymbolMarker] = dict() # maps from symbol name to attribute to apply
        self.reset_symbols()

    def copy(self, result_obj_filepath: str):
        cmd = ["objcopy", self.obj_filepath, result_obj_filepath]
        for symbol, attr in self.symbol_attrs.items():
            self.assert_symbol_exists(symbol)
            if attr == self.SymbolMarker.WEAKEN:
                cmd.append(f"-W{self.mangle_map[symbol]}")
                print(f"weakening {symbol}")
            elif attr == self.SymbolMarker.REMOVE:
                cmd.append(f"-N{self.mangle_map[symbol]}")
                print(f"removing {symbol}")
        print(f"running {cmd}")
        print(subprocess.check_output(cmd).decode('utf-8'))

    def assert_obj_exists(self):
        if not os.path.isfile(self.obj_filepath):
            raise FileNotFoundError(f"No file {self.obj_filepath}")

    def assert_symbol_exists(self, symbol_to_assert: str):
        if symbol_to_assert not in self.mangle_map:
            raise ValueError(f"Cannot find unmangled symbol {symbol_to_assert}\nSymbols: {self.mangle_map}")

    def mark_to_weaken(self, symbol_to_weaken: str):
        self.assert_obj_exists()
        self.assert_symbol_exists(symbol_to_weaken)
        self.symbol_attrs[symbol_to_weaken] = self.SymbolMarker.WEAKEN

    def mark_to_remove(self, symbol_to_weaken: str):
        self.assert_obj_exists()
        self.assert_symbol_exists(symbol_to_weaken)
        self.symbol_attrs[symbol_to_weaken] = self.SymbolMarker.REMOVE

    def __contains__(self, symbol):
        return symbol in self.mangle_map

    def reset_symbols(self):
        '''
        reload object file symbols
        '''
        self.assert_obj_exists()
        self.mangle_map = dict()
        self.symbol_attrs = dict()
        # List function symbols, and use regex to acquire the function names only
        try:
            cmd = ["nm", self.obj_filepath]
            print(f"Running {cmd}")
            symbol_table = subprocess.check_output(cmd).decode('utf-8')
            mangled_symbols = NM_FUNC_PATTERN.findall(symbol_table)
            print(f"Mangled symbols: {mangled_symbols}")
            # Generate a map from plain names to mangled names
            for mangled_func in mangled_symbols:
                demangled_func = subprocess.check_output(["c++filt", mangled_func]).decode('utf-8').strip()
                self.mangle_map[demangled_func] = mangled_func
            print(f"Map from demangled to mangled symbols: {self.mangle_map}")

            cmd = ["objdump", "-t", self.obj_filepath]
            print(f"Output of {cmd}: ")
            print(subprocess.check_output(cmd).decode('utf-8'))
        except subprocess.CalledProcessError as cperror:
            print("Error encountered while reading and demangling object file at: {}".format(self.obj_filepath))
            if cperror.output is not None:
                print("Erroneous call: {}".format(cperror.cmd))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # oc = ObjCopier("student.o")
    # for symbol in oc.mangle_map:
    #     oc.symbol_attrs[symbol] = ObjCopier.SymbolMarker.WEAKEN
    # oc.copy("allWeakStudent.o")

    instructor_objs = [filename for filename in os.listdir("./build") if filename.endswith(".o")]
    print(f"Collected object files: {instructor_objs}")
    with open("tested_functions.txt", "r") as tested_functions_file:
        tested_functions = {idx: tested_function.strip() for idx, tested_function in enumerate(tested_functions_file.readlines()) if tested_function}
    print(f"Testing functions: {tested_functions}")

    # TODO: Take in list of object files (instructor) and partially link it into a .o
    # Scan obj file for every symbol.  Create a map between function signature and unique ID.  Be sure to print this out!
    # For each function sig. in the obj file, make a version of the obj file with that function removed from the symbol table
    # Now for any given function to be unit tested, we have an obj file where all functions are mocked out except that exact symbol
    # Name the object file instructor_<ID>.o

    # For every student project
    # Partially link whole project into a .o
    # Weaken every symbol

    # For each ID, student.o and instructor<ID>.o.  Run the test on the resulting binary.
