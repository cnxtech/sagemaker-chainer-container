# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import chainermn
import mpi4py.MPI


def train():
    mpi_comm = mpi4py.MPI.COMM_WORLD

    if mpi_comm.rank == 0:
        raise ValueError('failure!')
    chainermn.create_communicator('naive', mpi_comm)
