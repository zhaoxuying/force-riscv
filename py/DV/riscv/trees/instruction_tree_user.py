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
from base.InstructionMap import InstructionMap

#"""
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Groupings from ISA instruction listings
#
#References...
#  The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA
#  > Chapter 24 - RV32/64G Instruction Set Listings
#  > Chapter 16.8 - RVC Instruction Set Listings - Tables 16.5-16.7
#------------------------------------------------------------------------------
#
#Extension       Component extensions and/or instructions
#------------------------------------------------------------------------------
#RV32I             completed
#RV64I             completed
#RV32F             completed
#RV64F             completed
#RV32D             completed
#RV64D             completed
#RV32M             completed
#RV64M             completed
#RV32A             completed
#RV64A             completed
#Zicsr             completed
#Zifencei          completed
#RV_A              completed     =   RV32A + RV64A
#RV_C              completed         Does not contain instructions exclusive to
#                                    RV32C or RV128C.
#RV_V              pending       =   ALU_V + LDST_V
#RV_G              completed     =   RV32I + RV64I + RV32F + RV64F + RV32D +
#                                    RV64D + RV32M + RV64M + RV32A + RV64A +
#                                    Zicsr + Zifencei
#                                    (More succinctly, RV64I plus the standard
#                                    extensions: I, M, A, F, D, Zicsr, Zifencei)
#Trap_Return       pending       =   {URET, SRET, MRET, WFI}
#Fence             pending       =   {SFENCE.VMA, HFENCE.BVMA, HFENCE.GVMA}
#
#RV_ALL_NoVector   pending       =   RV_G + RV_C + Trap_Return + Fence
#RV_ALL            pending       =   ALL_RISCV_NoVector + RV_V
#
#
#
#Additional groups focused on functional units
#----------------------------------------------------------
#
#Regular loads and stores
#  LD_Int            completed
#  LD_Float          completed
#  ST_Int            completed
#  ST_Float          completed
#  LDST_Int          completed       =   LD_Int + ST_Int
#  LDST_Float        completed       =   LD_Float + ST_Float
#  LDST_IntFloat     completed       =   LDST_Int + LDST_Float
#  LDST_IFC          completed       =   LDST_IntFloat + LDST_C
#  LDST_All          partially completed, missing V
#                                    =   LDST_IntFloat + LDST_C + (LDST_V)
#  LDST_Byte         completed
#  LDST_Half         completed
#  LDST_Word         completed
#  LDST_Double       completed
#
#Regular ALU Int
#  ALU_Int32         completed       =   RV32I - loads - stores - branches -
#                                        umps
#  ALU_Int64         completed       =   RV64I - loads - stores
#  ALU_M             completed       =   RV32M + RV64M
#  ALU_Int_All       completed       =   ALU_Int32 + ALU_Int64 + ALU_M +
#                                        ALU_Int_C
#  BranchJump        completed
#
#Regular ALU Float
#  ALU_Float_Single  completed       =   RV32S + RV64S - loads - stores - FCVT
#  ALU_Float_Double  completed       =   RV32D + RV64D - loads - stores - FCVT
#  FCVT              completed
#  ALU_Float_All     completed       =   ALU_Float_Single + ALU_Float_Double
#
#C extension
#  LD_C              completed
#  ST_C              completed
#  LDST_C            completed       =   LD_C + ST_C
#  BranchJump_C      completed
#  ALU_Int_C         completed
#
#V extension
#  LD_V              pending
#  ST_V              pending
#  LDST_V            pending         =   LD_V + ST_V
#  ALU_V             pending
#
#==============================================================================
#"""

