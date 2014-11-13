<#--

    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.

-->

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
  <#assign options = options + " ${deployed.liquibaseExtraArguments}"> 
</#if>
cd "${step.uploadedArtifactPath}"


<#assign outputfile = "">
<#if deployed.container.generatedSqlPath??>
  for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (set CURRENT_DATE=%%c-%%b-%%a)
  for /f "tokens=1-2 delims=/:" %%a in ("%TIME%") do (set CURRENT_TIME=%%a%%b)
  set GENERATED_SQL_DIR=${deployed.container.generatedSqlPath}\%CURRENT_DATE%_%CURRENT_TIME%
  if not exist %GENERATED_SQL_DIR% mkdir %GENERATED_SQL_DIR%
  set GENERATED_SQL_FILE=%GENERATED_SQL_DIR%\update.sql
  echo "liquibase will generate update.sql to " %GENERATED_SQL_FILE%
  <#assign outputfile = " 1>">
<#else>
  SET GENERATED_SQL_FILE=
  <#assign outputfile = " 1>&1"> 
</#if>

${deployed.container.javaCmd} -jar ${deployed.container.liquibaseJarPath} ${options} --changeLogFile="${deployed.changeLogFile}" updateSQL ${outputfile}%GENERATED_SQL_FILE%
if %errorlevel%==-1 goto :done
${deployed.container.javaCmd} -jar ${deployed.container.liquibaseJarPath} ${options} --changeLogFile="${deployed.changeLogFile}" update
:done
%errorlevel%
