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
from DV.riscv.xsCommonApi.PageFaultSequence import PageFaultSequence
from riscv.ModifierUtils import PageFaultModifier, displayPageInfo
import RandomUtils
from riscv.AssemblyHelperRISCV import AssemblyHelperRISCV
from DV.riscv.xsCommonApi.xsCommonDef import *

class xsCommonModifyPte(PageFaultSequence):
    def random_modify_pte_rights(self, page_target_addr, radical=False, pagefault_level=2):
        # set pte function
        def random_set_pte_rights( reg_data):
            def set_bit(value, bit, bit_val):
                if bit_val:
                    return value | (1 << bit)
                else:
                    return value & ~(1 << bit)
            def modify_random_bits(reg_data, num_bits_to_change):
                bits_to_change = set()
                while len(bits_to_change) < num_bits_to_change:
                    sel_bit = RandomUtils.random32(0, 7)
                    bits_to_change.add(sel_bit)
                for bit in list(bits_to_change):
                    bit_val = RandomUtils.random32(0, 1)
                    reg_data = set_bit(reg_data, bit, bit_val)
                return reg_data
            def weighted_random():
                rand_num = RandomUtils.random32(0, 100)
                if rand_num < 72:   
                    return 1
                elif rand_num < 79: 
                    return 2
                elif rand_num < 85: 
                    return 3
                elif rand_num < 90: 
                    return 4
                elif rand_num < 94: 
                    return 5
                elif rand_num < 97: 
                    return 6
                elif rand_num < 99: 
                    return 7
                else:               
                    return 8
            # I want to random set one bit has more probability, set multi-bits has lower probalitiy
            num_bits_to_change = weighted_random()
            self.notice("Before modified reg_data: 0x%x" % reg_data)
            reg_data = modify_random_bits(reg_data, num_bits_to_change)
            self.notice("After modified reg_data: 0x%x" % reg_data)
            return reg_data

        # Start from here
        # First get Page Info, fetch PTEs addr
        page_obj = self.getPageInfo(page_target_addr, "VA", 0)
        displayPageInfo(self, page_obj)
        self.notice("Current PageFault Level is %d" % pagefault_level)
        get_page_info = page_obj.get('Page') # page descriptions
        get_table2_info = page_obj.get('Table#2') # level 2 pte descriptions
        get_table1_info = page_obj.get('Table#1') # level 1 pte descriptions
        get_table0_info = page_obj.get('Table#0') # leaf pte descriptions
        # choose a pte level
        if(get_table0_info is not None):
            tables = [get_table2_info, get_table1_info, get_table0_info]
            self.notice(">>>>>>>>>>> Query page level: is 3 level page, 4k page")
        elif(get_table1_info is not None):
            tables = [get_table2_info, get_table1_info]
            self.notice(">>>>>>>>>>> Query page level: is 2 level page, 2M page")
        elif(get_table2_info is not None):
            tables = [get_table2_info]
            self.notice(">>>>>>>>>>> Query page level: is 1 level page, 1G page")
        else:
            self.notice("NO PAGE here! Cant modify PTE.")
            return

        if(radical): # radcial means has probability to modify all level pte
            sel_pte_table = self.choice(tables) # but modify high level pte has more probability fail
        else:
            sel_pte_table = tables[-1]

        target_addr = sel_pte_table['DescriptorAddr']

        self.notice("Select to modify pte level: %d" % sel_pte_table['Level'])
        # Choice a GRP load PTE
        gpr_dest_index = self.getRandomGPR(exclude="0")
        self.genInstruction("LD##RISCV", {"LSTarget": target_addr, "rd" : gpr_dest_index})
        gpr_name = "x%d" % gpr_dest_index
        (gpr_val, valid) = self.readRegister(gpr_name)
        # Read PTE structure
        pte0_V = sel_pte_table['DescriptorDetails']["V"]
        pte0_WR = sel_pte_table['DescriptorDetails']["WR"]
        pte0_X = sel_pte_table['DescriptorDetails']["X"]
        pte0_U = sel_pte_table['DescriptorDetails']["G"]
        pte0_DA = sel_pte_table['DescriptorDetails']["DA"]
        pte0_RSW = sel_pte_table['DescriptorDetails']["RSW"]
        pte0_PPN = sel_pte_table['DescriptorDetails']["Address"]
        print("Leaf PTE structure >>>>>>>>>>>>>>>>>>>")
        print("Valid",sel_pte_table['DescriptorDetails']["V"])
        print("WR",sel_pte_table['DescriptorDetails']["WR"])
        print("X",sel_pte_table['DescriptorDetails']["X"])
        print("U",sel_pte_table['DescriptorDetails']["U"])
        print("G",sel_pte_table['DescriptorDetails']["G"])
        print("DA",sel_pte_table['DescriptorDetails']["DA"])
        print("RSW",sel_pte_table['DescriptorDetails']["RSW"])
        print("PPN",sel_pte_table['DescriptorDetails']["Address"])
        print("<<<<<<<<<<<<<<<<<<")
        old_read_val=gpr_val
        self.notice("Write leaf PTE now >>>>>>>>>>>>>>>>>>>")
        # Random modify leaf PTE rights, modify one bits has higher probability
        modify_pte_val = random_set_pte_rights(gpr_val)
        self.notice("Write leaf PTE should be: 0x%x" % modify_pte_val)

        # New PTE val write by a GPR, CAT this VAL to SrcREG first
        imm_bit15_0 =  modify_pte_val & 0xFFFF
        imm_bit31_16= (modify_pte_val & 0xFFFF0000) >> 16
        imm_bit47_32= (modify_pte_val & 0xFFFF00000000) >> 32
        imm_bit63_48= (modify_pte_val & 0xFFFF000000000000) >>48

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
        (temp_val,tmp_valid) = self.readRegister("x%d" %(w_gpr[0]))
        print(">>>>>>>>>>>>>>>>Debug write reg val: ",hex(temp_val))
        # Load Leaf PTE again to Check PTE should change successfully

        self.genInstruction("LD##RISCV", {"LSTarget": target_addr, "rd" : gpr_dest_index})
        print(">>>>>>>>>>>>>>>>PTE LSTarget: ",hex(target_addr),gpr_dest_index)
        print(">>>>>>>>>>>>>>>>Read old PTE val")
        print(hex(old_read_val))
        print(">>>>>>>>>>>>>>>>Write new PTE val")
        (gpr_val_new, valid) = self.readRegister(gpr_name)
        print(hex(gpr_val_new))

