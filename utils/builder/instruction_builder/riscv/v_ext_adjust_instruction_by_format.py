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
import re

from shared.instruction import add_addressing_operand

from vector_operand_adjustor import VectorOperandAdjustor

format_map = {}


def v_ext_adjust_instruction_by_format(aInstruction):
    success = False

    instruction_format = aInstruction.get_format()

    set_register_layouts(aInstruction)

    adjust_register_layouts(aInstruction)

    if instruction_format == "vd/rd-vs2-vs1-vm":
        success = adjust_vdrd_vs2_vs1_vm(aInstruction)
    elif instruction_format == "vd-vs2-vs1-vm":
        success = adjust_vd_vs2_vs1_vm(aInstruction)
    elif instruction_format == "vd-vs2-simm5-vm":
        success = adjust_vd_vs2_simm5_vm(aInstruction)
    elif instruction_format == "vd-vs2-rs1-vm":
        success = adjust_vd_vs2_rs1_vm(aInstruction)
    elif instruction_format == "vd/rd-vs2-rs1-vm":
        success = adjust_vdrd_vs2_rs1_vm(aInstruction)
    # unary instruction formats
    elif instruction_format == "vd/rd-vs2-vm":
        success = adjust_vdrd_vs2_vm(aInstruction)
    elif instruction_format == "vd-vs2-vm":
        success = adjust_vd_vs2_vm(aInstruction)
    elif instruction_format == "vd/rd-vs2":
        success = adjust_vdrd_vs2(aInstruction)
    elif instruction_format == "rd-vs2-vm":
        success = adjust_rd_vs2_vm(aInstruction)
    elif instruction_format == "rd-vs2":
        success = adjust_rd_vs2(aInstruction)
    elif instruction_format == "vd-rs1-vm":
        success = adjust_vd_rs1_vm(aInstruction)
    elif instruction_format == "vd/rd-rs1-vm":
        success = adjust_vdrd_rs1_vm(aInstruction)
    elif instruction_format == "vd-vm":
        success = adjust_vd_vm(aInstruction)
    # vset{i}vl{i} instructions
    elif instruction_format == "rd-rs1-rs2":
        success = adjust_rd_rs1_rs2(aInstruction)
    elif instruction_format == "rd-uimm[4:0]-zimm[9:0]":
        success = adjust_rd_uimm_4_0_zimm_9_0(aInstruction)
    elif instruction_format == "rd-rs1-zimm[10:0]":
        success = adjust_rd_rs1_zimm_10_0(aInstruction)
    # vmerge and vmv instructions
    elif instruction_format == "vd-vs2-simm5":
        success = adjust_vd_vs2_simm5(aInstruction)
    elif instruction_format == "vd$\\neq$0-vs2-simm5":
        success = adjust_vd_nonzero_vs2_simm5(aInstruction)
    elif instruction_format == "vd-vs2-vs1":
        success = adjust_vd_vs2_vs1(aInstruction)
    elif instruction_format == "vd$\\neq$0-vs2-vs1":
        success = adjust_vd_nonzero_vs2_vs1(aInstruction)
    elif instruction_format == "vd-vs2-rs1":
        success = adjust_vd_vs2_rs1(aInstruction)
    elif instruction_format == "vd$\\neq$0-vs2-rs1":
        success = adjust_vd_nonzero_vs2_rs1(aInstruction)
    elif instruction_format == "vd-simm5":
        success = adjust_vd_simm5(aInstruction)
    elif instruction_format == "vd-vs1":
        success = adjust_vd_vs1(aInstruction)
    elif instruction_format == "vd-vs2":
        success = adjust_vd_vs2(aInstruction)
    # vl<nf>r/vs<nf>r instructions
    elif instruction_format == "vd-rs1":
        success = adjust_vd_rs1(aInstruction)
    elif instruction_format == "vd-rs1-vs2-vm":
        success = adjust_vd_rs1_vs2_vm(aInstruction)
    elif instruction_format == "vd-rs1-rs2-vm":
        success = adjust_vd_rs1_rs2_vm(aInstruction)
    elif instruction_format == "vs3-rs1":
        success = adjust_vs3_rs1(aInstruction)
    elif instruction_format == "vs3-rs1-vm":
        success = adjust_vs3_rs1_vm(aInstruction)
    elif instruction_format == "vs3-rs1-vs2-vm":
        success = adjust_vs3_rs1_vs2_vm(aInstruction)
    elif instruction_format == "vs3-rs1-rs2-vm":
        success = adjust_vs3_rs1_rs2_vm(aInstruction)
    # vamo instructions
    elif instruction_format == "rs1-vs2-vs3-vm":
        success = adjust_rs1_vs2_vs3_vm(aInstruction)
    elif instruction_format == "rs1-vs2-vd-vm":
        success = adjust_rs1_vs2_vd_vm(aInstruction)
    # Zvbb instructions
    elif instruction_format == "vd-vs2-uimm[4:0]-i5-vm":
        success = adjust_vd_vs2_uimm6_vm(aInstruction)
    elif instruction_format == "vd-vs2-uimm[4:0]-vm":
        success = adjust_vd_vs2_uimm5_vm(aInstruction)
    else:
        record_instruction_format(instruction_format)

    return success


