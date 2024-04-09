from artiq.experiment import *
from artiq.master.databases import DeviceDB
from artiq.master.worker_db import DeviceManager
from artiq.frontend.artiq_run import *
from artiq.frontend.artiq_run import _build_experiment, get_argparser, DummyScheduler, DummyCCB

args = get_argparser(False).parse_args()
common_args.init_logger_from_args(args)

device_mgr = DeviceManager(DeviceDB(args.device_db),
                               virtual_devices={"scheduler": DummyScheduler(),
                                                "ccb": DummyCCB()})
dataset_db = DatasetDB(args.dataset_db)
dataset_mgr = DatasetManager(dataset_db)

exp_inst = _build_experiment(device_mgr, dataset_mgr, args)
