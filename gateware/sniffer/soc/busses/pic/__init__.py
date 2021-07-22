from nmigen import Elaboratable, Module
from nmigen.utils import log2_int
from nmigen_soc.memory import MemoryMap
from .types import *

__all__ = ('PICBus')

class PICBus(Elaboratable):
	def __init__(self):
		self.processor = None
		self.memoryMap = MemoryMap(addr_width = 7, data_width = 8)

	def add_processor(self, processor):
		assert self.processor == None, "Cannot add more than one processor to the bus"
		self.processor = processor

	def add_register(self, *, address) -> Register:
		register = Register()
		self.memoryMap.add_resource(register, size = 1, addr = address)
		return register

	def add_memory(self, *, address, size) -> Memory:
		 # Validate size and create Memory instance..
		memory = Memory(address_width = log2_int(size))
		self.memoryMap.add_resource(memory, size = size, addr = address)
		return memory

	def elaborate(self, platform):
		assert self.processor != None, "Must provide a processor for PICBus to connect to"
		self.memoryMap.freeze()

		m = Module()
		processor = Processor()

		m.d.comb += self.processor.pBus.connect(processor)

		for resource, addressRange in self.memoryMap.all_resources():
			addressBegin, addressEnd, dataWidth = addressRange
			assert dataWidth == 8
			addressCount = addressEnd - addressBegin
			addressSlice = log2_int(addressCount)
			with m.If(processor.address[addressSlice:] == (addressBegin >> addressSlice)):
				m.d.comb += [
					resource.read.eq(processor.read),
					processor.readData.eq(resource.readData),
					resource.write.eq(processor.write),
					resource.writeData.eq(processor.writeData),
				]
				if isinstance(resource, Memory):
					m.d.comb += resource.address.eq(processor.address[:addressSlice])

		return m