Int_1src_instructions ={
    "C.ADDI##RISCV": 10,
    "C.ADDI16SP##RISCV": 10,
    "C.ADDI4SPN##RISCV": 10,
    "C.ADDIW##RISCV": 10,
    "C.ANDI##RISCV": 10,
    "C.SLLI##RISCV": 10,
    "C.SLLI64##RISCV": 10,
    "C.SRAI64##RISCV": 10,
    "C.SRLI64##RISCV": 10,
    "ADDI##RISCV": 10,
    "ANDI##RISCV": 10,
    "ORI##RISCV": 10,
    "SLLI#RV32I#RISCV": 10,
    "SLTI##RISCV": 10,
    "SLTIU##RISCV": 10,
    "SRAI#RV32I#RISCV": 10,
    "SRLI#RV32I#RISCV": 10,
    "XORI##RISCV": 10,
    "ADDIW##RISCV": 10,
    "SLLI#RV64I#RISCV": 10,
    "SLLIW##RISCV": 10,
    "SRAI#RV64I#RISCV": 10,
    "SRAIW##RISCV": 10,
    "SRLI#RV64I#RISCV": 10,
    "SRLIW##RISCV": 10,
}
Int_1src_map= InstructionMap("Int_1src_instructions", Int_1src_instructions)

Int_2src_instructions ={
    "C.ADD##RISCV": 10,
    "C.ADDW##RISCV": 10,
    "C.AND##RISCV": 10,
    "C.SUB##RISCV": 10,
    "C.SUBW##RISCV": 10,
    "ADD##RISCV": 10,
    "AND##RISCV": 10,
    "OR##RISCV": 10,
    "SLL##RISCV": 10,
    "SLT##RISCV": 10,
    "SLTU##RISCV": 10,
    "SRA##RISCV": 10,
    "SRL##RISCV": 10,
    "SUB##RISCV": 10,
    "XOR##RISCV": 10,
    "ADDW##RISCV": 10,
    "SLLW##RISCV": 10,
    "SRAW##RISCV": 10,
    "SRLW##RISCV": 10,
    "SUBW##RISCV": 10,

}
Int_2src_map= InstructionMap("Int_2src_instructions", Int_2src_instructions)

Fp_1src_instructions ={

    "FCLASS.S##RISCV": 10,
    "FSQRT.S##RISCV": 10,
    "FSQRT.D##RISCV": 10,
    "FSQRT.H##RISCV": 10,
    "FMV.W.X##RISCV": 10,
    "FMV.X.W##RISCV": 10,
    "FCVT.S.W##RISCV": 10,
    "FCVT.S.WU##RISCV": 10,
    "FCVT.W.S##RISCV": 10,
    "FCVT.WU.S##RISCV": 10,
    "FCVT.L.S##RISCV": 10,
    "FCVT.LU.S##RISCV": 10,
    "FCVT.S.L##RISCV": 10,
    "FCVT.S.LU##RISCV": 10,
    "FCVT.D.S##RISCV": 10,
    "FCVT.D.W##RISCV": 10,
    "FCVT.D.WU##RISCV": 10,
    "FCVT.S.D##RISCV": 10,
    "FCVT.W.D##RISCV": 10,
    "FCVT.WU.D##RISCV": 10,
    "FCVT.D.L##RISCV": 10,
    "FCVT.D.LU##RISCV": 10,
    "FCVT.L.D##RISCV": 10,
    "FCVT.LU.D##RISCV": 10,
    "FMV.D.X##RISCV": 10,
    "FMV.X.D##RISCV": 10,

}
Fp_1src_map= InstructionMap("Fp_1src_instructions", Fp_1src_instructions)

Fp_2src_instructions ={

     "FADD.D##RISCV": 10,
     "FDIV.D##RISCV": 10,
     "FEQ.D##RISCV": 10,
     "FLE.D##RISCV": 10,
     "FLT.D##RISCV": 10,
     "FMADD.D##RISCV": 10,
     "FMAX.D##RISCV": 10,
     "FMIN.D##RISCV": 10,
     "FMSUB.D##RISCV": 10,
     "FMUL.D##RISCV": 10,
     "FNMADD.D##RISCV": 10,
     "FNMSUB.D##RISCV": 10,
     "FSGNJ.D##RISCV": 10,
     "FSGNJN.D##RISCV": 10,
     "FSGNJX.D##RISCV": 10,
     "FSQRT.D##RISCV": 10,
     "FSUB.D##RISCV": 10,
     "FDIV.S##RISCV": 10,
     "FDIV.D##RISCV": 10,
}
Fp_2src_map= InstructionMap("Fp_2src_instructions", Fp_2src_instructions)


