"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <lauris.skraucis@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import datetime
import logging

from PyMatcha.utils import create_blocks_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Block(Model):
    table_name = "blocks"

    id = Field(int, modifiable=False)
    blocker_id = Field(int)
    blocked_id = Field(int)
    dt_blocked = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create(blocker_id: int, blocked_id: int, dt_blocked: datetime.datetime = datetime.datetime.utcnow()) -> Block:
        new_blocked = Block(blocker_id=blocker_id, blocked_id=blocked_id, dt_blocked=dt_blocked)
        new_blocked.save()
        logging.debug("Creating new block")
        return new_blocked

    @classmethod
    def create_table(cls):
        create_blocks_table(cls.db)
