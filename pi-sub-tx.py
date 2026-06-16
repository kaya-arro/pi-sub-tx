#! /home/kaya/.local/share/pipx/venvs/cc1101/bin/python

# This script currently only works for files using EV1527 or BinRAW modulation
# TODO: Add support for more modulations

from sys import argv
from argparse import ArgumentParser
from pathlib import Path
from binascii import unhexlify
from time import sleep
import cc1101

parser = ArgumentParser(
	prog='pi-tx',
	description='Transmit signals specified by Flipper Zero .sub files',
)

parser.add_argument('files', type=Path, nargs='+')
parser.add_argument('-r', '--reps', type=int, default=1)

args = parser.parse_args(argv[1:])

demod = lambda x: {'0':'1000', '1':'1110'}[x]
hexadec = lambda x: int(''.join(x), 16)

n = 0
while n < args.reps:
	for file in args.files:
		with open(file, mode='r') as conts:
			lines = conts.readlines()

		for line in lines[2:]:
			vals = line.split()[1:]
			val = vals[0]
			if line.startswith('Frequency:'):
				freq = int(val)
			elif line.startswith('TE:'):
				baud = 1000000/int(val)
			# elif line.startswith('Protocol:'):
			# 	proto = val
			elif line.startswith('Data_RAW'):
				data = unhexlify(''.join(vals))
			elif line.startswith('Key:'):
				mod_bin = bin(hexadec(vals))[2:]
				mod_bin = mod_bin.rjust(24, '0')
				bin_str = ''.join(map(demod, mod_bin)) + '1'
				data = unhexlify('00000' + hex(int(bin_str, 2))[2:])
			# elif line.startswith('Guard_time:'):
			# 	guard = int(val)

		data *= 3
		print(data)
		with cc1101.CC1101() as transceiver:
			transceiver.set_base_frequency_hertz(freq)
			transceiver.set_symbol_rate_baud(baud)
			transceiver.set_sync_mode(cc1101.SyncMode.NO_PREAMBLE_AND_SYNC_WORD)
			transceiver.set_packet_length_mode(cc1101.PacketLengthMode.FIXED)
			transceiver.set_packet_length_bytes(len(data))
			transceiver.disable_checksum()
			transceiver.set_output_power((0, 0xC0))  # OOK modulation: (off, on)
			transceiver.transmit(data)
			print(transceiver)
			
		# sleep(0.05)
	n += 1
