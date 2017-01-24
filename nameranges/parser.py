# Copyright 2017 Bright Computing Holding BV.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re


class RangeParseError(Exception):
    pass


def parse(grouped_names):
    """Parse group of grouped names into an array of extended names

    :param grouped_names Represent the names grouped
    :type grouped_names: string
    :return array of extended names
    """
    names = []
    try:
        parts = re.split(r'\)?[, ]\(?', grouped_names)
        for part in parts:
            sbr1 = part.find('[')
            if sbr1 != -1:
                # We have a source string like "node0[01..11]"
                sbr2 = part.find(']')
                if sbr2 != -1:
                    header = part[:sbr1]
                    footer = part[sbr2 + 1:]
                    rng = part[sbr1 + 1:sbr2]
                    dots = rng.find('..')
                    start = rng[:dots]
                    start_len = len(start)
                    end = rng[dots + 2:]

                    start_int = 0
                    end_int = 0
                    try:
                        start_int = int(start)
                        end_int = int(end)
                    except ValueError:
                        raise RangeParseError("Incorrect range format")
                    temp_hostnames = ""

                    for r in range(start_int, end_int + 1):
                        zeros = '0' * (start_len - len(str(r)))
                        temp_hostnames += header + zeros + str(r) + footer + ','
                    names.extend(parse(temp_hostnames))
            else:
                # Convert "node001..node011" to "node0[01..11]" and parse again
                dots = part.find('..')
                if dots == -1:
                    if len(part):
                        names.append(part)
                    continue
                s1 = part[:dots]
                s2 = part[dots + 2:]
                length1 = len(s1)
                length2 = len(s2)
                if length1 != length2:
                    raise Exception("Incorrect range format")
                base = ''
                diff = False
                for i in range(0, length1):
                    if s1[i] == s2[i]:
                        base += s1[i]
                    else:
                        diff = True
                        std_form = "%s[%s..%s]" % (base, s1[i:], s2[i:])
                        names.extend(parse(std_form))
                        break
                # Something is wrong => try to handle as better as possible
                if not diff:
                    if length1 == length2:
                        names.append(base)
    except Exception as ex:
        raise RangeParseError(str(ex))
    return names
