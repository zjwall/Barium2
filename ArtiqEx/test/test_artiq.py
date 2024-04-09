import argparse
import sys
from operator import itemgetter
import logging
from collections import defaultdict

import h5py

from llvmlite_artiq import binding as llvm

from sipyco import common_args

from artiq import __version__ as artiq_version
from artiq.language.environment import EnvExperiment, ProcessArgumentManager
from artiq.language.types import TBool
from artiq.master.databases import DeviceDB, DatasetDB
from artiq.master.worker_db import DeviceManager, DatasetManager
from artiq.coredevice.core import CompileError, host_only
from artiq.compiler.embedding import EmbeddingMap
from artiq.compiler import import_cache
from artiq.tools import *
from artiq.frontend.artiq_run import _build_experiment, get_argparser, DummyScheduler, DummyCCB

args = get_argparser().parse_args({'C:\\Users\\barium133\\ArtiqEx\\test\\urukul.py'})
device_mgr = DeviceManager(DeviceDB(args.device_db),
                           virtual_devices={"scheduler": DummyScheduler(),
                                            "ccb": DummyCCB()})
dataset_db = DatasetDB(args.dataset_db)
dataset_mgr = DatasetManager(dataset_db)

exp_inst=_build_experiment(device_mgr, dataset_mgr, args)
exp_inst.prepare()
exp_inst.build()
exp_inst.run()



