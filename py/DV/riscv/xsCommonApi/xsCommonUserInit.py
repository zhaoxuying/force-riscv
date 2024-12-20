#from riscv.EnvRISCV import EnvRISCV
#from riscv.GenThreadRISCV import GenThreadRISCV
#from base.Sequence import Sequenc

def userInitializationMcounter(gen_thread):
        gen_thread.initializeRegister(name="mcounteren",field="CY",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="TM",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="IR",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM3",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM4",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM5",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM6",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM7",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM8",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM9",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM10",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM11",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM12",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM13",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM14",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM15",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM16",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM17",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM18",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM19",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM20",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM21",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM22",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM23",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM24",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM25",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM26",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM27",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM28",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM29",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM30",value=0x0)
        gen_thread.initializeRegister(name="mcounteren",field="HPM31",value=0x0)

def userInitializationXie(gen_thread):
        gen_thread.initializeRegister(name="mie",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="MSIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="STIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="MTIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="SEIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="MEIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="mie",field="WPRI",value=0x0)

        gen_thread.initializeRegister(name="sie",field="STIP",value=0x0)
        gen_thread.initializeRegister(name="sie",field="SEIP",value=0x0)
        gen_thread.initializeRegister(name="sie",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="sie",field="WPRI",value=0x0)

def userInitializationMideleg(gen_thread):
        gen_thread.initializeRegister(name="mideleg",field="MIDELEG",value=0x0)

def userInitializationXip(gen_thread):
        gen_thread.initializeRegister(name="mip",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="MSIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="STIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="MTIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="SEIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="MEIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="mip",field="WPRI",value=0x0)

        gen_thread.initializeRegister(name="sip",field="STIP",value=0x0)
        gen_thread.initializeRegister(name="sip",field="SEIP",value=0x0)
        gen_thread.initializeRegister(name="sip",field="SSIP",value=0x0)
        gen_thread.initializeRegister(name="sip",field="WPRI",value=0x0)

def userInitializationImpl(gen_thread):
        gen_thread.initializeRegister(name="sbpctl",field="SBPCTL_VAL",value=0x0)
        gen_thread.initializeRegister(name="spfctl",field="SPFCTL_VAL",value=0x0)
        gen_thread.initializeRegister(name="slvpredctl",field="SLVPREDCTL_VAL",value=0x0)
        gen_thread.initializeRegister(name="smblockctl",field="SMBLOCKCTL_VAL",value=0x0)
        gen_thread.initializeRegister(name="srnctl",field="SRNCTL_VAL",value=0x0)

def userInitializationCacheOp(gen_thread):
        gen_thread.initializeRegister(name="cache_op",field="CACHE_OP_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_op_finish",field="CACHE_OP_FINISH_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_level",field="CACHE_LEVEL_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_way",field="CACHE_WAY_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_idx",field="CACHE_IDX_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_bank_num",field="CACHE_BANK_NUM_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_tag_ecc",field="CACHE_TAG_ECC_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_tag_bits",field="CACHE_TAG_BITS_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_tag_low",field="CACHE_TAG_LOW_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_tag_high",field="CACHE_TAG_HIGH_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_ecc_width",field="CACHE_ECC_WIDTH_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_ecc",field="CACHE_DATA_ECC_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_0",field="CACHE_DATA_0_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_1",field="CACHE_DATA_1_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_2",field="CACHE_DATA_2_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_3",field="CACHE_DATA_3_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_4",field="CACHE_DATA_4_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_5",field="CACHE_DATA_5_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_6",field="CACHE_DATA_6_VAL",value=0x0)
        gen_thread.initializeRegister(name="cache_data_7",field="CACHE_DATA_7_VAL",value=0x0)


def userInitializationPmpcfgPC0x80000000(gen_thread):
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
        # for startPC=0x8000_0000
        gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x20000000)
        gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x39000000) 
        gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x3fffffff)     
        # for startPC=0x10_0000_0000
        #gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x400000000)
        #gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x790000000) 
        #gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x7ffffffff)
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

def userInitializationPmpcfg(gen_thread):
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
        # for startPC=0x8000_0000
        gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x20000000)
        gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x39000000) 
        gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x3fffffff)     
        # for startPC=0x10_0000_0000
        #gen_thread.initializeRegister(name="pmpaddr0",field="address[55:2]",value=0x400000000)
        #gen_thread.initializeRegister(name="pmpaddr1",field="address[55:2]",value=0x790000000) 
        #gen_thread.initializeRegister(name="pmpaddr2",field="address[55:2]",value=0x7ffffffff)        
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

