import os
import subprocess
import re

# Regex to match the output of nm for functions: hex address, "T", function name, newline
NM_FUNC_PATTERN = re.compile(r"[a-fA-F0-9]+ T (.*)$", flags=re.MULTILINE)
WHITESPACE_PATTERN = re.compile(r"\s+")

class CppFuncSymbols:
    def __init__(self, obj_filepath):
        self.reset_symbols(obj_filepath)
        
    def __contains__(self, symbol):
        return symbol in self.mangle_map

    def reset_symbols(self, obj_filepath=None):
        '''
        reload object file function symbols from a given filepath, or the current filepath is no path is given 
        '''
        if not os.path.isfile(obj_filepath):
            print()
        if obj_filepath is not None:
            self.obj_filepath = obj_filepath
        # List function symbols, and use regex to acquire the function names only
        try:

            symbol_table = subprocess.check_output(["nm", self.obj_filepath], stderr=subprocess.STDOUT).decode('utf-8')
            self.mangled_symbols = re.findall(NM_FUNC_PATTERN, symbol_table) 
            # Generate a map from plain names to mangled names
            self.mangle_map = {}
            for mangled_func in self.mangled_symbols:
                demangled_func = subprocess.check_output(["c++filt", mangled_func], stderr=subprocess.STDOUT).decode('utf-8')
                demangled_func = re.sub(WHITESPACE_PATTERN, "", demangled_func)
                self.mangle_map[demangled_func] = mangled_func
        except subprocess.CalledProcessError as cperror:
            print("Error encountered while reading and demangling object file at: {}".format(self.obj_filepath))
            print(cperror.message)
        except Exception as e:
            print(e)

 


def mangling_map(obj_filepath):

    # Demangle the symbols, and use regex to acquire the demangled function names only
    mangled_funcs = re.findall(NM_FUNC_PATTERN, subprocess.check_output(["nm", obj_filepath]).decode('utf-8'))

    # Generate a map from plain names to mangled names
    symbol_map = {}
    for mangled_func in mangled_funcs:
        demangled_func = subprocess.check_output(["c++filt", mangled_func]).decode('utf-8')
        demangled_func = re.sub(WHITESPACE_PATTERN, "", demangled_func)
        symbol_map[demangled_func] = mangled_func
    return symbol_map
    


CppFuncSymbols("student.o") 
