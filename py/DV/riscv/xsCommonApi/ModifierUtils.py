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
import itertools

from base.ChoicesModifier import ChoicesModifier
from EnumsRISCV import EPagingMode
import Log
import RandomUtils
import VirtualMemory


class PageFaultModifier(ChoicesModifier):
    def __init__(self, aGenThread, aAppRegWidth):
        super().__init__(aGenThread, "PageFaultModifier")

        self._mValidFaultTypes = [
            "Invalid DA",
            "Invalid U",
            "Invalid X",
            "Invalid WR",
            "Invalid V",
        ]

        table_levels = 0
        if VirtualMemory.getPagingMode() == EPagingMode.Sv32:
            table_levels = 2
        elif VirtualMemory.getPagingMode() == EPagingMode.Sv39:
            table_levels = 3
        else:
            table_levels = 4

        self._mValidFaultLevels = {
            "Invalid DA": range(0, table_levels),
            "Invalid U": range(0, table_levels),
            "Invalid X": range(0, table_levels),
            "Invalid WR": range(0, table_levels),
            "Invalid V": range((table_levels - 1), -1, -1),
        }

        self._mValidPrivilegeLevels = {
            "Invalid DA": ["S"],
            "Invalid U": ["S"],
            "Invalid X": ["S"],
            "Invalid WR": ["S"],
            "Invalid V": ["S"],
        }

    def getValidFaultTypes(self):
        return self._mValidFaultTypes

    def getValidFaultLevels(self):
        return self._mValidFaultLevels

    def update(self, **kwargs):
        if "All" in kwargs:
            self.updateAllFaultChoices()
        elif "Type" in kwargs:
            self._updateWithType(kwargs["Type"], **kwargs)
        else:
            Log.error("specify All or fault name as kwarg to update choices.")

    def modifyExceptionRegulation(self):
        print('--- test')
        choice_dict = {"Prevent": 0, "Allow": 0, "Trigger": 100}
        self.modifyPagingChoices("InstructionPageFault#S#stage 1", choice_dict)
        self.modifyPagingChoices("LoadPageFault#S#stage 1", choice_dict)
        self.modifyPagingChoices("StoreAmoPageFault#S#stage 1", choice_dict)

    def updatePageFaultChoice(self, aType, aLevel, aPriv, aWeight):
        choice_name = "{}#level {}#{}#stage 1".format(aType, aLevel, aPriv)
        # choice_dict = {"false": 100 - aWeight, "true": aWeight}
        # self.modifyPagingChoices(choice_name, choice_dict)
        choice_dict = {"false": 0, "true": 100}
        self.modifyPagingChoices(choice_name, choice_dict)

    def updateFaultTypeChoices(self, aType, **kwargs):
        table_levels = kwargs.get("Level", self._mValidFaultLevels[aType])
        self._validateTableLevels(aType, table_levels)
        priv_levels = kwargs.get("Privilege", self._mValidPrivilegeLevels[aType])
        self._validatePrivilegeLevels(aType, priv_levels)
        weight = kwargs.get("Weight", 100)
        self._validateWeight(aType, weight)

        for (table_level, priv_level) in itertools.product(table_levels, priv_levels):
            self.updatePageFaultChoice(aType, table_level, priv_level, weight)

        self.modifyExceptionRegulation()

        if "All" in kwargs:
            # ensure we can get both superpages/full walks for last level
            # ptr + misaligned superpage
            self.updateSuperpageSizeChoices(50)
        elif aType == "Misaligned Superpage":
            self.updateSuperpageSizeChoices(100)  # needs superpage descriptor
        elif aType == "Last Level Pointer":
            self.updateSuperpageSizeChoices(0)  # needs level 0 (4K) table descriptor

    def updateAllFaultChoices(self, **kwargs):
        for fault_type in self._mValidFaultTypes:
            self.updateFaultTypeChoices(fault_type, **kwargs)

    def updateSuperpageSizeChoices(self, aWeight):
        choice_name = "Page size#4K granule#S#stage 1"
        choice_dict = {
            "4K": 101 - aWeight,
            "2M": aWeight,
            "1G": aWeight,
            "512G": 0,
        }
        self.modifyPagingChoices(choice_name, choice_dict)

    def _updateWithType(self, aType, **kwargs):
        if aType in self._mValidFaultTypes:
            self.updateFaultTypeChoices(aType, **kwargs)
        else:
            Log.error("invalid type specified, type={}".format(aType))

    def _validateTableLevels(self, aType, aTableLevels):
        for table_level in aTableLevels:
            if table_level not in self._mValidFaultLevels[aType]:
                Log.error("invalid table level={} for fault type={}".format(table_level, aType))

    def _validatePrivilegeLevels(self, aType, aPrivLevels):
        for priv_level in aPrivLevels:
            if priv_level not in self._mValidPrivilegeLevels[aType]:
                Log.error("invalid priv level={} for fault type={}".format(priv_level, aType))

    def _validateWeight(self, aType, aWeight):
        if not (0 <= aWeight <= 100):
            Log.error(
                "invalid weight specified, please use integer between "
                "0-100. weight={}".format(aWeight)
            )


