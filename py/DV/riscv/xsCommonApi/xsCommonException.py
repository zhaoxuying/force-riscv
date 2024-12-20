from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV
from base.Sequence import Sequence
from DV.riscv.trees.instruction_tree import *
from base.InstructionMap import InstructionMap

from DV.riscv.xsCommonApi.PageFaultSequence import PageFaultSequence
from base.ChoicesModifier import ChoicesModifier
from riscv.ModifierUtils import *
from EnumsRISCV import EPagingMode
import VirtualMemory

# af = new xsCommonAF.AFSequence()
# af.generate()
# GenThreadInitialization = xsCommonAF.gen_thread_initialization()

# Utility func to merge dic
def merge(*args):
    result = {}
    for dict1 in args:
        result.update(dict1)
    return result


# LD_Int_instructions LD_Float_instructions LD_C_instructions
class AFSequence(Sequence):
    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self._mExceptionCodes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15)
        self._iter_count = 20
        self._exception_counts = dict.fromkeys(self._mExceptionCodes, 0)
        self.instruction_count = 400
        self._mInstrList = []

        (self._iter_count_tmp, valid) = self.getOption("IterCount")
        if valid:
            self._iter_count = self._iter_count_tmp

        self.load_basic_instructions = merge(LD_Int_instructions, LD_Float_instructions, LD_C_instructions)
        for _ in range(self.instruction_count):
            self._mInstrList.append(self.pickWeighted(self.load_basic_instructions))
        

    def _tc_load_basic(self, instruction_count=50):
        load_basic_instructions = merge(LD_Int_instructions, LD_Float_instructions, LD_C_instructions)
        for _ in range(instruction_count):
            the_instruction = self.pickWeighted(load_basic_instructions)
            gen_mod = self.random32(0, 1)

            if gen_mod == 0:
                num = self.random32(1,10)
                for _ in range(num):
                    self.genInstruction(the_instruction)
            else:
                num = self.random32(1,10)
                for _ in range(num):
                    self.genInstruction(the_instruction)
                    the_instruction = self.pickWeighted(load_basic_instructions)

    def _tc_laod_access_fault(self):
        for _ in range(self._iter_count):
            target_addr = self.genVA(Type="D", Align=8, Range="0x40000000-0x79000000")
            self.notice('---target_addr: {:016x}'.format(target_addr))
            instr_id = self.genInstruction(self.choice(self._mInstrList), {"LSTarget": target_addr})
            instr_obj = self.queryInstructionRecord(instr_id)
            # Write exception count info into the gen.log
            self._displayExceptionInfo(instr_obj)

    def _displayExceptionInfo(self, instr_obj):
        # Report the exception generated
        for ec in self._mExceptionCodes:
            backend_exception_count = self.queryExceptionRecordsCount(ec)
            new_exception = backend_exception_count > self._exception_counts[ec]
            self._exception_counts[ec] = backend_exception_count
            self.notice(
                ">>>>>>>  Exception:  {}    Query value:  {}".format(
                    ec, self.queryExceptionRecordsCount(ec)
                )
            )
            self.notice(
                ">>>>>>>  Instr:  {}    EType:  {}    New Exception? {}   count {}".format(
                    instr_obj["Name"], ec, new_exception, backend_exception_count
                )
            )

    def _add_instrs(self, instrs: list()):
        self._mInstrList = instrs

    def generate(self, **kargs):
        self.genInstruction("MRET##RISCV", {"NoSkip" : 1, "priv" : 1})
        self.notice('---privilege level = {}'.format({self.getPEstate("PrivilegeLevel")}))
        self._tc_laod_access_fault()

