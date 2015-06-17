#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from overtherepy import StringUtils

def none_or_empty(s):
    return StringUtils.empty(s)

def build_cmd_line(container):
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
