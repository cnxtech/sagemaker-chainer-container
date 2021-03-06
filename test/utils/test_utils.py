# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from __future__ import absolute_import

from contextlib import contextmanager
import fcntl
import os
import tarfile
import time


def predict_and_assert_response_length(estimator, data, instance_type, serializer=None,
                                       deserializer=None, content_type='application/x-npy'):
    with local_mode_lock():
        try:
            predictor = estimator.deploy(1, instance_type)
            if content_type != 'application/x-npy':
                predictor.content_type = content_type
                predictor.serializer = serializer
                predictor.accept = content_type
                predictor.deserializer = deserializer

            response = predictor.predict(data)
            assert len(response) == len(data)
        finally:
            predictor.delete_endpoint()


def files_exist(output_path, directory_file_map):
    for directory, files in directory_file_map.items():
        with tarfile.open(os.path.join(output_path, '{}.tar.gz'.format(directory))) as tar:
            for f in files:
                tar.getmember(f)


@contextmanager
def local_mode_lock():
    base_path = os.path.dirname(os.path.realpath(__file__))
    lock_path = os.path.join(base_path, '..', 'resources', 'local_mode_lock')

    # Since Local Mode uses the same port for serving, we need a lock in order
    # to allow concurrent test execution.
    local_mode_lock_fd = open(lock_path, 'w')
    local_mode_lock = local_mode_lock_fd.fileno()

    fcntl.lockf(local_mode_lock, fcntl.LOCK_EX)

    try:
        yield
    finally:
        time.sleep(5)
        fcntl.lockf(local_mode_lock, fcntl.LOCK_UN)
