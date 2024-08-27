-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this file,
-- You can obtain one at http://mozilla.org/MPL/2.0/.
--
-- Copyright (c) 2014-2024, Lars Asplund lars.anders.asplund@gmail.com

library vunit_lib;
context vunit_lib.vunit_context;

entity tb_example is
  generic (
    runner_cfg : string;
    value : natural := 42);
end entity;

architecture tb of tb_example is
begin
  main : process
    function recurse(value : integer) return integer is
    begin
      if value <= 0 then
        return 0;
      else
        return 1 + recurse(value - 1);
      end if;
    end;
  begin
    test_runner_setup(runner, runner_cfg);

    while test_suite loop
      if run("test") then
      end if;

      info("Running " & running_test_case & " with generic value = " & to_string(value));
      info("Recurse = " & to_string(recurse(value)));
    end loop;

    test_runner_cleanup(runner);
  end process;
end architecture;