def userInitializationEventCounter(gen_thread):
        gen_thread.initializeRegister(name="mcounteren",field="CY",value=0x0)
        gen_thread.initializeRegister(name="scounteren",field="CY",value=0x0)
        gen_thread.initializeRegister(name="mcountinhibit",field="CY",value=0x0)
        gen_thread.initializeRegister(name="mhpmevent3",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent4",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent5",field="EVENT",value=0x1)        
        gen_thread.initializeRegister(name="mhpmevent6",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent7",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent8",field="EVENT",value=0x1) 
        gen_thread.initializeRegister(name="mhpmevent9",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent10",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent11",field="EVENT",value=0x1) 
        gen_thread.initializeRegister(name="mhpmevent12",field="EVENT",value=0x1) 
        gen_thread.initializeRegister(name="mhpmevent13",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent14",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent15",field="EVENT",value=0x1)        
        gen_thread.initializeRegister(name="mhpmevent16",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent17",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent18",field="EVENT",value=0x1) 
        gen_thread.initializeRegister(name="mhpmevent19",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent20",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent21",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent22",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent23",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent24",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent25",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent26",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent27",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent28",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent29",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent30",field="EVENT",value=0x1)
        gen_thread.initializeRegister(name="mhpmevent31",field="EVENT",value=0x1)

def userInitializationMstatus(gen_thread):
        gen_thread.initializeRegister(name="mstatus", field="WPRI" ,  value = 0x0) #bit62:38,31-23,4,2,0
        gen_thread.initializeRegister(name="mstatus", field="MBE" ,  value = 0x0)  #bit37
        gen_thread.initializeRegister(name="mstatus", field="SBE" ,  value = 0x0)  #bit36
        gen_thread.initializeRegister(name="mstatus", field="SXL" ,  value = 0x2)  #bit[35:34]
        gen_thread.initializeRegister(name="mstatus", field="UXL" ,  value = 0x2)  #bit[33:32]
        gen_thread.initializeRegister(name="mstatus", field="TSR" ,  value = 0x0)  #bit22
        gen_thread.initializeRegister(name="mstatus", field="TW"  ,  value = 0x0)  #bit21
        gen_thread.initializeRegister(name="mstatus", field="TVM" ,  value = 0x0)  #bit20
        gen_thread.initializeRegister(name="mstatus", field="MXR" ,  value = 0x0)  #bit19
        gen_thread.initializeRegister(name="mstatus", field="SUM" ,  value = 0x0)  #bit18
        gen_thread.initializeRegister(name="mstatus", field="MPRV",  value = 0x0)  #bit17
                                                                                   #bit[16:15] XS
        gen_thread.initializeRegister(name="mstatus", field="FS"  ,  value = 0x3)  #bit[14:13]
        gen_thread.initializeRegister(name="mstatus", field="MPP" ,  value = 0x0)  #bit[12:]
        gen_thread.initializeRegister(name="mstatus", field="VS"  ,  value = 0x1)  #bit[10:9] VS
        gen_thread.initializeRegister(name="mstatus", field="SPP" ,  value = 0x1)  #bit8
        gen_thread.initializeRegister(name="mstatus", field="MPIE",  value = 0x1)  #bit7        
        gen_thread.initializeRegister(name="mstatus", field="UBE" ,  value = 0x1)  #bit6
        gen_thread.initializeRegister(name="mstatus", field="SPIE",  value = 0x0)  #bit5
        gen_thread.initializeRegister(name="mstatus", field="MIE" ,  value = 0x1)  #bit3
        gen_thread.initializeRegister(name="mstatus", field="SIE" ,  value = 0x0)  #bit1

def userInitializationVCSR(gen_thread):
        #gen_thread.initializeRegister(name="vl",field="VL",value=0x1)
        gen_thread.initializeRegister(name="vxsat",field="VXSAT",value=0x0)
        gen_thread.initializeRegister(name="vxrm",field="VXRM",value=0x0)
        #gen_thread.initializeRegister(name="vtype",field="VLMUL",value=0x2)
        #gen_thread.initializeRegister(name="vtype",field="VSEW",value=0x2)

def userInitializationMisa(gen_thread):
        gen_thread.initializeRegister(name="misa",field="H",value=0x1)

def userInitializationNanHuV3(gen_thread):
        userInitializationPmpcfg(gen_thread)
        userInitializationMstatus(gen_thread)

def userInitializationKunMingHu(gen_thread):
        userInitializationVCSR(gen_thread)
        userInitializationPmpcfgPC0x80000000(gen_thread)
        userInitializationMisa(gen_thread)
        userInitializationMstatus(gen_thread)
        userInitializationEventCounter(gen_thread)

def userInitializationXiangShanCore(gen_thread):
        userInitializationKunMingHu(gen_thread)




        

