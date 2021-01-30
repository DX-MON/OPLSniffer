from nmigen import Elaboratable, Module, Signal
from .types import ALUOpcode

__all__ = ["ALU"]

class ALU(Elaboratable):
	def __init__(self):
		self.lhs = Signal(8)
		self.rhs = Signal(8)
		self.result = Signal(8)

		self.operation = Signal(ALUOpcode)

	def elaborate(self, platform):
		m = Module()
		lhs = self.lhs
		rhs = self.rhs
		result = self.result

		with m.Switch(self.operation):
			with m.Case(ALUOpcode.ADD):
				m.d.sync += [
					result.eq(lhs + rhs)
				]
			with m.Case(ALUOpcode.SUB):
				m.d.sync += [
					result.eq(lhs - rhs)
				]
			with m.Case(ALUOpcode.INC):
				m.d.sync += [
					result.eq(rhs + 1)
				]
			with m.Case(ALUOpcode.DEC):
				m.d.sync += [
					result.eq(rhs - 1)
				]
			with m.Case(ALUOpcode.AND):
				m.d.sync += [
					result.eq(lhs & rhs)
				]
			with m.Case(ALUOpcode.OR):
				m.d.sync += [
					result.eq(lhs | rhs)
				]
			with m.Case(ALUOpcode.XOR):
				m.d.sync += [
					result.eq(lhs ^ rhs)
				]

		return m