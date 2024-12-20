#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
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
from DV.riscv.trees.instruction_tree import *
from base.InstructionMap import InstructionMap

class xsCommonDef(Sequence):

    # define a CSR write def
    # ------1. impotr xsCommonDef.py in your XX.py
    # ------2. create an object of classs xsCommonDef in your XX.py
    # ------3. call thie def for example objectName.wrCSR("CSR register name", 0x5a5af) in your XX.py
    def wrCSR(self, csr_name, val):

        (csr_val_before,vld) = self.readRegister(csr_name)

        gpr = self.getRandomRegisters(4, "GPR", "0")

        for i in gpr:
            for _ in range(2):
                self.genInstruction("SLLI#RV64I#RISCV",{"rd": i,"rs1": i,"shamt": 32,},)

        imm_bit15_0 =  val & 0xFFFF
        imm_bit31_16= (val & 0xFFFF0000) >> 16
        imm_bit47_32= (val & 0xFFFF00000000) >> 32
        imm_bit63_48= (val & 0xFFFF000000000000) >>48
        self.notice("imm_bit15_0==0x%x,imm_bit31_16==0x%x,imm_bit47_32==0x%x,imm_bit63_48==0x%x"%(imm_bit15_0,imm_bit31_16,imm_bit47_32,imm_bit63_48))

        self.genInstruction("LUI##RISCV", {"rd": gpr[0],"simm20": imm_bit15_0}) 
        self.genInstruction("LUI##RISCV", {"rd": gpr[1],"simm20": imm_bit31_16})
        self.genInstruction("LUI##RISCV", {"rd": gpr[2],"simm20": imm_bit47_32})
        self.genInstruction("LUI##RISCV", {"rd": gpr[3],"simm20": imm_bit63_48})

        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[3],"rs1": gpr[3],"shamt": 36,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[2],"rs1": gpr[2],"shamt": 20,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[1],"rs1": gpr[1],"shamt": 4,},)
        self.genInstruction("SRLI#RV64I#RISCV",{"rd": gpr[0],"rs1": gpr[0],"shamt": 12,},)

        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[1]},)
        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[2]},)
        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[3]},)

        self.genInstruction("CSRRW#register#RISCV", {"csr": self.getRegisterIndex(csr_name), "rd": 0, "rs1": gpr[0]})

        (csr_val_after, _) = self.readRegister(csr_name)
        self.notice("--- write csr : {}, before write value : {:#x}, write value : 0x{}, after write : {:#x}".format(csr_name, csr_val_before, val, csr_val_after))


    def rdCSR(self, csr_name):
        
        gpr = self.getRandomRegisters(1, "GPR", "0")
        self.genInstruction("CSRRS#register#RISCV", {"csr": self.getRegisterIndex(csr_name), "rd": gpr[0], "rs1": 0})

    def wrGPR(self, gprName, val):
        
        #self.reserveRegister(name= gprName, access = "Write")
        #print("------wrGPR gprName == %s"%gprName)
        
        gpr = self.getRandomRegisters(4, "GPR", "0")
        for i in gpr:
            for _ in range(2):
                self.genInstruction("SLLI#RV64I#RISCV",{"rd": i,"rs1": i,"shamt": 32,},)

        imm_bit15_0 =  val & 0xFFFF
        imm_bit31_16= (val & 0xFFFF0000) >> 16
        imm_bit47_32= (val & 0xFFFF00000000) >> 32
        imm_bit63_48= (val & 0xFFFF000000000000) >>48
        self.notice("imm_bit15_0==0x%x,imm_bit31_16==0x%x,imm_bit47_32==0x%x,imm_bit63_48==0x%x"%(imm_bit15_0,imm_bit31_16,imm_bit47_32,imm_bit63_48))

        self.genInstruction("LUI##RISCV", {"rd": gpr[0],"simm20": imm_bit15_0}) 
        self.genInstruction("LUI##RISCV", {"rd": gpr[1],"simm20": imm_bit31_16})
        self.genInstruction("LUI##RISCV", {"rd": gpr[2],"simm20": imm_bit47_32})
        self.genInstruction("LUI##RISCV", {"rd": gpr[3],"simm20": imm_bit63_48})

        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[3],"rs1": gpr[3],"shamt": 36,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[2],"rs1": gpr[2],"shamt": 20,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": gpr[1],"rs1": gpr[1],"shamt": 4,},)
        self.genInstruction("SRLI#RV64I#RISCV",{"rd": gpr[0],"rs1": gpr[0],"shamt": 12,},)

        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[1]},)
        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[2]},)
        self.genInstruction("ADD##RISCV", {"rd":gpr[0] ,"rs1": gpr[0],"rs2": gpr[3]},)
        
        #self.unreserveRegister(gprName, "Write")
        self.genInstruction("ADD##RISCV", {"rd":gprName,"rs1":gpr[0],"rs2":0})

    def wrVPR(self, vprName, val):

        #get current vl and vtype value  
        (cur_vl, vld) = self.readRegister("vl")
        (cur_vtype, vld)= self.readRegister("vtype")
        self.notice(">>>>>> cur_vl==0x%x,cur_vtype==0x%x"%(cur_vl,cur_vtype))
        vl_recover   = cur_vl
        vill_recover = (cur_vtype & 0x8000000000000000) >> 63
        vma_recover  = (cur_vtype & 0xff) >> 7
        vta_recover  = (cur_vtype & 0x40) >> 6
        vsew_recover = (cur_vtype & 0x38) >> 3
        vlmul_recover = (cur_vtype & 0x7) 
  
        gpr = self.getRandomRegisters(2, "GPR", "0")

        gpReg0 = "x" + str(gpr[0])
        gpReg1 = "x" + str(gpr[1])

        self.reserveRegister(name= gpReg0, access = "Write")
        self.reserveRegister(name= gpReg1, access = "Write")

        val_low64bits  = val & 0xFFFFFFFFFFFFFFFF
        val_high64bits = (val & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 64
        
        # move target data into two X-registers
        self.wrGPR(gpr[0],val_low64bits)
        self.wrGPR(gpr[1],val_high64bits)
        
        # element size=64 bits, two elements, both active
        self.setVlandVtype(vill=0,vl=2,vma=0,vta=0,vsew=3,vlmul=0,mode="vsetvl") 
        # update two element by High64bits both
        self.genInstruction("VMV.V.X##RISCV",{"vd":vprName,"rs1":gpr[1]})
        # element size=64 bits, two elements, both active 
        self.setVlandVtype(vill=0,vl=1,vma=0,vta=0,vsew=3,vlmul=0,mode="vsetvl")
        # update the first element by Low64bits 
        self.genInstruction("VMV.V.X##RISCV",{"vd":vprName,"rs1":gpr[0]})

        self.unreserveRegister(name= gpReg0, access = "Write")
        self.unreserveRegister(name= gpReg1, access = "Write")

        # recover vl and vtype config
        self.setVlandVtype(vill=vill_recover,vl=vl_recover,vma=vma_recover,vta=vta_recover,vsew=vsew_recover,vlmul=vlmul_recover,mode="vsetvl")
      
    def ReadAndSetCsr(self, csr_name, set_bit, set_val):
        # read given CSR name, get old CSR val, set set_val to set_bit
        (old_csr_val, valid) = self.readRegister(csr_name)
        self.notice(">>>>>>> read old %s val is %x" % (csr_name, old_csr_val))
        new_csr_val = old_csr_val | (set_val << set_bit) 
        self.notice(">>>>>>> set csr %s bit %d to  %x" % (csr_name, set_bit, set_val))
        self.wrCSR(csr_name, new_csr_val)
        self.notice(">>>>>>> write new %s val is %x" % (csr_name, new_csr_val))

    def ReadAndSetCsr(self, csr_name, set_bit, set_val):
        # read given CSR name, get old CSR val, set set_val to set_bit
        (old_csr_val, valid) = self.readRegister(csr_name)
        self.notice(">>>>>>> read old %s val is %x" % (csr_name, old_csr_val))
        new_csr_val = old_csr_val | (set_val << set_bit) 
        self.notice(">>>>>>> set csr %s bit %d to  %x" % (csr_name, set_bit, set_val))
        self.wrCSR(csr_name, new_csr_val)
        self.notice(">>>>>>> write new %s val is %x" % (csr_name, new_csr_val))

    def randomSWPrivilege(self,**kargs):   
        # swith to another privilege level by user setting or random choice
        current_privi_level= self.getPEstate("PrivilegeLevel")
        self.notice(">>>>>> the current privilege level == %d" %(current_privi_level))
        if("privi_level" in kargs):
            priviLevel = kargs.get("privi_level")
            self.notice(">>>>>> the privilege level switch to set value == %d" %(priviLevel))
        else: 
          priviLevel = self.choice((0,1,3))
          self.notice(">>>>>> the random privilege level has to switch == %d" %(priviLevel))
        sys_call_params = {"PrivilegeLevel":priviLevel}
        self.systemCall(sys_call_params)

    def genIllegalInstr(self, pc, instr):
        
        target_pa_pc = pc
        target_va_pc = self.genVAforPA(
            PA=target_pa_pc,
            Bank="Default",
            FlatMap=0,
            Type="I",
            Size=64,
        )
        target_addr = target_va_pc
        self.notice(" >>>>>>>>>> Gen target PA is %x." % target_pa_pc)
        self.notice(" >>>>>>>>>> Gen target VA is %x." % target_va_pc)
        target_instr = instr
        imm_bit15_0 =  target_instr  & 0xFFFF
        imm_bit31_16= (target_instr  & 0xFFFF0000) >> 16
        imm_bit47_32= (target_instr  & 0xFFFF00000000) >> 32
        imm_bit63_48= (target_instr  & 0xFFFF000000000000) >> 48

        w_gpr = self.getRandomRegisters(4, "GPR", "0")

        self.genInstruction("LUI##RISCV", {"rd": w_gpr[0],"simm20": imm_bit15_0}) 
        self.genInstruction("LUI##RISCV", {"rd": w_gpr[1],"simm20": imm_bit31_16})
        self.genInstruction("LUI##RISCV", {"rd": w_gpr[2],"simm20": imm_bit47_32})
        self.genInstruction("LUI##RISCV", {"rd": w_gpr[3],"simm20": imm_bit63_48})

        self.genInstruction("SLLI#RV64I#RISCV",{"rd": w_gpr[3],"rs1": w_gpr[3],"shamt": 36,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": w_gpr[2],"rs1": w_gpr[2],"shamt": 20,},)
        self.genInstruction("SLLI#RV64I#RISCV",{"rd": w_gpr[1],"rs1": w_gpr[1],"shamt": 4,},)
        self.genInstruction("SRLI#RV64I#RISCV",{"rd": w_gpr[0],"rs1": w_gpr[0],"shamt": 12,},)

        self.genInstruction("ADD##RISCV", {"rd":w_gpr[0] ,"rs1": w_gpr[0],"rs2": w_gpr[1]},)
        self.genInstruction("ADD##RISCV", {"rd":w_gpr[0] ,"rs1": w_gpr[0],"rs2": w_gpr[2]},)
        self.genInstruction("ADD##RISCV", {"rd":w_gpr[0] ,"rs1": w_gpr[0],"rs2": w_gpr[3]},)

        self.genInstruction("SD##RISCV", {"LSTarget": target_addr, "rs2" : w_gpr[0]})
        tar_jmp_name = "x%d" % w_gpr[0]
        (tar_jmp_val, valid) = self.readRegister(tar_jmp_name)
        self.notice(" >>>>>>>>>>>>>> Reserve memory store Debug: target addr store %x" % tar_jmp_val)
        load_debug = "x%d" % w_gpr[0]
        (load_debug_val, valid) = self.readRegister(load_debug)
        self.genInstruction("LD##RISCV", {"LSTarget": target_addr, "rd" : w_gpr[1] ,"NoSkip":1})
        self.notice(" >>>>>>>>>>>>>> Reserve memory load Debug: target addr store %x" % load_debug_val)

        amo_instr = self.pickWeighted(RV_A_instructions)
        self.genInstruction(amo_instr)

        self.genInstruction("JALR##RISCV", {"BRTarget": target_addr, "NoSkip":1}) # inst 3: jmp to target

        for _ in range(20):
            self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})


    def setIntRegsToZero(self,**kargs):
        if("start" in kargs):
            start_idx = kargs.get("start")
        else:
            start_idx =20
        if("end" in kargs):
            end_idx = kargs.get("end")
        else:
            end_idx =31
        for i in range(start_idx,end_idx):
            if i == 0:
               pass
            else:
               self.genInstruction("LUI##RISCV",{"rd":i,"simm20":0x0})
               
    def setAllFpRegsToZero(self):
        for i in range(4):
            for i in range(32):
                self.genInstruction("FCVT.D.W##RISCV",{"rd":i,"rs1":0})
        
    def setAllFpRegsToRandom(self):
        for i in range(4):
            for i in range(32): 
                self.genInstruction("FCVT.D.W##RISCV",{"rd":i})

    def setAllVectorRegsToZero(self):
        vtype_val=self.readRegister("vtype")
        lmul_val=vtype_val[0] & 0x7
        self.notice(" >>>>>>>>>> current_vtype is 0x%x, current_lmul is 0x%x" %(vtype_val[0],lmul_val))        
        for i in range(4):
            for j in range(32):
                if(lmul_val ==  0):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0x0})
                elif((lmul_val == 1) and (j%2 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0x0})
                elif((lmul_val == 2) and (j%4 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0x0})
                elif((lmul_val == 3) and (j%8 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0x0})                

    def setAllVectorRegsToRandom(self):
        vtype_val=self.readRegister("vtype")
        lmul_val=vtype_val[0] & 0x7
        self.notice(" >>>>>>>>>> current_vtype is 0x%x, current_lmul is 0x%x" %(vtype_val[0],lmul_val))        
        for i in range(4):
            for j in range(32):
                if(lmul_val ==  0):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j})
                elif((lmul_val == 1) and (j%2 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j})
                elif((lmul_val == 2) and (j%4 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j})
                elif((lmul_val == 3) and (j%8 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j})                

    def setAllVectorRegsToTrue(self):
        vtype_val=self.readRegister("vtype")
        lmul_val=vtype_val[0] & 0x7
        self.notice(" >>>>>>>>>> current_vtype is 0x%x, current_lmul is 0x%x" %(vtype_val[0],lmul_val))        
        for i in range(4):
            for j in range(32):
                if(lmul_val ==  0):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0xf})
                elif((lmul_val == 1) and (j%2 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0xf})
                elif((lmul_val == 2) and (j%4 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0xf})
                elif((lmul_val == 3) and (j%8 == 0)):
                   self.genInstruction("VMV.V.I##RISCV",{"vd":j,"simm5":0xf})


    def setVlandVtype(self,**kargs): 
        # the demo of using this def is: xx.setVlandVtype(vl=2,vlmul=1,vsew=1,vta=0,vma=0,vill=0,mode="vsetivli")
        # set vector vl and vtype by one of VSETIVLI,VSETVLI,VSETVL instruction
        # parsing parameters given by user
        VLMUL=0
        VSEW=0
        if("vl" in kargs):
            VL = kargs.get("vl")
            self.notice(">>>>>> set vl by user == %d" %(VL))
        else: 
            VL = self.random32(0,16)
            self.notice(">>>>>> set vl by randmization == %d" %(VL))
        if("vlmul" in kargs):
            VLMUL = kargs.get("vlmul")
            self.notice(">>>>>> set vlmul by user == 0x%x" %(VLMUL))
        else:
            VLMUL = self.random32(0,7)
            if(VLMUL == 4): #LOW ratio to generate reserved configration data
               localRatio = self.random32(0,100)
               if(localRatio > 10):
                  VLMUL = self.random32(0,3)
               else:
                  VLMUL = VLMUL 
            else:
               pass
            self.notice(">>>>>> set vlmul by randmization == 0x%x" %(VLMUL))
        if("vsew" in kargs):
            VSEW = kargs.get("vsew")
            self.notice(">>>>>> set vsew by user == 0x%x" %(VSEW))
        else: #VLMAX=LMUL*VELN/SEW=1 are forbiden
            if(~("vlmul" in kargs) and (VLMUL == 5)):    #LMUL=1/8, SEW can only be 8
               VSEW = 0
            elif(~("vlmul" in kargs) and (VLMUL == 6)):  #LMUL=1/4, SEW can only be 8,16 
               VSEW = self.random32(0,1)
            elif(~("vlmul" in kargs) and (VLMUL == 7)):  #LMUL=1/2, SEW can only be 8,16,32
               VSEW = self.random32(0,2)
            else: #LOW ratio to generate reserved configration data
               localRatio = self.random32(0,100)
               if(localRatio > 10):
                  VSEW = self.random32(0,3)
               else:
                  VSEW = self.random32(0,7)                  
            self.notice(">>>>>> set vsew by randmization == 0x%x" %(VSEW))
        if("vta" in kargs):
            VTA = kargs.get("vta")
            self.notice(">>>>>> set vta by user == %d" %(VTA))            
        else:
            VTA = self.random32(0,1)
            self.notice(">>>>>> set vta by randmization == %d" %(VTA))
        if("vma" in kargs):
            VMA = kargs.get("vma")
            self.notice(">>>>>> set vta by user == %d" %(VMA))         
        else:
            VMA = self.random32(0,1)
            self.notice(">>>>>> set vma by randmization == %d" %(VMA))
        if("vill" in kargs):
            VILL = kargs.get("vill")
            self.notice(">>>>>> set vill by user == %d" %(VILL))          
        else:
            localRatio = self.random32(0,100)
            if(localRatio > 2):
               VILL = 0
            else:
               VILL = 1
            self.notice(">>>>>> set vill by randmization == %d" %(VILL))
        if("mode" in kargs):
            INST_MOD = kargs.get("mode")
            self.notice(">>>>>> chose vset Instruction by user == %s" %(INST_MOD))
        else:
            INST_MOD = self.choice(("vsetivli","vsetvli","vsetvl"))
            self.notice(">>>>>> chose vset Instruction by randomization == %s" %(INST_MOD))
        # contruct Vetor Lenth and Vtype value
        vl_value = VL
        vtype_value = (VILL<<8) + (VMA<<7) + (VTA<<6) + (VSEW<<3) + VLMUL
        self.notice(">>>>>> the final value to set vl == %d, vtype == 0x%x" %(vl_value,vtype_value))
        # access vl and vtype CSR register
        if(INST_MOD == "vsetivli"):
            self.genInstruction("VSETIVLI##RISCV",{"uimm5":vl_value,"zimm10":vtype_value})
        elif(INST_MOD == "vsetvli"):
            gpr = self.getRandomRegisters(1, "GPR", "0")
            self.genInstruction("LUI##RISCV",{"rd":gpr[0],"simm20":vl_value})
            self.genInstruction("SRLI#RV64I#RISCV",{"rd": gpr[0],"rs1": gpr[0],"shamt": 12,},)
            self.genInstruction("VSETVLI##RISCV",{"rs1":gpr[0],"zimm11":vtype_value})
        elif(INST_MOD == "vsetvl"):
            gpr = self.getRandomRegisters(2, "GPR", "0")
            self.genInstruction("LUI##RISCV",{"rd":gpr[0],"simm20":vl_value})
            self.genInstruction("SRLI#RV64I#RISCV",{"rd": gpr[0],"rs1": gpr[0],"shamt": 12,},)
            self.genInstruction("LUI##RISCV",{"rd":gpr[1],"simm20":vtype_value})
            self.genInstruction("SRLI#RV64I#RISCV",{"rd": gpr[1],"rs1": gpr[1],"shamt": 12,},)
            self.genInstruction("VSETVL##RISCV",{"rs1":gpr[0],"rs2":gpr[1]})
        # read all Vector CSR registers to verify the result
        self.rdCSR("vl")
        self.rdCSR("vtype")
        self.rdCSR("vlenb")
        self.rdCSR("vxrm")
        self.rdCSR("vxsat")

            
    def insertFlush(self,**kargs):
        #use direct jump inst to triggle RTL-flush
        #the demo of using this def is xxx.insertFlush(ratio=100)
        if("ratio" in kargs):
            ratioLocal = kargs.get("ratio")
            self.notice(">>>>>> set insert Flush ratio by user == %d" %(ratioLocal))
        else: 
            ratioLocal = self.random32(1,99)
            self.notice(">>>>>> set insert Flush ratio by randmization == %d" %(ratioLocal))
        ratioBase=self.random32(0,100)        
        self.notice(">>>>>> set insert Flush ratioBase == %d" %(ratioBase))        
        if(ratioBase < ratioLocal):
           cur_pc = self.getPEstate("PC")
           br_imm = self.random32(1,10) * 4
           gpr = self.getRandomRegisters(2, "GPR", "0")
           self.genInstruction("LUI##RISCV", {"rd": gpr[0],"simm20": self.random32(1,2)}) 
           self.genInstruction("LUI##RISCV", {"rd": gpr[1],"simm20": self.random32(1,2)})
           inst_mod = self.random32(0,3)
           self.notice("cur_pc == 0x%x,br_imm == 0x%x,inst_mod == %d"%(cur_pc,br_imm,inst_mod)) 
           if inst_mod   == 0:
              self.genInstruction("BEQ##RISCV",{"rs2":gpr[0],"rs1":gpr[1],"simm12":br_imm,"NoRestriction":"1"})
           elif inst_mod == 1:
              self.genInstruction("BNE##RISCV",{"rs2":gpr[0],"rs1":gpr[1],"simm12":br_imm,"NoRestriction":"1"})
           elif inst_mod == 2:
              self.genInstruction("BLT##RISCV",{"rs2":gpr[0],"rs1":gpr[1],"simm12":br_imm,"NoRestriction":"1"})
           else:
              self.genInstruction("BGE##RISCV",{"rs2":gpr[0],"rs1":gpr[1],"simm12":br_imm,"NoRestriction":"1"})
        else:
          pass

    def insertIntLoadCancel(self,**kargs):
        #use direct jump inst to triggle RTL-flush
        #the demo of using this def is xxx.insertIntLoadCancel(ratio=100)
        if("ratio" in kargs):
            ratioLocal = kargs.get("ratio")
            self.notice(">>>>>> set insert IntLoadCancel ratio by user == %d" %(ratioLocal))
        else: 
            ratioLocal = self.random32(1,99)
            self.notice(">>>>>> set insert IntLoadCancel ratio by randmization == %d" %(ratioLocal))
        ratioBase=self.random32(0,100)        
        self.notice(">>>>>> set insert IntLoadCancel ratioBase == %d" %(ratioBase))        
        if(ratioBase < ratioLocal):
          ld_inst1=LD_Int_map.pick(self.genThread)
          gpr = self.getRandomRegisters(2,"GPR","0")
          targetVA1= self.genVA(Type="D",Align=8, Range="0x80050000-0x800F0000")
          targetVA2=  targetVA1 + 0x1000
          self.wrGPR(gpr[1],targetVA2)
          self.genInstruction(ld_inst1, {"rd":gpr[0],"rs1":gpr[1],"simm12":0})
          self.notice(">>>>>> the dst IntReg index == %d" %(gpr[0]))
          return gpr[0]
        else:
          gpr = self.getRandomRegisters(1,"GPR","0")
          self.genInstruction("ADD##RISCV", {"rd":gpr[0]})
          self.notice(">>>>>> the dst IntReg index == %d" %(gpr[0]))
          return gpr[0]           

    def insertFpLoadCancel(self,**kargs):
        #use direct jump inst to triggle RTL-flush
        #the demo of using this def is xxx.insertFpLoadCancel(ratio=100)
        if("ratio" in kargs):
            ratioLocal = kargs.get("ratio")
            self.notice(">>>>>> set insert FpLoadCancel ratio by user == %d" %(ratioLocal))
        else: 
            ratioLocal = self.random32(1,99)
            self.notice(">>>>>> set insert FpLoadCancel ratio by randmization == %d" %(ratioLocal))
        ratioBase=self.random32(0,100)        
        self.notice(">>>>>> set insert FpLoadCancel ratioBase == %d" %(ratioBase))        
        if(ratioBase < ratioLocal):
          ld_inst1=LD_Float_map.pick(self.genThread)
          gpr = self.getRandomRegisters(1,"GPR","0")
          fpr = self.getRandomRegisters(1,"FPR","0")
          targetVA1= self.genVA(Type="D",Align=8, Range="0x80050000-0x800F0000")
          targetVA2=  targetVA1 + 0x1000
          self.wrGPR(gpr[0],targetVA2)
          self.genInstruction(ld_inst1, {"rd":fpr[0],"rs1":gpr[0],"simm12":0})
          self.notice(">>>>>> the dst FpReg index == %d" %(fpr[0]))
          return fpr[0]
        else:
          fpr = self.getRandomRegisters(1,"FPR","0")
          self.genInstruction("FADD.S##RISCV", {"rd":fpr[0]})
          self.notice(">>>>>> the dst FpReg index == %d" %(fpr[0]))
          return fpr[0]


##  Points to the MainSequence defined in this file
#MainSequenceClass = MainSequence
#
##  Using GenThreadRISCV by default, can be overriden with extended classes
#GenThreadClass = GenThreadRISCV
#
##  Using EnvRISCV by default, can be overriden with extended classes
#EnvClass = EnvRISC
