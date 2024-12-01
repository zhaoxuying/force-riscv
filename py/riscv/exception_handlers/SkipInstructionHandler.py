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
from base.exception_handlers.ReusableSequence import ReusableSequence
from riscv.exception_handlers.ExceptionHandlerContext import RegisterCallRole


class SkipInstructionHandlerRISCV(ReusableSequence):
    def generateHandler(self, **kwargs):
        try:
            handler_context = kwargs["handler_context"]
        except KeyError:
            self.error(
                "INTERNAL ERROR: one or more arguments to "
                "SkipInstructionHandlerRISCV generate method missing."
            )

        self.debug(
            "[SkipInstructionHandlerRISCV] generate handler address: 0x%x" % self.getPEstate("PC")
        )

        priv_level_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.PRIV_LEVEL_VALUE
        )
        scratch_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.TEMPORARY, 1
        )

        self.mAssemblyHelper.genIncrementExceptionReturnAddress(
            scratch_reg_index, priv_level_reg_index
        )
        self.mAssemblyHelper.genReturn()

class SkipInstructionHandlerRISCVTimerInterruptAndStoreAF(ReusableSequence):
    def generateHandler(self, **kwargs):
        try:
            handler_context = kwargs["handler_context"]
        except KeyError:
            self.error(
                "INTERNAL ERROR: one or more arguments to "
                "SkipInstructionHandlerRISCV generate method missing."
            )

        self.debug(
            "[SkipInstructionHandlerRISCV] generate handler address: 0x%x" % self.getPEstate("PC")
        )

        priv_level_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.PRIV_LEVEL_VALUE
        )
        scratch_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.TEMPORARY, 1
        )
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})
        if (self.getPEstate("PrivilegeLevel")==1):
            privMode = "S" 
        else:
            privMode = "M"
        readCause = privMode.lower() + "cause"
        xie = privMode.lower() + "ie"

        (cause_val, valid) = self.readRegister(readCause)
        isInterrupt = cause_val & 0x8000_0000_0000_0000
        if(isInterrupt):
            self.notice("Has interrupt")
            xsComdef = xsCommonDef(self.genThread)
            set_bit = 7
            xsComdef.ReadAndSetCsr(xie, set_bit, 0)
            self.writeRegister(xie, 0x0)

        self.mAssemblyHelper.genIncrementExceptionReturnAddressTimer(
            scratch_reg_index, priv_level_reg_index
        )
        self.mAssemblyHelper.genReturn()

class InstAccessFaultSkipFastHandlerRISCV(ReusableSequence):
    def generateHandler(self, **kwargs):
        try:
            handler_context = kwargs["handler_context"]
        except KeyError:
            self.error(
                "INTERNAL ERROR: one or more arguments to "
                "SkipInstructionHandlerRISCV generate method missing."
            )

        self.debug(
            "[SkipInstructionHandlerRISCV] generate handler address: 0x%x" % self.getPEstate("PC")
        )

        priv_level_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.PRIV_LEVEL_VALUE
        )
        scratch_reg_index = handler_context.getScratchRegisterIndices(
            RegisterCallRole.TEMPORARY, 1
        )

        self.mAssemblyHelper.genIncrementExceptionReturnAddress(
            scratch_reg_index, priv_level_reg_index
        )
        self.mAssemblyHelper.genReturnAccessFaultSetMepc(scratch_reg_index)
