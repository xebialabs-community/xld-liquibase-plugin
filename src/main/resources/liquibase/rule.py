#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

DESTROY_RESOURCES = 40
CREATE_RESOURCES = 60


def apply_changelog_steps(d, ctx):
    step = steps.jython(description="Apply changelog [%s] in liquibase [%s]" % (d.name, d.container.name),
                        order=CREATE_RESOURCES,
                        script='liquibase/apply_changelog.py',
                        jython_context={"container": d.container, "deployed": d})
    ctx.addStep(step)
    step = steps.jython(description="Create deployment rollback tag [%s%s] in liquibase [%s]" % (d.rollbackVersionPrefix, d.rollbackVersion, d.container.name),
                        order=CREATE_RESOURCES,
                        script='liquibase/apply_tag.py',
                        jython_context={"container": d.container, "tag": "%s%s" % (d.rollbackVersionPrefix, d.rollbackVersion)})
    ctx.addStep(step)


def handle_create(d, ctx):
    step = steps.jython(description="Create initial deployment rollback tag [%s] in liquibase [%s]" % (d.baseRollbackTag, d.container.name),
                        order=CREATE_RESOURCES,
                        script='liquibase/apply_tag.py',
                        jython_context={"container": d.container, "tag": d.baseRollbackTag})
    ctx.addStep(step)
    apply_changelog_steps(d, ctx)


def handle_destroy(d, ctx):
    step = steps.jython(description="Rollback to tag [%s] in liquibase [%s]" % (d.baseRollbackTag, d.container.name),
                        order=DESTROY_RESOURCES,
                        script='liquibase/apply_rollback.py',
                        jython_context={"container": d.container, "tag": d.baseRollbackTag, "deployed": d})
    ctx.addStep(step)

def handle_modify(pd, d, ctx):
    if d.rollbackVersion < pd.rollbackVersion:
        step = steps.jython(description="Rollback to tag [%s%s] in liquibase [%s]" % (d.rollbackVersionPrefix, d.rollbackVersion, d.container.name),
                            order=DESTROY_RESOURCES,
                            script='liquibase/apply_rollback.py',
                            jython_context={"container": d.container, "tag": "%s%s" % (d.rollbackVersionPrefix, d.rollbackVersion), "deployed": pd})
        ctx.addStep(step)
    else:
        apply_changelog_steps(d, ctx)


operation = str(delta.operation)

if operation == "CREATE":
    handle_create(deployed, context)
elif operation == "DESTROY":
    handle_destroy(previousDeployed, context)
elif operation == "MODIFY":
    handle_modify(previousDeployed, deployed, context)