class TrapsRedirectModifier(ChoicesModifier):
    def __init__(self, aGenThread):
        super().__init__(aGenThread, "TrapsRedirectModifier")

        self.mSupportedExceptions = {
            "Instruction address misaligned": 1,
            "Instruction access fault": 1,
            "Illegal instruction": 1,
            "Breakpoint": 1,
            "Load address misaligned": 1,
            "Load access fault": 1,
            "Store/AMO address misaligned": 1,
            "Store/AMO access fault": 1,
            "Environment call from U-mode": 1,
            "Environment call from S-mode": 1,
            "Instruction page fault": 1,
            "Load page fault": 1,
            "Store/AMO page fault": 1,
        }

        self.mHaveMods = False

    def update(self, **kwargs):
        try:
            if "Weight" in kwargs:
                self.updateChoices(
                    kwargs["ExceptionCode"],
                    kwargs["TrapChoice"],
                    kwargs["Weight"],
                )
            else:
                self.updateChoices(kwargs["ExceptionCode"], kwargs["TrapChoice"])
        except KeyError:
            Log.error(
                "TrapDelegationRedirectionModifier: 'ExceptionCode' or "
                "'TrapChoice' arguments missing."
            )

    def updateChoices(self, aExceptionCode, aTrapChoice, aWeight):
        try:
            rcode = self.mSupportedExceptions[aExceptionCode]
        except KeyError:
            Log.error(
                "TrapDelegationRedirectionModifier: ExceptionCode '%s' is not supported.",
                aExceptionCode,
            )

        if aTrapChoice == "Delegate":
            self.delegateException(aExceptionCode, aWeight)
        elif aTrapChoice == "Redirect":
            self.redirectException(aExceptionCode, aWeight)
        else:
            Log.error(
                "TrapDelegationRedirectionModifier: TrapChoice '%s' not "
                "recognized" % aTrapChoice
            )

    def delegateException(self, aExceptionCode, aWeight=100):
        my_choice = "medeleg.{}".format(aExceptionCode)
        Log.notice("delegation choice:{}".format(my_choice))
        weightDict = {"0x0": 100 - aWeight, "0x1": aWeight}
        self.modifyRegisterFieldValueChoices(my_choice, weightDict)
        self.mHaveMods = True

    def redirectException(self, aExceptionCode, aWeight=100):
        my_choice = "Redirect Trap - {}".format(aExceptionCode)
        Log.notice("redirect choice:{}".format(my_choice))
        weightDict = {"DoNotRedirect": 100 - aWeight, "DoRedirect": aWeight}
        self.modifyGeneralChoices(my_choice, weightDict)
        self.mHaveMods = True

    def commit(self):
        if self.mHaveMods:
            self.commitSet()


# displayPageInfo
# formats some of the information contained in the page object returned by the self.getPageInfo() API.
# The infomation becomes [notice] records in the gen.log file.
# Required arguments:
# - MainSequence object from test template
# - Page object returned from the self.getPageInfo()
def displayPageInfo(seq, page_obj):
    seq.notice(">>>>>>>  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    seq.notice(">>>>>>>  Page Object:  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    for (key, value) in page_obj.items():
        if key == "Page":
            _display_page_details(seq, value)
        elif key.startswith("Table"):
            _display_table_details(seq, value)

    seq.notice(">>>>>>>  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


def _display_page_details(seq, page_details):
    if page_details["PageSize"] == 2 ** 12:
        page_size_string = "4KB"
    elif page_details["PageSize"] == 2 ** 21:
        page_size_string = "2MB"
    elif page_details["PageSize"] == 2 ** 30:
        page_size_string = "1GB"
    elif page_details["PageSize"] == 2 ** 39:
        page_size_string = "512GB"
    else:
        page_size_string = "unknown"

    seq.notice(">>>>>>>      Page Size:  {}".format(page_size_string))
    seq.notice(
        ">>>>>>>      Virtual Address Range:    {:#018x} - {:#018x}".format(
            page_details["Lower"], page_details["Upper"]
        )
    )
    seq.notice(
        ">>>>>>>      Physical Address Range:   {:#018x} - {:#018x}".format(
            page_details["PhysicalLower"], page_details["PhysicalUpper"]
        )
    )
    seq.notice(">>>>>>>      Descriptor:  {:#018x}".format(page_details["Descriptor"]))
    seq.notice(
        ">>>>>>>      Descriptor Address:  {}".format(page_details["DescriptorDetails"]["Address"])
    )
    seq.notice(
        ">>>>>>>      Descriptor Details:    DA         G          U          X          WR         V"
    )
    seq.notice(
        (">>>>>>>      Descriptor Details:    " + "{:<10} " * 6 + " ").format(
            page_details["DescriptorDetails"]["DA"],
            page_details["DescriptorDetails"]["G"],
            page_details["DescriptorDetails"]["U"],
            page_details["DescriptorDetails"]["X"],
            page_details["DescriptorDetails"]["WR"],
            page_details["DescriptorDetails"]["V"],
        )
    )


def _display_table_details(seq, table_details):
    for (field, info) in table_details.items():
        if field in ("DescriptorAddr", "Descriptor"):
            seq.notice(">>>>>>>      {:<20}:    {:#018x}".format(field, info))
        elif field == "Level":
            seq.notice(">>>>>>>    {}  {}".format(field, info))
        elif field == "DescriptorDetails":
            seq.notice(
                ">>>>>>>      PPN of Next PTE     :    {}".format(
                    table_details["DescriptorDetails"]["Address"]
                )
            )
