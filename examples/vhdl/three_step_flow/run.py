# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2024, Lars Asplund lars.anders.asplund@gmail.com

from argparse import Namespace
from pathlib import Path
from vunit import VUnit, VUnitCLI
from os import environ
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s.%(msecs)03d - %(levelname)7s - %(message)s", datefmt="%H:%M:%S"
)

cli = VUnitCLI()

environ["VUNIT_SIMULATOR"] = "modelsim"

vu = VUnit.from_argv()
vu.add_vhdl_builtins()

root = Path(__file__).parent

lib1 = vu.add_library("lib1")
lib1.add_source_files(root / "sub_module" / "*.vhd")

lib2 = vu.add_library("lib2")
lib2.add_source_files(root / "*.vhd")

tb = lib2.test_bench("tb_example")
test = tb.test("test")

for value in range(5):
    test.add_config(name=f"{value}", generics=dict(value=value))

vu.set_sim_option("modelsim.three_step_flow", True)
vu.set_sim_option("modelsim.vsim_flags", ["-novopt", "-suppress", "12110"])

event_handler = LoggingEventHandler()
observer = Observer()
observer.schedule(event_handler, root / "vunit_out" / "modelsim", recursive=True)
observer.start()


def post_run(results):
    observer.stop()
    observer.join()


vu.main(post_run=post_run)