def record_instruction_format(aInstructionFormat):
    if aInstructionFormat in format_map:
        format_map[aInstructionFormat] += 1
    else:
        format_map[aInstructionFormat] = 1


def set_register_layouts(aInstruction):
    if _is_load_store(aInstruction):
        if _is_whole_register_load_store(aInstruction.name):
            _set_whole_register_load_store_register_layouts(aInstruction)
        elif _is_mask_load_store(aInstruction.name):
            _set_mask_load_store_register_layouts(aInstruction)
        elif _is_indexed_load_store(aInstruction):
            _set_indexed_load_store_register_layouts(aInstruction)
        else:
            _set_load_store_register_layouts(aInstruction)
    elif _is_whole_register_move(aInstruction.name):
        _set_whole_register_move_register_layouts(aInstruction)
    else:
        _set_arithmetic_register_layouts(aInstruction)


# Account for non-standard register layouts due to wide and narrow operands
def adjust_register_layouts(aInstruction):
    adjust_dest = False
    dest_layout_multiple = 2
    if aInstruction.name.startswith("VW") or aInstruction.name.startswith("VFW"):
        adjust_dest = True
    elif aInstruction.name.startswith("VQMACC"):
        adjust_dest = True
        dest_layout_multiple = 4

    adjust_source = False
    source_layout_multiple = 2
    if ".W" in aInstruction.name:
        adjust_source = True
    elif aInstruction.name.startswith("VSEXT.VF") or aInstruction.name.startswith("VZEXT.VF"):
        adjust_source = True
        layout_divisor = int(aInstruction.name[-1])
        source_layout_multiple = 1 / layout_divisor

    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if adjust_dest:
        operand_adjustor.adjust_dest_layout(dest_layout_multiple)
        operand_adjustor.set_vs1_differ_vd()

    if adjust_source:
        operand_adjustor.adjust_source_layout(source_layout_multiple)

    if adjust_dest != adjust_source:
        operand_adjustor.set_vs2_differ_vd()


def get_element_size(aConstBitsOpr):
    elem_size = 0

    width = aConstBitsOpr.value[-10:-7]
    mew = aConstBitsOpr.value[3]
    if mew == "0":
        if width == "000":
            elem_size = 1
        elif width == "101":
            elem_size = 2
        elif width == "110":
            elem_size = 4
        elif width == "111":
            elem_size = 8
    elif mew == "1":
        if width == "000":
            elem_size = 16
        elif width == "101":
            elem_size = 32
        elif width == "110":
            elem_size = 64
        elif width == "111":
            elem_size = 128

    return elem_size


def adjust_vd_rs1(aInstruction):
    if aInstruction.iclass == "LoadStoreInstruction":
        operand_adjustor = VectorOperandAdjustor(aInstruction)
        operand_adjustor.set_vd()
        operand_adjustor.set_rs1_int_ls_base()

        width = get_element_size(aInstruction.find_operand("const_bits"))
        attr_dict = dict()
        subop_dict = dict()
        subop_dict["base"] = "rs1"
        attr_dict["alignment"] = width
        attr_dict["base"] = "rs1"
        attr_dict["element-size"] = width
        attr_dict["mem-access"] = "Read"

        add_addressing_operand(
            aInstruction,
            None,
            "LoadStore",
            "VectorBaseOffsetLoadStoreOperandRISCV",
            subop_dict,
            attr_dict,
        )
    else:
        operand_adjustor = VectorOperandAdjustor(aInstruction)
        operand_adjustor.set_vd()
        if ".F" in aInstruction.name:
            operand_adjustor.set_rs1_sp()
        else:
            operand_adjustor.set_rs1_int()

    return True


