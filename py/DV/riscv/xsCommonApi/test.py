#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
# FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV
from DV.riscv.xsCommonApi import xsCommonException

# use -o IterCount=10 to set generating 10 cases
class MainPFSequence(xsCommonException.PFSequence):
    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self.my_instrs = ["ADDI##RISCV", "LD##RISCV", "SD##RISCV"]
        super()._add_instrs(my_instrs)
    def generate(self, **kargs):
        super().generate()

class MainAFSequence(xsCommonException.AFSequence):
    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self.my_instrs = ["ADDI##RISCV", "LD##RISCV", "SD##RISCV"]
        super()._add_instrs(self.my_instrs)
    def generate(self, **kargs):
        super().generate()

class MainMisalignSequence(xsCommonException.MisalignSequence):
    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self.my_instrs = ["LD##RISCV", "SD##RISCV"]
        super()._add_instrs(self.my_instrs)
    def generate(self, **kargs):
        super().generate()

GenThreadInitialization = xsCommonException.AF_gen_thread_initialization
MainSequenceClass = MainAFSequence

GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV