# opengauss_sqlalchemy/psycopg2.py
# Copyright (C) 2021-2022 Huawei.
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from sqlalchemy.dialects.postgresql.psycopg2 import PGCompiler_psycopg2, PGDialect_psycopg2
from sqlalchemy import schema
from sqlalchemy import util

from opengauss_sqlalchemy.base import OpenGaussDDLCompiler, OpenGaussIdentifierPreparer


class OpenGaussCompiler_psycopg2(PGCompiler_psycopg2):
    def get_cte_preamble(self, recursive):
        return "WITH RECURSIVE"


class OpenGaussDialect_psycopg2(PGDialect_psycopg2):
    name = "opengauss"
    driver = "psycopg2"

    cte_follows_insert = True
    supports_statement_cache = True

    statement_compiler = OpenGaussCompiler_psycopg2
    ddl_compiler = OpenGaussDDLCompiler
    preparer = OpenGaussIdentifierPreparer

    construct_arguments = [
        (
            schema.Index,
            {
                "concurrently": False,
                "using": None,
                "ops": {},
                "local": [],
                "with": {},
                "tablespace": None,
                "where": None,
            },
        ),
        (
            schema.Table,
            {
                "ignore_search_path": False,
                "with": {},
                "on_commit": None,
                "compress": False,
                "tablespace": None,
                "distribute_by": None,
                "to": None,
                "partition_by": None,
                "enable_row_movement": False,
            },
        ),
    ]

    _supports_table_distribute_by = False

    @util.memoized_property
    def _isolation_lookup(self):
        extensions = self._psycopg2_extensions()

        return {
            "AUTOCOMMIT": extensions.ISOLATION_LEVEL_AUTOCOMMIT,
            "READ COMMITTED": extensions.ISOLATION_LEVEL_READ_COMMITTED,
            "READ UNCOMMITTED": extensions.ISOLATION_LEVEL_READ_UNCOMMITTED,
            "REPEATABLE READ": extensions.ISOLATION_LEVEL_REPEATABLE_READ,
            # opengauss does NOT support SERIALIZABLE
        }

    def _get_server_version_info(self, connection):
        # most of opengauss features are same with postgres 9.2.4
        return (9, 2, 4)


dialect = OpenGaussDialect_psycopg2