# modify _mInstrList, witch is in func "__init__", to add your own instruction
class PFSequence(PageFaultSequence):
    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self._mInstrList = []
        self.instruction_count = 400
        self.hasLoad=True
        self.hasStore=True
        self.load_basic_instructions = merge(LD_Int_instructions, LD_Float_instructions, LD_C_instructions)
        self.store_basic_instructions = merge(ST_Int_instructions, ST_Float_instructions, ST_C_instructions)
        self.ldst_basic_instructions = merge(self.load_basic_instructions, self.store_basic_instructions)

        for _ in range(self.instruction_count):
            if self.hasLoad and self.hasStore:
                self._mInstrList.append(self.pickWeighted(self.ldst_basic_instructions))
            elif self.hasLoad:
                self._mInstrList.append(self.pickWeighted(self.load_basic_instructions))
            elif self.hasStore:
                self._mInstrList.append(self.pickWeighted(self.store_basic_instructions))

        self._mInstrList = tuple(self._mInstrList)
        self._mExceptionCodes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15)
        self._requested_fault_type = None
        self._page_fault_level = None
        self._iter_count = 5
        self._exception_counts = dict.fromkeys(self._mExceptionCodes, 0)

    def _add_instrs(self, instrs: list()):
        self._mInstrList = instrs

    def generate(self, **kwargs):
        self._processFctrlOptions()
        # Generate some no-ops before making changes to the paging choices
        self._genDummyInstructions()
        # Modify the paging choices based on the options parsed from the fctrl file
        page_fault_mod = PageFaultModifier(self.genThread, self.getGlobalState("AppRegisterWidth"))
        self.notice('---{}'.format(page_fault_mod.getValidFaultTypes()))

        if not self._requested_fault_type in page_fault_mod.getValidFaultTypes():
            self.error("'PageFaultType' of {} is an unsupported type.").format(
                self._requested_fault_type
            )
        else:
            if self._page_fault_level == None:
                page_fault_mod.apply(**{"Type": self._requested_fault_type})
            else:
                page_fault_mod.apply(
                    **{"Type": self._requested_fault_type, "Level": [self._page_fault_level]}
                )
        self.notice('---instrlist : {}'.format(self._mInstrList))
        # Generate the faulting instructions
        for _ in range(self._iter_count):
            instr_id = self.genInstruction(self.choice(self._mInstrList))
            instr_obj = self.queryInstructionRecord(instr_id)

            # Write exception count info into the gen.log
            self._displayExceptionInfo(instr_obj)

            # Write the page translation info into the gen.log
            ls_target_addr = instr_obj["LSTarget"]
            page_obj = self.getPageInfo(ls_target_addr, "VA", 0)
            self.notice('--- page info : '.format(page_obj))
            displayPageInfo(self, page_obj)

        # Restore the paging choices to values before the page_fault_mod.apply
        page_fault_mod.revert()

        # Some no-ops after the paging choices were restored
        self._genDummyInstructions()

    def _genDummyInstructions(self):
        for _ in range(5):
            self.genInstruction("ORI##RISCV", {"rd": 0, "rs1": 0, "simm12": 0})

    def _processFctrlOptions(self):

        # Process options from the fctrl file:
        # - PagingDisabled   = [0, 1]
        # - IterCount        = integer
        # - PageFaultType    = ["Invalid_DA", "Invalid_U", "Invalid_X", "Invalid_WR", "Invalid_V"]
        # - PageFaultLevel   = [0, 1] for sv32; [0, 1, 2] for sv39; [0, 1, 2, 3] for sv48.

        # Check to make sure paging is not disabled in the options
        (paging_disabled, valid) = self.getOption("PagingDisabled")
        if valid and (paging_disabled == 1):
            self.error("'PagingDisabled' option set, can't generate page faults.")
        paging_disabled = 0

        # Check to see if a specific page fault type is requested in the options.
        (self._requested_fault_type, valid) = self.getOption("PageFaultType")
        if not valid:
            self.error("Option 'PageFaultType' was not specified.")
        # Temporary - I'm not sure how to code the option to allow a space in the option string.
        if self._requested_fault_type == "Invalid_DA":
            self._requested_fault_type = "Invalid DA"
        if self._requested_fault_type == "Invalid_U":
            self._requested_fault_type = "Invalid U"
        if self._requested_fault_type == "Invalid_X":
            self._requested_fault_type = "Invalid X"
        if self._requested_fault_type == "Invalid_WR":
            self._requested_fault_type = "Invalid WR"
        if self._requested_fault_type == "Invalid_V":
            self._requested_fault_type = "Invalid V"

        # Get the value of the requested page table level from the options in the fctrl file
        # Valid levels are 0, 1, 2, 3 for rv64; 0, 1 for rv32.  The isValidPageFaultLevel
        # considers whether the configuration is rv32 or rv64.
        # If the page_fault_level option is not specified, the paging choices for all levels
        # of that page fault type are modified.
        # The default weight of 100 is used unless the 'Weight' is included in the dictionary
        # passed to apply.
        (self._page_fault_level, valid) = self.getOption("PageFaultLevel")
        if not valid: 
            self._page_fault_level = None
        elif (self._page_fault_level == 3) and (VirtualMemory.getPagingMode() == EPagingMode.Sv39):
            self._page_fault_level = 2

        # Get the iteration count
        (self._iter_count, valid) = self.getOption("IterCount")

    def _displayExceptionInfo(self, instr_obj):
        # Report the exception generated
        for ec in self._mExceptionCodes:
            backend_exception_count = self.queryExceptionRecordsCount(ec)
            new_exception = backend_exception_count > self._exception_counts[ec]
            self._exception_counts[ec] = backend_exception_count
            self.notice(
                ">>>>>>>  Exception:  {}    Query value:  {}".format(
                    ec, self.queryExceptionRecordsCount(ec)
                )
            )
            self.notice(
                ">>>>>>>  Instr:  {}    EType:  {}    New Exception? {}   count {}".format(
                    instr_obj["Name"], ec, new_exception, backend_exception_count
                )
            )

