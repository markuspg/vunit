-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this file,
-- You can obtain one at http://mozilla.org/MPL/2.0/.
--
-- Copyright (c) 2014-2024, Lars Asplund lars.anders.asplund@gmail.com

library vunit_lib;
context vunit_lib.vunit_context;

entity tb_a is
  generic (
    runner_cfg : string);
end entity;

architecture tb of tb_a is
begin
  main : process
    function recurse(value : integer) return integer is
    begin
      if value <= 0 then
        return 0;
      elsif value mod 2 = 0 then
        return 1 + recurse(value - 1);
      else
        return recurse(value - 1);
      end if;
    end;
  begin
    test_runner_setup(runner, runner_cfg);

    info("Running tb_a: " & to_string(recurse(17)));

    test_runner_cleanup(runner);
  end process;
end architecture;