# >>>>>>>>>>>>>There is a PTE struct to Reference
# Page {'MemoryType': 'Default', 'MemoryAttr': '', 'Lower': 18446744064992661504, 'Upper': 18446744064992665599, 'PhysicalLower': 69951524864, 'PhysicalUpper': 69951528959, 'PhysPageId': 0, 'MemAttrIndex': 0, 'PageSize': 4096, 'Descriptor': 17487881539, 'DescriptorDetails': {'Accessed': '1', 'Address': '0x10496f9(0x4125be400)', 'DA': '0x1(0x40)', 'DataAccessPermission': 'ReadOnlyNoUser', 'G': '0x0(0x0)', 'InstrAccessPermission': 'NoExecute', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x1(0x100)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x1(0x2)', 'X': '0x0(0x0)'}}
# Table#2 {'Level': 2, 'DescriptorAddr': 70212415416, 'Descriptor': 18157303809, 'DescriptorDetails': {'Address': '0x10e909e(0x43a427800)', 'DA': '0x0(0x0)', 'G': '0x0(0x0)', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x0(0x0)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x0(0x0)', 'X': '0x0(0x0)'}}
# Table#1 {'Level': 1, 'DescriptorAddr': 72629218840, 'Descriptor': 18157302785, 'DescriptorDetails': {'Address': '0x10e909d(0x43a427400)', 'DA': '0x0(0x0)', 'G': '0x0(0x0)', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x0(0x0)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x0(0x0)', 'X': '0x0(0x0)'}}
# Table#0 {'Level': 0, 'DescriptorAddr': 72629213032, 'Descriptor': 17487881539, 'DescriptorDetails': {'Accessed': '1', 'Address': '0x10496f9(0x4125be400)', 'DA': '0x1(0x40)', 'DataAccessPermission': 'ReadOnlyNoUser', 'G': '0x0(0x0)', 'InstrAccessPermission': 'NoExecute', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x1(0x100)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x1(0x2)', 'X': '0x0(0x0)'}}
    def specific_modify_pte_rights(self, page_target_addr, locate_bits_to_change):
        # set pte function
        def random_set_pte_rights( reg_data, locate_bits_to_change):
            def set_bit(value, bit, bit_val):
                if bit_val:
                    return value | (1 << bit)
                else:
                    return value & ~(1 << bit)
            def modify_specific_bits(reg_data, num_bits_to_change, locate_bits_to_change):
                bits_to_change = set()
                bits_to_change.add(locate_bits_to_change)
                for bit in list(bits_to_change):
                    bit_val = RandomUtils.random32(0, 1)
                    reg_data = set_bit(reg_data, bit, bit_val)
                return reg_data
            # specific 1 bits to change. only change bit on locate_bits_to_change
            num_bits_to_change = 1 
            self.notice("Before modified reg_data: 0x%x" % reg_data)
            reg_data = modify_specific_bits(reg_data, num_bits_to_change, locate_bits_to_change)
            self.notice("After modified reg_data: 0x%x" % reg_data)
            return reg_data

        # Start from here
        # First get Page Info, fetch PTEs addr
        page_obj = self.getPageInfo(page_target_addr, "VA", 0)
        displayPageInfo(self, page_obj)
        get_page_info = page_obj.get('Page') # page descriptions
        get_table2_info = page_obj.get('Table#2') # level 2 pte descriptions
        get_table1_info = page_obj.get('Table#1') # level 1 pte descriptions
        get_table0_info = page_obj.get('Table#0') # leaf pte descriptions
        if get_table0_info is not None:
            target_addr = get_table0_info['DescriptorAddr']
        else:
            self.notice("NO PAGE here! Cant modify PTE.")
            return
        # Choice a GRP load PTE
        gpr_dest_index = self.getRandomGPR(exclude="0")
        self.genInstruction("LD##RISCV", {"LSTarget": target_addr, "rd" : gpr_dest_index})
        gpr_name = "x%d" % gpr_dest_index
        (gpr_val, valid) = self.readRegister(gpr_name)
        # Read PTE structure
        pte0_V = get_table0_info['DescriptorDetails']["V"]
        pte0_WR = get_table0_info['DescriptorDetails']["WR"]
        pte0_X = get_table0_info['DescriptorDetails']["X"]
        pte0_U = get_table0_info['DescriptorDetails']["G"]
        pte0_DA = get_table0_info['DescriptorDetails']["DA"]
        pte0_RSW = get_table0_info['DescriptorDetails']["RSW"]
        pte0_PPN = get_table0_info['DescriptorDetails']["Address"]
        print("Leaf PTE structure >>>>>>>>>>>>>>>>>>>")
        print("Valid",get_table0_info['DescriptorDetails']["V"])
        print("WR",get_table0_info['DescriptorDetails']["WR"])
        print("X",get_table0_info['DescriptorDetails']["X"])
        print("U",get_table0_info['DescriptorDetails']["U"])
        print("G",get_table0_info['DescriptorDetails']["G"])
        print("DA",get_table0_info['DescriptorDetails']["DA"])
        print("RSW",get_table0_info['DescriptorDetails']["RSW"])
        print("PPN",get_table0_info['DescriptorDetails']["Address"])
        print("<<<<<<<<<<<<<<<<<<")
        old_read_val=gpr_val
        self.notice("Write leaf PTE now >>>>>>>>>>>>>>>>>>>")
        # Random modify leaf PTE rights, modify one bits has higher probability
        modify_pte_val = random_set_pte_rights(gpr_val, locate_bits_to_change)
        self.notice("Write leaf PTE should be: 0x%x" % modify_pte_val)

        # New PTE val write by a GPR, CAT this VAL to SrcREG first
        imm_bit15_0 =  modify_pte_val & 0xFFFF
        imm_bit31_16= (modify_pte_val & 0xFFFF0000) >> 16
        imm_bit47_32= (modify_pte_val & 0xFFFF00000000) >> 32
        imm_bit63_48= (modify_pte_val & 0xFFFF000000000000) >>48

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
        (temp_val,tmp_valid) = self.readRegister("x%d" %(w_gpr[0]))
        print(">>>>>>>>>>>>>>>>Debug write reg val: ",hex(temp_val))
        # Load Leaf PTE again to Check PTE should change successfully

        self.genInstruction("LD##RISCV", {"LSTarget": target_addr, "rd" : gpr_dest_index})
        print(">>>>>>>>>>>>>>>>PTE LSTarget: ",hex(target_addr),gpr_dest_index)
        print(">>>>>>>>>>>>>>>>Read old PTE val")
        print(hex(old_read_val))
        print(">>>>>>>>>>>>>>>>Write new PTE val")
        (gpr_val_new, valid) = self.readRegister(gpr_name)
        print(hex(gpr_val_new))

