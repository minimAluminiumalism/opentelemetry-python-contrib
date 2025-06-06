# Copyright The OpenTelemetry Authors
#
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

import asyncio

from .nonstreaming_base import NonStreamingTestCase


class TestGenerateContentAsyncNonstreaming(NonStreamingTestCase):
    def generate_content(self, *args, **kwargs):
        return asyncio.run(
            self.client.aio.models.generate_content(*args, **kwargs)  # pylint: disable=missing-kwoa
        )

    @property
    def expected_function_name(self):
        return "google.genai.AsyncModels.generate_content"
