#!/usr/bin/env python3

import argparse
import logging
import os

import sqlalchemy

from fastqc_db.fastqc_db import fastqc_db


def setup_logging(args: argparse.Namespace, job_uuid: str) -> logging.Logger:
    logging.basicConfig(
        filename=os.path.join(job_uuid + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def main() -> int:
    parser = argparse.ArgumentParser('FastQC to sqlite')

    # Logging flags.
    parser.add_argument(
        '-d',
        '--debug',
        action='store_const',
        const=logging.DEBUG,
        dest='level',
        help='Enable debug logging.',
    )
    parser.set_defaults(level=logging.INFO)

    # Required flags.
    parser.add_argument('--job_uuid', required=True)
    parser.add_argument('--INPUT', required=True)

    # setup required parameters
    args = parser.parse_args()
    job_uuid = args.job_uuid
    fastqc_zip_path = args.INPUT

    fastqc_zip_name = os.path.basename(fastqc_zip_path)
    fastqc_zip_base, _ = os.path.splitext(fastqc_zip_name)

    logger = setup_logging(args, job_uuid)

    sqlite_name = f'{fastqc_zip_base}.db'
    engine_path = f'sqlite:///{sqlite_name}'
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    fastqc_db(job_uuid, fastqc_zip_path, engine, logger)
    return 0


if __name__ == '__main__':
    main()