class MisalignSequence(Sequence):

    def __init__(self, gen_thread, name=None):
        super().__init__(gen_thread, name)
        self._mExceptionCodes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15)
        self._instr_count = 5
        self._exception_counts = dict.fromkeys(self._mExceptionCodes, 0)
        self._mInstrList = []
        self.instruction_count = 5
        self.load_basic_instructions = merge(LD_Int_instructions, LD_Float_instructions, LD_C_instructions)

        for _ in range(self.instruction_count):
            self._mInstrList.append(self.pickWeighted(self.load_basic_instructions))

    def _genMisalignedDataAddress(self):
        target_addr = self.genVA(Type="D", PrivilegeLevel=1)
        self.notice(">>>>>  Next target addr: {:016x}".format(target_addr))
        if (target_addr & 0x3) == 0:
            target_addr = target_addr | self.random32(1, 3)
        self.notice(">>>>>  Misaligned target addr: {:016x}".format(target_addr))
        return target_addr

    def _add_instrs(self, instrs: list()):
        self._mInstrList = instrs

    def generate(self, **kargs):
        for _ in range(self._instr_count):
            target_addr = self._genMisalignedDataAddress()
            load_instr = self.choice(self._mInstrList)

            mod = self.random32(0, 1)
            if mod == 0:
                self.genInstruction(load_instr)
            else:
                instr_id = self.genInstruction(load_instr, {"LSTarget": target_addr})
                instr_obj = self.queryInstructionRecord(instr_id)
                # Write exception count info into the gen.log
                self._displayExceptionInfo(instr_obj)

    def _displayExceptionInfo(self, instr_obj):
        # Report the exception generated
        for ec in self._mExceptionCodes:
            backend_exception_count = self.queryExceptionRecordsCount(ec)
            new_exception = backend_exception_count > self._exception_counts[ec]
            self._exception_counts[ec] = backend_exception_count
            self.notice(
                ">>>>>>>  Exception:  {}    Query value:  {}".format(
                    ec, self.queryExceptionRecordsCount(ec)
                )
            )
            self.notice(
                ">>>>>>>  Instr:  {}    EType:  {}    New Exception? {}   count {}".format(
                    instr_obj["Name"], ec, new_exception, backend_exception_count
                )
            )

def gen_thread_initialization(gen_thread):
    (delegate_opt, valid) = gen_thread.getOption("DelegateExceptions")
    if valid and delegate_opt == 1:
        # enable exception delegation for some portion of the generated tests...
        delegation_enables = ChoicesModifier(gen_thread)
        weightDict = {"0x0": 0, "0x1": 50}
        delegation_enables.modifyRegisterFieldValueChoices("medeleg.Load page fault", weightDict)
        delegation_enables.modifyRegisterFieldValueChoices(
            "medeleg.Store/AMO page fault", weightDict
        )
        delegation_enables.commitSet()
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp0cfg",value=0xf)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp1cfg",value=0xf)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp2cfg",value=0xf)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp3cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp4cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp5cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp6cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp7cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp8cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp9cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp10cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp11cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp12cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp13cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp14cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp15cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x400000000)
    gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x790000000)
    gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x7ffffffff)
    gen_thread.initializeRegister(name="pmpaddr3",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr4",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr5",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr6",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr7",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr8",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr9",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr10",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr11",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr12",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr13",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr14",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr15",field="address[55:2]",value=0x0)

def AF_gen_thread_initialization(gen_thread):
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp0cfg",value=0xd) 
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp1cfg",value=0xd) # X W R : d/101/XR, f/111/XWR, c/100/X
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp2cfg",value=0xd)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp3cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp4cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp5cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp6cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg0",field="pmp7cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp8cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp9cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp10cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp11cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp12cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp13cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp14cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpcfg2",field="pmp15cfg",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x400000000)
    gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x790000000)
    gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x7ffffffff)
    gen_thread.initializeRegister(name="pmpaddr3",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr4",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr5",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr6",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr7",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr8",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr9",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr10",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr11",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr12",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr13",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr14",field="address[55:2]",value=0x0)
    gen_thread.initializeRegister(name="pmpaddr15",field="address[55:2]",value=0x0)