def adjust_vs3_rs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vs3()
    operand_adjustor.set_rs1_int_ls_base()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    attr_dict["alignment"] = width
    attr_dict["base"] = "rs1"
    attr_dict["element-size"] = width
    attr_dict["mem-access"] = "Write"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorBaseOffsetLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    return True


def adjust_vs3_rs1_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vs3()
    operand_adjustor.set_rs1_int_ls_base()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    attr_dict["alignment"] = width
    attr_dict["base"] = "rs1"
    attr_dict["element-size"] = width
    attr_dict["mem-access"] = "Write"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorBaseOffsetLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vm()
    return True


def adjust_vs3_rs1_vs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vs3()
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs2_differ_vs3()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "vs2"
    attr_dict["base"] = "rs1"
    attr_dict["mem-access"] = "Write"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorIndexedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vm()
    return True


def adjust_vs3_rs1_rs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    reg_count = 1
    if "SEG" in aInstruction.name:
        src_opr = aInstruction.find_operand("vs3")
        reg_count = int(src_opr.regCount)

    operand_adjustor.set_vs3()
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_rs2_int_ls_base()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "rs2"
    attr_dict["alignment"] = width
    attr_dict["base"] = "rs1"
    attr_dict["data-size"] = width * reg_count
    attr_dict["element-size"] = width
    attr_dict["mem-access"] = "Write"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorStridedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vm()
    return True


def adjust_rs1_vs2_vs3_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs2_differ_vs3()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "vs2"
    attr_dict["base"] = "rs1"
    attr_dict["mem-access"] = "ReadWrite"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorIndexedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vs3()
    operand_adjustor.set_vm()
    return True


