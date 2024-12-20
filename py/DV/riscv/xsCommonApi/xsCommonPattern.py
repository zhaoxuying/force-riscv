#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV
from base.Sequence import Sequence
import random

logic_instructions = {         
    "ANDI##RISCV" : 10,        
    "AND##RISCV": 10,          
    "ORI##RISCV": 10,          
    "OR##RISCV": 10,           
    "XORI##RISCV": 10,         
    "XOR##RISCV": 10,          
    "ORC.B##RISCV": 10,         
}                              




class xsCommonPattern(Sequence):

    #repeat_times=self.random32(1,10)
    
	def ratio(self,value=50):
		if(self.random32(1,100)<value):
			return True
		else:
			return False

	def fusedAdduw(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
			#if(self.ratio(50)):
			#	self.genInstruction("LUI##RISCV")               
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLI#RV64I#RISCV" ,{ "rs1":rand_rd,"rd":rand_rd})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
	def fusedAddwbit(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0x1})
		elif(self.ratio(33)):# to make sure probability of every condition is 25%
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0x1})
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0x1})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0x1})

	def fusedAddwbyte(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0xff})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0xff})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0xff})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":0xff})

	def fusedAddwsexth(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("SEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("SEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("SEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("SEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
	def fusedAddwzexth(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
	def fusedByte2(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":8})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":255})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":8})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":255})
	def fusedLogiclsb(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":1})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":1})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":1})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"simm12":1})
	def fusedLogicZexth(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rs1,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rd,"rs2":rand_rs2,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rs1,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			logic_instr = self.pickWeighted(logic_instructions)
			self.genInstruction(logic_instr ,{"rs1":rand_rd,"rs2":rand_rd,"rd":rand_rd})
			self.genInstruction("ZEXT.H##RISCV" ,{"rs1":rand_rd, "rd":rand_rd})
	def fusedMulw7(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":127})
			self.genInstruction("MULW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":127})
			self.genInstruction("MULW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":127})
			self.genInstruction("MULW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":127})
			self.genInstruction("MULW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedOddadd(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedOddaddw(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":1})
			self.genInstruction("ADDW##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedOrh48(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":0xF00})
			self.genInstruction("OR##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":0xF00})
			self.genInstruction("OR##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"simm12":0xF00})
			self.genInstruction("OR##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("ANDI##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"simm12":0xF00})
			self.genInstruction("OR##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSexth(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLIW##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":16})
			self.genInstruction("SRAIW##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":16})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLIW##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":16})
			self.genInstruction("SRAIW##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":16})
	def fusedSh1add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":1})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSh2add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":2})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":2})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":2})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":2})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSh3add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":3})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":3})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":3})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":3})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSh4add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":4})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":4})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":4})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":4})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSr29add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":29})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":29})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":29})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":29})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSr30add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":30})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":30})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":30})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":30})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSr31add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":31})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":31})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":31})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":31})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSr32add(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":32})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":32})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rs2, "rd":rand_rd})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":32})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":32})
			self.genInstruction("ADD##RISCV" ,{"rs1":rand_rd,"rs2":rand_rd, "rd":rand_rd})
	def fusedSzewl1(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":31})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":31})
	def fusedSzewl2(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":30})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":30})
	def fusedSzewl3(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":29})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":32})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":29})
	def fusedZexth(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":48})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":48})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLI#RV64I#RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":48})
			self.genInstruction("SRLI#RV64I#RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":48})
	def fusedZexth1(self):
		if(self.ratio(50)):
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			self.genInstruction("SLLIW##RISCV" ,{"rs1":rand_rs1,"rd":rand_rd,"shamt":16})
			self.genInstruction("SRLIW##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":16})
		else:
			gpr = self.getRandomRegisters(2,"GPR")
			rand_rd = gpr[0]
			self.genInstruction("SLLIW##RISCV" ,{"rs1":rand_rd,"rd":rand_rd,"shamt":16})
			self.genInstruction("SRLIW##RISCV" ,{"rs1":rand_rd, "rd":rand_rd,"shamt":16})


	def fusedLuiAddi(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDI##RISCV" ,{"rd":rand_rd ,"rs1":rand_rs1,"sim12":0x1})            
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDI##RISCV" ,{"rd":rand_rs1,"rs1":rand_rs1,"sim12":0x1})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDI##RISCV" ,{"rd":rand_rd,"rs1":rand_rd,"sim12":0x1})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rd,"simm20":0xffffa})
			self.genInstruction("ADDI##RISCV" ,{"rd":rand_rs2,"rs1":rand_rs1,"sim12":0x1})                      

	def fusedLuiAddiw(self):
		if(self.ratio(25)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDIW##RISCV" ,{"rd":rand_rd ,"rs1":rand_rs1,"sim12":0x1})            
		elif(self.ratio(33)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDIW##RISCV" ,{"rd":rand_rs1,"rs1":rand_rs1,"sim12":0x1})
		elif(self.ratio(50)):
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rs1,"simm20":0xffffa})
			self.genInstruction("ADDIW##RISCV" ,{"rd":rand_rd,"rs1":rand_rd,"sim12":0x1})
		else:
			gpr = self.getRandomRegisters(3,"GPR")
			rand_rd = gpr[0]
			rand_rs1 = gpr[1]
			rand_rs2 = gpr[2]
			self.genInstruction("LUI##RISCV" ,{"rd":rand_rd,"simm20":0xffffa})
			self.genInstruction("ADDIW##RISCV" ,{"rd":rand_rs2,"rs1":rand_rs1,"sim12":0x1})

	def fusionInsert(self):
		FusedInstructions = [self.fusedAdduw,self.fusedAddwbit,self.fusedAddwbyte,self.fusedAddwsexth,self.fusedAddwzexth,
							 self.fusedByte2,self.fusedLogiclsb,self.fusedLogicZexth,self.fusedMulw7,self.fusedOddadd,
							 self.fusedOddaddw,self.fusedOrh48,self.fusedSexth,self.fusedSh1add,self.fusedSh2add,self.fusedSh3add,
							 self.fusedSh4add,self.fusedSr29add,self.fusedSr30add,self.fusedSr31add,self.fusedSr32add,
							 self.fusedSzewl1,self.fusedSzewl2,self.fusedSzewl3,self.fusedZexth,self.fusedZexth1,self.fusedLuiAddi,self.fusedLuiAddiw]
		self.choice(FusedInstructions)()

	def fusionPatternPick(self):
		FusedInstructions = [self.fusedAdduw,self.fusedAddwbit,self.fusedAddwbyte,self.fusedAddwsexth,self.fusedAddwzexth,
							 self.fusedByte2,self.fusedLogiclsb,self.fusedLogicZexth,self.fusedMulw7,self.fusedOddadd,
							 self.fusedOddaddw,self.fusedOrh48,self.fusedSexth,self.fusedSh1add,self.fusedSh2add,self.fusedSh3add,
							 self.fusedSh4add,self.fusedSr29add,self.fusedSr30add,self.fusedSr31add,self.fusedSr32add,
							 self.fusedSzewl1,self.fusedSzewl2,self.fusedSzewl3,self.fusedZexth,self.fusedZexth1,self.fusedLuiAddi,self.fusedLuiAddiw]
		return self.choice(FusedInstructions)   





























    
    
    
    

        
