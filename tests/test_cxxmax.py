from progressivis.core import aio
from progressivis.core.scheduler import Scheduler
from progressivis import Print, RandomPTable
from progressivis.table.stirrer import Stirrer, StirrerView
from progressivis_cpp.examples.cxxmax import Max  # type: ignore
from unittest import TestCase
import numpy as np
import sys
from typing import Any


def terse(x: Any) -> None:
    _ = x
    print(".", end="", file=sys.stderr, flush=True)


class TestCxxMax(TestCase):
    def compare(self, res1: dict[str, Any], res2: dict[str, Any]) -> None:
        v1 = np.array(list(res1.values()))
        v2 = np.array(list(res2.values()))
        # print('v1 = ', v1)
        # print('v2 = ', v2)
        self.assertTrue(np.allclose(v1, v2, rtol=1e-04))

    def test_max(self) -> None:
        s = Scheduler()
        random = RandomPTable(10, rows=10_000, scheduler=s)
        max_ = Max(name="max_" + str(hash(random)), scheduler=s)
        max_.input[0] = random.output.result
        pr = Print(proc=terse, scheduler=s)
        pr.input[0] = max_.output.result
        aio.run(s.start())
        assert random.result is not None
        res1 = random.result.max()
        res2 = max_.cxx_module.get_output_table().last().to_dict(ordered=True)
        self.compare(res1, res2)

    def test_stirrer(self) -> None:
        s = Scheduler()
        random = RandomPTable(2, rows=100_000, scheduler=s)
        stirrer = Stirrer(
            update_column="_1",
            delete_rows=5,
            update_rows=5,
            fixed_step_size=100,
            scheduler=s,
        )
        stirrer.input[0] = random.output.result
        max_ = Max(name="max_" + str(hash(random)), scheduler=s)
        max_.input[0] = stirrer.output.result
        pr = Print(proc=terse, scheduler=s)
        pr.input[0] = max_.output.result
        aio.run(s.start())
        assert random.result is not None
        res1 = random.result.max()
        res2 = max_.cxx_module.get_output_table().last().to_dict(ordered=True)
        self.compare(res1, res2)

    def test_stirrer_view(self) -> None:
        s = Scheduler()
        random = RandomPTable(2, rows=100_000, scheduler=s)
        stirrer = StirrerView(
            update_column="_1",
            delete_rows=5,
            update_rows=5,
            fixed_step_size=100,
            scheduler=s,
        )
        stirrer.input[0] = random.output.result
        max_ = Max(name="max_" + str(hash(random)), scheduler=s)
        max_.input[0] = stirrer.output.result
        pr = Print(proc=terse, scheduler=s)
        pr.input[0] = max_.output.result
        aio.run(s.start())
        assert random.result is not None
        res1 = random.result.max()
        res2 = max_.cxx_module.get_output_table().last().to_dict(ordered=True)
        self.compare(res1, res2)
