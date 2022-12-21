#!/usr/bin/env python3
# Copyright 2010-2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""We are trying to group items in equal sized groups.
Each item has a color and a value. We want the sum of values of each group to
be as close to the average as possible.
Furthermore, if one color is an a group, at least k items with this color must
be in that group."""

import math
from ortools.sat.python import cp_model

# Data

max_quantities = [
    ["N_Total", 1944],
    ["P2O5", 1166.4],
    ["K2O", 1822.5],
    ["CaO", 1458],
    ["MgO", 486],
    ["Fe", 9.7],
    ["B", 2.4],
]

chemical_set = [
    ["A", 0, 0, 510, 540, 0, 0, 0],
    ["B", 110, 0, 0, 0, 160, 0, 0],
    ["C", 61, 149, 384, 0, 30, 1, 0.2],
    ["D", 148, 70, 245, 0, 15, 1, 0.2],
    ["E", 160, 158, 161, 0, 10, 1, 0.2],
]

NUM_PRODUCTS = len(max_quantities)
ALL_PRODUCTS = range(NUM_PRODUCTS)

NUM_SETS = len(chemical_set)
ALL_SETS = range(NUM_SETS)

# Model

model = cp_model.CpModel()

# Scale quantities by 100.
max_set = [
    int(
        math.ceil(
            min(max_quantities[q][1] * 1000 / chemical_set[s][q + 1]
                for q in ALL_PRODUCTS if chemical_set[s][q + 1] != 0)))
    for s in ALL_SETS
]

set_vars = [model.NewIntVar(0, max_set[s], f"set_{s}") for s in ALL_SETS]

epsilon = model.NewIntVar(0, 10000000, "epsilon")

for p in ALL_PRODUCTS:
    model.Add(
        sum(int(chemical_set[s][p + 1] * 10) * set_vars[s]
            for s in ALL_SETS) <= int(max_quantities[p][1] * 10000))
    model.Add(
        sum(int(chemical_set[s][p + 1] * 10) * set_vars[s]
            for s in ALL_SETS) >= int(max_quantities[p][1] * 10000) - epsilon)

model.Minimize(epsilon)

# Creates a solver and solves.
solver = cp_model.CpSolver()
status = solver.Solve(model)
print(f"Status = {solver.StatusName(status)}")
# The objective value of the solution.
print(f"Optimal objective value = {solver.ObjectiveValue() / 10000.0}")

for s in ALL_SETS:
    print(f"  {chemical_set[s][0]} = {solver.Value(set_vars[s]) / 1000.0}", end=" ")
    print()
for p in ALL_PRODUCTS:
    name = max_quantities[p][0]
    max_quantity = max_quantities[p][1]
    quantity = sum(
        solver.Value(set_vars[s]) / 1000.0 * chemical_set[s][p + 1]
        for s in ALL_SETS)
    print(f"{name}: {quantity} out of {max_quantity}")
