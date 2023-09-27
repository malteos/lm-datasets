import argparse
import yaml
import logging


logger = logging.getLogger(__name__)


def get_common_argparser(required_configs: bool = False):
    common_parser = argparse.ArgumentParser()

    common_parser.add_argument(
        "--raw_datasets_dir",
        default=None,
        type=str,
        help="Dataset files are read from this directory (needed for `is_downloaded` field)",
    )
    common_parser.add_argument(
        "--output_dir",
        default=None,
        type=str,
        help="Processed dataset are saved in this directory (need for `has_output_file` field)",
    )
    common_parser.add_argument(
        "--output_format",
        default="jsonl",
        type=str,
        help="Format of processed dataset (jsonl,parquet; need for `has_output_file` field)",
    )
    common_parser.add_argument(
        "--extra_dataset_registries",
        default=None,
        type=str,
        help="List of Python packages to load dataset registries",
    )
    common_parser.add_argument(
        "-c",
        "--configs",
        nargs="+",
        help=(
            "Paths to one or more YAML-config files (duplicated settings are override based on config order; "
            "cmd args override configs)"
        ),
        default=None,
        dest="config_paths",
        required=required_configs,
    )

    return common_parser


class Config:
    local_dirs_by_dataset_id = {}
    local_dirs_by_source_id = {}
    sampling_factor_by_dataset_id = {}
    sampling_factor_by_source_id = {}
    sampling_factor_by_language = {}

    selected_dataset_ids = []
    selected_source_ids = []

    validation_ratio = 0.005  # number of documents in the split: len(dataset) * ratio
    validation_min_total_docs = 1_000  # to be used as validation set, the dataset must have at least n docs
    validation_max_split_docs = 1_000  # number of documents in validation split are capped at this numbers
    validation_min_split_docs = 10  # split must have at least this number of documents, otherwise it will be discarded
    tokenizer_train_ratio = 0.1  # % of train data used for tokenizer training

    verbose = False
    log_file = None

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def init_logger(self, logger_name):
        log_handlers = [logging.StreamHandler()]

        if self.log_file:
            log_handlers.append(logging.FileHandler(self.log_file))

        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG if self.verbose else logging.INFO,
            handlers=log_handlers,
        )
        logger = logging.getLogger(logger_name)

        return logger


def parse_args_and_get_config(parser):
    args = parser.parse_args()
    config = {}

    config = {}

    if args.config_paths:
        for config_path in args.config_paths:
            logger.info(f"Loading config: {config_path}")
            with open(config_path) as f:
                _config = yaml.safe_load(f)

                config.update(_config)

    # Override with args
    config.update(args.__dict__)

    return Config(**config)