def adjust_rd_rs1_rs2(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rd_int()
    operand_adjustor.set_rs1_vsetvl()
    operand_adjustor.set_rs2_vsetvl()
    return True


def adjust_rd_uimm_4_0_zimm_9_0(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rd_int()
    operand_adjustor.set_imm_avl_vsetvl()
    operand_adjustor.set_imm_vtype_vsetvl("zimm[9:0]", 10)
    return True


def adjust_rd_rs1_zimm_10_0(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rd_int()
    operand_adjustor.set_rs1_vsetvl()
    operand_adjustor.set_imm_vtype_vsetvl("zimm[10:0]", 11)
    return True


def adjust_vdrd_rs1_vm(aInstruction):
    funct3 = aInstruction.find_operand("const_bits").value[11:14]
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if funct3 == "101":  # OPFVF
        operand_adjustor.set_vdrd_sp()
        operand_adjustor.set_rs1_sp()
    else:
        operand_adjustor.set_vdrd_int()
        operand_adjustor.set_rs1_int()
    operand_adjustor.set_vm()
    return True


def adjust_vd_rs1_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if aInstruction.iclass == "LoadStoreInstruction":
        operand_adjustor.set_vd()
        operand_adjustor.set_rs1_int_ls_base()

        width = get_element_size(aInstruction.find_operand("const_bits"))
        attr_dict = dict()
        subop_dict = dict()
        subop_dict["base"] = "rs1"
        attr_dict["alignment"] = width
        attr_dict["base"] = "rs1"
        attr_dict["element-size"] = width
        attr_dict["mem-access"] = "Read"

        add_addressing_operand(
            aInstruction,
            None,
            "LoadStore",
            "VectorBaseOffsetLoadStoreOperandRISCV",
            subop_dict,
            attr_dict,
        )
    else:
        funct3 = aInstruction.find_operand("const_bits").value[11:14]
        operand_adjustor.set_vd()
        if funct3 == "101":  # OPFVF
            operand_adjustor.set_rs1_sp()
        else:
            operand_adjustor.set_rs1_int()
    operand_adjustor.set_vm()
    return True


def adjust_vd_rs1_vs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs2_differ_vd()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "vs2"
    attr_dict["base"] = "rs1"
    attr_dict["mem-access"] = "Read"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorIndexedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vm()
    return True


def adjust_vd_rs1_rs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    reg_count = 1
    if "SEG" in aInstruction.name:
        dest_opr = aInstruction.find_operand("vd")
        reg_count = int(dest_opr.regCount)

    operand_adjustor.set_vd()
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_rs2_int_ls_base()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "rs2"
    attr_dict["alignment"] = width
    attr_dict["base"] = "rs1"
    attr_dict["data-size"] = width * reg_count
    attr_dict["element-size"] = width
    attr_dict["mem-access"] = "Read"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorStridedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vm()
    return True


def adjust_rs1_vs2_vd_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rs1_int_ls_base()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs2_differ_vd()

    width = get_element_size(aInstruction.find_operand("const_bits"))
    attr_dict = dict()
    subop_dict = dict()
    subop_dict["base"] = "rs1"
    subop_dict["index"] = "vs2"
    attr_dict["base"] = "rs1"
    attr_dict["mem-access"] = "ReadWrite"

    add_addressing_operand(
        aInstruction,
        None,
        "LoadStore",
        "VectorIndexedLoadStoreOperandRISCV",
        subop_dict,
        attr_dict,
    )

    operand_adjustor.set_vd()
    operand_adjustor.set_vm()
    return True


def adjust_vdrd_vs2_vm(aInstruction):
    funct3 = aInstruction.find_operand("const_bits").value[11:14]
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if funct3 == "001":  # OPFVV
        operand_adjustor.set_vdrd_sp()
    else:
        operand_adjustor.set_vdrd_int()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vm()
    return True


def adjust_vd_vs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vm()

    if aInstruction.name in ("VMSBF.M", "VMSIF.M", "VMSOF.M", "VIOTA.M"):
        operand_adjustor.set_vs2_differ_vd()

    return True


def adjust_vdrd_vs2(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if ".F" in aInstruction.name:
        operand_adjustor.set_vdrd_sp()
    else:
        operand_adjustor.set_vdrd_int()
    operand_adjustor.set_vs2()
    return True


def adjust_vd_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vm()
    return True


def adjust_rd_vs2_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rd_int()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vm()
    return True


def adjust_rd_vs2(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_rd_int()
    operand_adjustor.set_vs2()
    return True


def adjust_vdrd_vs2_vs1_vm(aInstruction):
    funct3 = aInstruction.find_operand("const_bits").value[6:9]
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    if funct3 == "001":  # OPFVV
        operand_adjustor.set_vdrd_sp()
    else:
        operand_adjustor.set_vdrd_int()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs1()
    operand_adjustor.set_vm()
    return True


def adjust_vd_vs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs1()
    return True


def adjust_vd_vs2(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    return True


def adjust_vd_vs2_vs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs1()

    if aInstruction.name == "VCOMPRESS.VM":
        operand_adjustor.set_vs2_differ_vd()
        operand_adjustor.set_vs1_differ_vd()

    return True


def adjust_vd_nonzero_vs2_vs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd_nonzero()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs1()
    return True


def adjust_vd_vs2_vs1_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_vs1()
    operand_adjustor.set_vm()

    if aInstruction.name == "VRGATHER.VV":
        operand_adjustor.set_vs2_differ_vd()
        operand_adjustor.set_vs1_differ_vd()

    return True


def adjust_vd_simm5(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_imm("simm5", "simm5", True)
    return True


def adjust_vd_vs2_simm5(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_imm("simm5", "simm5", True)
    return True


def adjust_vd_nonzero_vs2_simm5(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd_nonzero()
    operand_adjustor.set_vs2()
    operand_adjustor.set_imm("simm5", "simm5", True)
    return True


def adjust_vd_vs2_simm5_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_imm("simm5", "simm5", True)
    operand_adjustor.set_vm()

    if aInstruction.name in ("VRGATHER.VI", "VSLIDEUP.VI"):
        operand_adjustor.set_vs2_differ_vd()

    return True


def adjust_vd_vs2_rs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_rs1_int()
    return True


def adjust_vd_nonzero_vs2_rs1(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd_nonzero()
    operand_adjustor.set_vs2()
    operand_adjustor.set_rs1_int()
    return True


def adjust_vd_vs2_rs1_vm(aInstruction):
    funct3 = aInstruction.find_operand("const_bits").value[6:9]
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    if funct3 == "101":  # OPFVF
        operand_adjustor.set_rs1_sp()
    else:
        operand_adjustor.set_rs1_int()

    operand_adjustor.set_vm()

    if aInstruction.name in (
        "VFSLIDE1UP.VF",
        "VRGATHER.VX",
        "VSLIDE1UP.VX",
        "VSLIDEUP.VX",
    ):
        operand_adjustor.set_vs2_differ_vd()

    return True


def adjust_vdrd_vs2_rs1_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vdrd_int()
    operand_adjustor.set_vs2()
    operand_adjustor.set_rs1_int()
    operand_adjustor.set_vm()
    return True

def adjust_vd_vs2_uimm6_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_imm("uimm[4:0]","uimm5",False)
    operand_adjustor.set_imm("i5","uimm1",False)
    operand_adjustor.set_vm()
    return True

def adjust_vd_vs2_uimm5_vm(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    operand_adjustor.set_vd()
    operand_adjustor.set_vs2()
    operand_adjustor.set_imm("uimm[4:0]","uimm5",False)    
    operand_adjustor.set_vm()
    return True    


def _is_load_store(aInstruction):
    if aInstruction.iclass in ("LoadStoreInstruction", "VectorAMOInstructionRISCV"):
        return True

    return False


def _is_whole_register_load_store(aInstructionName):
    if re.fullmatch(r"V(L|S)\dR(E\d{1,2})?\.V", aInstructionName):
        return True

    return False


def _is_mask_load_store(aInstructionName):
    if aInstructionName in ("VLM.V", "VSM.V"):
        return True

    return False


def _is_indexed_load_store(aInstruction):
    if (aInstruction.name[:4] in ("VLOX", "VLUX", "VSOX", "VSUX")) or (
        aInstruction.iclass == "VectorAMOInstructionRISCV"
    ):
        return True

    return False


def _is_whole_register_move(aInstructionName):
    if aInstructionName in ("VMV1R.V", "VMV2R.V", "VMV4R.V", "VMV8R.V"):
        return True

    return False


def _set_whole_register_load_store_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    reg_count = int(aInstruction.name[2])

    elem_width = 8
    if aInstruction.name[4] == "E":
        width_end_index = aInstruction.name.find(".")
        elem_width = int(aInstruction.name[5:width_end_index])

    src_dest_opr = _get_source_or_destination_operand(aInstruction)
    operand_adjustor.set_whole_register_layout(
        src_dest_opr, aRegCount=reg_count, aElemWidth=elem_width
    )


def _set_mask_load_store_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    src_dest_opr = _get_source_or_destination_operand(aInstruction)
    operand_adjustor.set_whole_register_layout(src_dest_opr, aRegCount=1)


def _set_indexed_load_store_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    (reg_count, elem_width) = _get_load_store_register_layout_parameters(aInstruction)

    src_dest_opr = _get_source_or_destination_operand(aInstruction)
    operand_adjustor.set_vtype_layout(aInstruction, src_dest_opr, aRegCount=reg_count)
    index_opr = aInstruction.find_operand("vs2")
    operand_adjustor.set_fixed_element_size_layout(index_opr, aRegCount=1, aElemWidth=elem_width)


def _set_load_store_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    (reg_count, elem_width) = _get_load_store_register_layout_parameters(aInstruction)

    src_dest_opr = _get_source_or_destination_operand(aInstruction)
    operand_adjustor.set_fixed_element_size_layout(
        src_dest_opr, aRegCount=reg_count, aElemWidth=elem_width
    )


def _set_whole_register_move_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)

    reg_count = int(aInstruction.name[3])

    dest_opr = aInstruction.find_operand("vd")
    operand_adjustor.set_whole_register_layout(dest_opr, aRegCount=reg_count)
    src_opr = aInstruction.find_operand("vs2")
    operand_adjustor.set_whole_register_layout(src_opr, aRegCount=reg_count)


def _set_arithmetic_register_layouts(aInstruction):
    operand_adjustor = VectorOperandAdjustor(aInstruction)
    for opr_name in ("vd", "vs1", "vs2", "vd/rd", "vd$\neq$0"):
        opr = aInstruction.find_operand(opr_name, fail_not_found=False)

        if opr:
            operand_adjustor.set_vtype_layout(aInstruction, opr)


def _get_source_or_destination_operand(aInstruction):
    src_dest_opr = aInstruction.find_operand("vd", fail_not_found=False)
    if not src_dest_opr:
        src_dest_opr = aInstruction.find_operand("vs3")

    return src_dest_opr


def _get_load_store_register_layout_parameters(aInstruction):
    reg_count = 1
    elem_width = None

    matches = re.findall("\d+", aInstruction.name)
    if len(matches) > 1:
        reg_count = matches[0]
        elem_width = matches[1]
    else:
        elem_width = matches[0]

    return (reg_count, elem_width)
