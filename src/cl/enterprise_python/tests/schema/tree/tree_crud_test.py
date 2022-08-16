# Copyright (C) 2021-present CompatibL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest
import mongoengine as me
from typing import List, Any

from cl.enterprise_python.core.schema.tree.tree_bond import TreeBond
from cl.enterprise_python.core.schema.tree.tree_leg import TreeLeg
from cl.enterprise_python.core.schema.tree.tree_swap import TreeSwap
from cl.enterprise_python.core.schema.tree.tree_trade import TreeTrade


class TreeCrudTest:
    """
    Tests for TreeSwap using MongoEngine ODM and deep style of embedding.
    """

    _alias: str = "deep"

    def connect(self) -> Any:
        """
        Connect and return connection object.

        MongoEngine provides no explicit type for
        the connection so Any is used in annotation.
        """
        # Connect to the database using class name for the table
        return me.connect(self._alias, alias=self._alias)

    def clean_up(self, connection: Any) -> None:
        """Drop database to clean up before and after the test."""
        connection.drop_database(self._alias)

    def create_records(self) -> List[TreeTrade]:
        """
        Return a list of random records objects.
        This method does not write to the database.
        """

        # Create a list of currencies to populate swap records
        ccy_list = ["USD", "GBP", "JPY", "NOK", "AUD"]
        ccy_count = len(ccy_list)

        # Create swap records
        swaps = [
            TreeSwap(
                trade_id=f"T{i+1}",
                trade_type="Swap",
                legs=[
                    TreeLeg(leg_type="Fixed", leg_ccy=ccy_list[i % ccy_count]),
                    TreeLeg(leg_type="Floating", leg_ccy="EUR")
                ]
            )
            for i in range(0, 2)
        ]
        bonds = [
            TreeBond(
                trade_id=f"T{i+1}",
                trade_type="Bond",
                bond_ccy=ccy_list[i % ccy_count]
            )
            for i in range(2, 3)
        ]
        return swaps + bonds

    def test_crud(self):
        """Test CRUD operations."""

        # Connect and set connection parameters
        connection = self.connect()

        # Drop database in case it is left over from the previous test
        self.clean_up(connection)

        # Create swap records
        records = self.create_records()

        # TODO - use bulk insert
        for record in records:
            record.save()

        # Retrieve all records
        print()
        print("All trades")
        for swap in TreeTrade.objects:
            print(swap.trade_id)

        # Retrieve only the swap records
        print()
        print("Swaps only")
        for swap in TreeSwap.objects:
            print(swap.trade_id)

        # Drop database to clean up after the test
        self.clean_up(connection)


if __name__ == "__main__":
    pytest.main([__file__])
