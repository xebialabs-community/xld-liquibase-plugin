#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from __future__ import with_statement
from overtherepy import OverthereHostSession
from liquibase import *

def perform_rollback_cmd(cmd, tag, target_changelog, container, session, context):
    cmd_line = build_cmd_line(container)
    cmd_line.extend(["--changeLogFile=%s" % target_changelog.path, cmd, tag])
    print_cmd_line(cmd_line, context)
    session.execute(cmd_line)


session = OverthereHostSession(container.host, stream_command_output=True, execution_context=context)
with session:
    target_changelog_root_file = get_changelog_root(session, deployed)
    perform_rollback_cmd('rollbackSQL', tag, target_changelog_root_file, container, session, context)
    perform_rollback_cmd('rollback', tag, target_changelog_root_file, container, session, context)
