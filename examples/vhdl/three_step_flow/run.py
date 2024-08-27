# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2024, Lars Asplund lars.anders.asplund@gmail.com

from argparse import Namespace
from pathlib import Path
from vunit import VUnit, VUnitCLI
from os import environ

cli = VUnitCLI()

environ["VUNIT_SIMULATOR"] = "modelsim"

vu = VUnit.from_argv()
vu.add_vhdl_builtins()

lib1 = vu.add_library("lib1")
lib1.add_source_files(Path(__file__).parent / "sub_module" / "*.vhd")

lib2 = vu.add_library("lib2")
lib2.add_source_files(Path(__file__).parent / "*.vhd")

tb = lib2.test_bench("tb_example")
test = tb.test("test")

for value in range(5):
    test.add_config(name=f"{value}", generics=dict(value=value))

vu.set_sim_option("modelsim.three_step_flow", True)

vu.main()
