#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from __future__ import with_statement
from overtherepy import OverthereHostSession
from liquibase import *

def perform_update_cmd(cmd, target_changelog, container, session, context):
    cmd_line = build_cmd_line(container)
    cmd_line.extend(["--changeLogFile=%s" % target_changelog.path, cmd])
    print_cmd_line(cmd_line, context)
    session.execute(cmd_line)

session = OverthereHostSession(container.host, stream_command_output=True, execution_context=context)
with session:
    target_changelog_root_file = get_changelog_root(session, deployed)
    perform_update_cmd("updateSQL", target_changelog_root_file, container, session, context)
    perform_update_cmd("update", target_changelog_root_file, container, session, context)

