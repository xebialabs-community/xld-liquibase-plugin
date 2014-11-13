<#--

    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.

-->
#!/bin/sh
<#assign options = ""> 

<#if deployed.container.databaseUsername??>
  <#assign options = options + " --username=${deployed.container.databaseUsername} --password=${deployed.container.databasePassword}">
</#if>

<#if deployed.container.databaseJDBCURL??>
  <#assign options = options + " --url=${deployed.container.databaseJDBCURL}">
</#if>

<#if deployed.container.databaseJDBCDriver??>
  <#assign options = options + " --driver=${deployed.container.databaseJDBCDriver}">
</#if>

<#if deployed.container.liquibaseConfigurationPath??>
  <#assign options = options + " --defaultsFile=${deployed.container.liquibaseConfigurationPath}"> 
</#if>
<#if deployed.container.driverClasspath??>
  <#assign options = options + " --classpath=${deployed.container.driverClasspath}"> 
</#if>
<#if deployed.container.liquibaseExtraArguments??>
  <#assign options = options + " ${deployed.container.liquibaseExtraArguments}"> 
</#if>

cd "${step.uploadedArtifactPath}"

<#assign outputfile = "">
<#if deployed.container.generatedSqlPath??>
  GENERATED_SQL_DIR=${deployed.container.generatedSqlPath}/$(date +%Y_%m_%d_%H:%M)
  mkdir -p $GENERATED_SQL_DIR
  GENERATED_SQL_FILE=$GENERATED_SQL_DIR/update.sql
  echo "liquibase will generate update.sql to " $GENERATED_SQL_FILE
  <#assign outputfile = " 1>">
<#else>
  GENERATED_SQL_FILE=
  <#assign outputfile = " 1>&1"> 
</#if>

${deployed.container.javaCmd} -jar ${deployed.container.liquibaseJarPath} ${options} --changeLogFile="${deployed.changeLogFile}" updateSQL ${outputfile}$GENERATED_SQL_FILE
generateStatus=$?
if [ $generateStatus == 0 ]; then
  ${deployed.container.javaCmd} -jar ${deployed.container.liquibaseJarPath} ${options} --changeLogFile="${deployed.changeLogFile}" update
else
   exit $generateStatus
fi

exit $?
