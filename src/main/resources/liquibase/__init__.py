#
# Copyright 2023 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from overtherepy import StringUtils

def none_or_empty(s):
    return StringUtils.empty(s)

def build_cmd_line(container):
    if not none_or_empty(container.liquibaseLauncher):
        options = [container.liquibaseLauncher]
    else:
        options = [container.javaCmd, '-jar', container.liquibaseJarPath]
    if not none_or_empty(container.driverClasspath):
        options.append("--classpath=%s" % container.driverClasspath)
    if not none_or_empty(container.databaseUsername):
        options.append("--username=%s" % container.databaseUsername)
    if not none_or_empty(container.databasePassword):
        options.append("--password=%s" % container.databasePassword)
    if not none_or_empty(container.databaseJDBCURL):
        options.append("--url=%s" % container.databaseJDBCURL)
    if not none_or_empty(container.databaseJDBCDriver):
        options.append("--driver=%s" % container.databaseJDBCDriver)
    if not none_or_empty(container.liquibaseConfigurationPath):
        options.append("--defaultsFile=%s" % container.liquibaseConfigurationPath)
    if not none_or_empty(container.liquibaseExtraArguments):
        options.extend(container.liquibaseExtraArguments.split())

    return options

def print_cmd_line(cmd_line, ctx):
    print_args = []
    for item in cmd_line:
        if StringUtils.contains(item, "--password"):
            print_args.append("--password=******")
        else:
            print_args.append(item)
    ctx.logOutput("Executing command:")
    ctx.logOutput(StringUtils.concat(print_args, " "))

def get_changelog_root(session, deployed):
    target_changelog_dir = session.work_dir_file("changelog")
    target_changelog_dir.mkdirs()
    session.copy_to(deployed.file, target_changelog_dir)
    return target_changelog_dir.getFile(deployed.changeLogFile)
