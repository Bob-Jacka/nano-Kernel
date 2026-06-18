# Build script for custom kernel

from pathlib import Path
import os
from typing import Final
import sys

ASSEMBLY_COMPILER: Final[str] = 'nasm' # favourite assembly compiler
C_COMPILER: Final[str] = 'gcc' # favourite c compiler
LINKER: Final[str] = 'ld' # favourite linker

CURRENT_DIR: Final[str] = Path().absolute() # path to current dir

current_dir_files: list[str] = list(
		filter(lambda x: not x.startswith('.') or x.endswith('.c') or x.endswith('.asm') or x.endswith('.ld'), 
		os.listdir(CURRENT_DIR))
)
"""
Only visible files in directory
"""

kernel_file_name: Final[str] = 'kernel-100' # kernel name with version

def build_asm() -> None:
	# nasm -f elf32 start_point.asm -o kasm.o
	print('Compiling assembler code')
	if current_dir_files.__contains__('start_point.asm'):
		os.system(f'{ASSEMBLY_COMPILER} -f elf32 start_point.asm -o kasm.o')
		return
	else:
		print('Current directory not contains asm file')

def build_c() -> None:
	# gcc -m32 -c main.c -o kc.o
	print('Compiling "C" code')
	if current_dir_files.__contains__('main.c'):
		os.system(f'{C_COMPILER} -m32 main.c -o kc.o')
		return
	else:
		print('Current directory not contains main.c file')

def use_linker() -> None:
	# ld -m elf_i386 -T link.ld -o kernel kasm.o kc.o
	print('Using linking')
	if current_dir_files.__contains__('main.c') and current_dir_files.__contains__('start_point.asm'):
		os.system(f'{LINKER} -m elf_i386 -T link.ld -o kernel kasm.o kc.o')
		return
	else:
		print('Current directory not contains any of compiled files')

def clear_dir():
	print('Clear compiled files')
	os.system(f'rm kc.o {kernel_file_name} kasm.o')
	
def all_build_stages():
	if current_dir_files.__contains__(kernel_file_name):
		print('Clear before rebuild')
		clear_dir()
	build_asm()
	build_c()
	use_linker()

def run_kernel():
	if current_dir_files.__contains__(kernel_file_name):
		print('Run kernel on qemu')
		os.system(f'qemu-system-i386 -kernel {kernel_file_name}')
	else:
		print('No compiled kernel file')

if __name__ == '__main__':
	if sys.platform == 'linux':
		print('Allowed system')
		while True:
			print('Choose option:')
			print('1. Compile assembler')
			print('2. Compile C code')
			print('3. Link entities')
			print('4. Rebuild all stages') # all stages include
			
			# run kernel in emulator
			print('5. Run kernel')
			
			# other:
			print('6. Clear all compiled files')
			print('7. Exit from utility')
			
			user_input = int(input('>> '))
			match user_input:
				case 1:
					build_asm()
					continue

				case 2:
					build_c()
					continue

				case 3:
					use_linker()
					continue
					
				case 4:
					all_build_stages()
					continue	
					
				case 5:
					run_kernel()
					continue

				case 6:
					clear_dir()
					continue

				case 7:
					print('Exit from kernel build system')
					exit(0)

				case _:
					print('Wrong option, try again')
					continue
		else:
			print('System is not allowed')