# >>>>>>>>>>>>>There is a PTE struct to Reference
# Page {'MemoryType': 'Default', 'MemoryAttr': '', 'Lower': 18446744064992661504, 'Upper': 18446744064992665599, 'PhysicalLower': 69951524864, 'PhysicalUpper': 69951528959, 'PhysPageId': 0, 'MemAttrIndex': 0, 'PageSize': 4096, 'Descriptor': 17487881539, 'DescriptorDetails': {'Accessed': '1', 'Address': '0x10496f9(0x4125be400)', 'DA': '0x1(0x40)', 'DataAccessPermission': 'ReadOnlyNoUser', 'G': '0x0(0x0)', 'InstrAccessPermission': 'NoExecute', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x1(0x100)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x1(0x2)', 'X': '0x0(0x0)'}}
# Table#2 {'Level': 2, 'DescriptorAddr': 70212415416, 'Descriptor': 18157303809, 'DescriptorDetails': {'Address': '0x10e909e(0x43a427800)', 'DA': '0x0(0x0)', 'G': '0x0(0x0)', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x0(0x0)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x0(0x0)', 'X': '0x0(0x0)'}}
# Table#1 {'Level': 1, 'DescriptorAddr': 72629218840, 'Descriptor': 18157302785, 'DescriptorDetails': {'Address': '0x10e909d(0x43a427400)', 'DA': '0x0(0x0)', 'G': '0x0(0x0)', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x0(0x0)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x0(0x0)', 'X': '0x0(0x0)'}}
# Table#0 {'Level': 0, 'DescriptorAddr': 72629213032, 'Descriptor': 17487881539, 'DescriptorDetails': {'Accessed': '1', 'Address': '0x10496f9(0x4125be400)', 'DA': '0x1(0x40)', 'DataAccessPermission': 'ReadOnlyNoUser', 'G': '0x0(0x0)', 'InstrAccessPermission': 'NoExecute', 'PteType': 'P4K', 'RES0': '0x0(0x0)', 'RSW': '0x1(0x100)', 'SystemPage': '0x0(0x0)', 'U': '0x0(0x0)', 'V': '0x1(0x1)', 'WR': '0x1(0x2)', 'X': '0x0(0x0)'}}
    
    def random_modify_pte_pmp(self, page_target_addr, radical=False):
        # random set a bit
        def set_bit(value, bit, bit_val):
            if bit_val:
                return value | (1 << bit)
            else:
                return value & ~(1 << bit)
        def modify_random_bits(reg_data, num_bits_to_change):
            bits_to_change = set()
            while len(bits_to_change) < num_bits_to_change:
                sel_bit = RandomUtils.random32(0, 2)
                bits_to_change.add(sel_bit)
            for bit in list(bits_to_change):
                bit_val = RandomUtils.random32(0, 1)
                reg_data = set_bit(reg_data, bit, bit_val)
            return reg_data
        # get cur priv mode
        def getCurStatus(self, notice):
            if self.getPEstate("PrivilegeLevel") == 3:
                self.notice(f"---{notice} M-mode---")
            elif self.getPEstate("PrivilegeLevel") == 2:
                self.notice(f"---{notice} H-mode---")
            elif self.getPEstate("PrivilegeLevel") == 1:
                self.notice(f"---{notice} S-mode---")
            elif self.getPEstate("PrivilegeLevel") == 0:
                self.notice(f"---{notice} U-mode---")
        def insert_address_and_update_range(pmps, pte_addr):
            insert_positions = [pte_addr, pte_addr + 1024]
            for i in range(len(pmps) - 1):
                if pmps[i] <= pte_addr < pmps[i + 1]:
                    for insert_address in insert_positions:
                        if insert_address not in pmps[i:i + 2]:
                            pmps.insert(i + 1, insert_address)
                            i += 1
                            pmps.pop()
                    return pmps, [i-1, i]
            return pmps, None

        def insert_pmpcfg(pmpcfg0, pmpcfg2, idx, new_value):
            # new_value = 0xff
            combined = (pmpcfg2 << 64) | pmpcfg0
            # print("combined",hex(combined))
            bit_offset = idx * 8
            dup_cfg = (combined & ((idx+1)*8-1)) >> (idx*8)
            # print("dup_cfg",dup_cfg)
            lower_cfg = (combined & ((1<<(idx+1)*8)-1))
            # print("lower_cfg",hex(lower_cfg),((idx+1)*8-1))
            higher_cfg = combined  >> ((idx)*8)  << ((idx+2)*8)
            # print("higher_cfg",hex(higher_cfg))
            insert_cfg = new_value << ((idx+1)*8)
            # print("insert_cfg",hex(insert_cfg))
            new_value_inserted = (higher_cfg | insert_cfg | lower_cfg ) & ((1<<128)-1)
            # print("new_value_inserted",hex(new_value_inserted))
            new_pmpcfg2 = new_value_inserted >> 64
            new_pmpcfg0 = new_value_inserted & ((1 << 64) - 1)
            return new_pmpcfg0, new_pmpcfg2

        # Start from here
        # First get Page Info, fetch PTEs addr
        page_obj = self.getPageInfo(page_target_addr, "VA", 0)
        displayPageInfo(self, page_obj)
        get_page_info = page_obj.get('Page') # page descriptions
        get_table2_info = page_obj.get('Table#2') # level 2 pte descriptions
        get_table1_info = page_obj.get('Table#1') # level 1 pte descriptions
        get_table0_info = page_obj.get('Table#0') # leaf pte descriptions
        # choose a pte level
        if(get_table0_info is not None):
            tables = [get_table2_info, get_table1_info, get_table0_info]
            self.notice(">>>>>>>>>>> Query page level: is 3 level page, 4k page")
        elif(get_table1_info is not None):
            tables = [get_table2_info, get_table1_info]
            self.notice(">>>>>>>>>>> Query page level: is 2 level page, 2M page")
        elif(get_table2_info is not None):
            tables = [get_table2_info]
            self.notice(">>>>>>>>>>> Query page level: is 1 level page, 1G page")
        else:
            self.notice("NO PAGE here! Cant modify PTE.")
            return

        if(radical): # radcial means has probability to modify all level pte
            sel_pte_table = self.choice(tables) # but modify high level pte has more probability fail
        else:
            sel_pte_table = tables[-1]

        target_addr = sel_pte_table['DescriptorAddr']

        # Choice a GRP load PTE
        reserve_pte = []
        reserve_pte_addr = []
        load_pte_gpr_idx = self.getRandomGPR(exclude="0")
        load_pte_gpr_name = "x%d" % load_pte_gpr_idx
        for pte in tables:
            pte_addr = pte['DescriptorAddr']
            self.genInstruction("LD##RISCV", {"LSTarget": pte_addr, "rd" : load_pte_gpr_idx})
            (load_pte_val, valid) = self.readRegister(load_pte_gpr_name)
            reserve_pte.append(load_pte_val)
            reserve_pte_addr.append(pte_addr)
            self.notice(">>>>>>>> read pte val %x" % load_pte_val)

        # print(hex(reserve_pte_addr[0]), hex(reserve_pte_addr[1]), hex(reserve_pte_addr[2]))
        # print(hex(reserve_pte[0]), hex(reserve_pte[1]), hex(reserve_pte[2]))

        # Call to M mode, prepare to change PMP on PTE addr
        sys_call_params = {"PrivilegeLevel": 3}
        self.systemCall(sys_call_params)
        getCurStatus(self,"swtich system stat:")

        # Read activate PMPs
        pmp_read_idx = self.getRandomGPR(exclude="0")
        read_pmp_names = (
            "pmpaddr0",         # 0x3b0     
            "pmpaddr1",         # 0x3b1
            "pmpaddr2",         # 0x3b2
            "pmpaddr3",         # 0x3b3
            "pmpaddr4",         # 0x3b4
            "pmpaddr5",         # 0x3b5
            "pmpaddr6",         # 0x3b6
            "pmpaddr7",         # 0x3b7
            "pmpaddr8",         # 0x3b8
            "pmpaddr9",         # 0x3b9
            "pmpaddr10",        # 0x3ba
            "pmpaddr11",        # 0x3bb
            "pmpaddr12",        # 0x3bc
            "pmpaddr13",        # 0x3bd
            "pmpaddr14",        # 0x3be
            "pmpaddr15",        # 0x3bf
        )
        self.notice(">>>>>>>>>>>>>Read activate PMP:")
        pmp_reserve = []
        # assembly_helper = AssemblyHelperRISCV(self)
        for pmp in read_pmp_names: 
            # assembly_helper.genReadSystemRegister(pmp_read_idx, pmp)
            (pmp_val, valid) = self.readRegister(pmp)
            pmp_reserve.append(pmp_val)
            # print(pmp,"val:", hex(pmp_val))
            # print(pmp_reserve)
        pmp_min_addr = pmp_reserve[0]
        for i in range (0,(len(pmp_reserve)-1)):
            if pmp_reserve[i] != 0:
                pmp_max_addr = pmp_reserve[i]
                pmp_use_idx = i
            else:
                break
        self.notice("<<<<<<<<<<<<< PMP has used %d, addr from 0x%x to 0x %x" % (pmp_use_idx+1, pmp_min_addr, pmp_max_addr))

        # Determine which PMP protection range the PTE address which need to MODIFY is in
        tables = [get_table2_info, get_table1_info, get_table0_info]
        sel_pte_table = self.choice(tables)
        self.notice("Prepare to modify PMP where pte %d located" % sel_pte_table['Level'])
        sel_pte_addr = sel_pte_table['DescriptorAddr']
        self.notice("PTE addr is : 0x%x ,and need to cut lower 2 bits: 0x%x" % (sel_pte_addr, sel_pte_addr>>2))
        self.notice(">>>>>>>> compare pmps >>>>>>>> old pmps")
        for i in range (0,(len(pmp_reserve))):
            self.notice("%s : 0x%x" % (read_pmp_names[i], pmp_reserve[i]))

        # insert modify pte located addr, set it only 4B, only make it AF!
        (update_pmps, idx_range) = insert_address_and_update_range(pmp_reserve, (sel_pte_addr>>2))
        if idx_range is None:
            self.notice("PTE ADDR NOT MATCH! Passed")

            # Call back to S mode, prepare to test PMP on PTE addr
            sys_call_params = {"PrivilegeLevel": 1}
            self.systemCall(sys_call_params)
            getCurStatus(self,"swtich system stat:")
            return
            # self.error("PTE ADDR NOT MATCH!")
        else:
            self.notice(">>>>>>>> compare pmps >>>>>>>> new pmps")
            self.notice("insert pmps in pmpaddr%d to pmpaddr%d" % (idx_range[0], idx_range[1]))
            for i in range (0,(len(pmp_reserve))):
                self.notice("%s : 0x%x" % (read_pmp_names[i], update_pmps[i]))
        # need to modify PMPCFG which correspond to PMPADDR!
        read_pmpcfg_names = ("pmpcfg0", "pmpcfg2")
        pmpcfg_reserve = []
        for pmpcfg in read_pmpcfg_names: 
            (pmpcfg_val, valid) = self.readRegister(pmpcfg)
            pmpcfg_reserve.append(pmpcfg_val)
        self.notice(">>>>>>>> compare pmpcfg >>>>>>>> old cfg")
        self.notice("%s : 0x%x" % (read_pmpcfg_names[0], pmpcfg_reserve[0]))
        self.notice("%s : 0x%x" % (read_pmpcfg_names[1], pmpcfg_reserve[1]))

        # random set PMPCFG: R W X, if need set A, modify function: modify_random_bits()
        num_bits_to_change = RandomUtils.random32(1, 3)
        random_insert_cfg = 0xE #modify_random_bits(0, num_bits_to_change)
        self.notice("set new config is: 0x%x" % random_insert_cfg)
        new_pmpcfg0, new_pmpcfg2 = insert_pmpcfg(pmpcfg_reserve[0], pmpcfg_reserve[1], idx_range[0], random_insert_cfg)
        self.notice(">>>>>>>> compare pmpcfg >>>>>>>> new cfg")
        self.notice("%s : 0x%x" % (read_pmpcfg_names[0], new_pmpcfg0))
        self.notice("%s : 0x%x" % (read_pmpcfg_names[1], new_pmpcfg2))

        # write all new PMPs & PMPCFGs
        xsComdef = xsCommonDef(self.genThread)
        for i in range (0,(len(pmp_reserve))):
            xsCommonDef.wrCSR(self,read_pmp_names[i], update_pmps[i])

        xsCommonDef.wrCSR(self,"pmpcfg0", new_pmpcfg0)
        xsCommonDef.wrCSR(self,"pmpcfg2", new_pmpcfg2)

        # Call back to S mode, prepare to test PMP on PTE addr
        sys_call_params = {"PrivilegeLevel": 1}
        self.systemCall(sys_call_params)
        getCurStatus(self,"swtich system stat:")

        # print(hex(reserve_pte_addr[0]), hex(reserve_pte_addr[1]), hex(reserve_pte_addr[2]))
        # print(hex(reserve_pte[0]), hex(reserve_pte[1]), hex(reserve_pte[2]))

        pte_gpr = self.getRandomRegisters(4, "GPR", "0")   
  
        for i in range(len(reserve_pte_addr)):
            pte_addr = reserve_pte_addr[i]
            reserve_pte_val = reserve_pte[i]
            # New PTE val write by a GPR, CAT this VAL to SrcREG first
            imm_bit15_0 =  reserve_pte_val & 0xFFFF
            imm_bit31_16= (reserve_pte_val & 0xFFFF0000) >> 16
            imm_bit47_32= (reserve_pte_val & 0xFFFF00000000) >> 32
            imm_bit63_48= (reserve_pte_val & 0xFFFF000000000000) >>48

            self.genInstruction("LUI##RISCV", {"rd": pte_gpr[0],"simm20": imm_bit15_0}) 
            self.genInstruction("LUI##RISCV", {"rd": pte_gpr[1],"simm20": imm_bit31_16})
            self.genInstruction("LUI##RISCV", {"rd": pte_gpr[2],"simm20": imm_bit47_32})
            self.genInstruction("LUI##RISCV", {"rd": pte_gpr[3],"simm20": imm_bit63_48})

            self.genInstruction("SLLI#RV64I#RISCV",{"rd": pte_gpr[3],"rs1": pte_gpr[3],"shamt": 36,},)
            self.genInstruction("SLLI#RV64I#RISCV",{"rd": pte_gpr[2],"rs1": pte_gpr[2],"shamt": 20,},)
            self.genInstruction("SLLI#RV64I#RISCV",{"rd": pte_gpr[1],"rs1": pte_gpr[1],"shamt": 4,},)
            self.genInstruction("SRLI#RV64I#RISCV",{"rd": pte_gpr[0],"rs1": pte_gpr[0],"shamt": 12,},)

            self.genInstruction("ADD##RISCV", {"rd":pte_gpr[0] ,"rs1": pte_gpr[0],"rs2": pte_gpr[1]},)
            self.genInstruction("ADD##RISCV", {"rd":pte_gpr[0] ,"rs1": pte_gpr[0],"rs2": pte_gpr[2]},)
            self.genInstruction("ADD##RISCV", {"rd":pte_gpr[0] ,"rs1": pte_gpr[0],"rs2": pte_gpr[3]},)

            self.genInstruction("SD##RISCV", {"LSTarget": pte_addr, "rs2" : pte_gpr[0]})

