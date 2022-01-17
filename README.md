# Liquibase plugin # 

This document describes the functionality provided by the Liquibase plugin.

See the **[XL Deploy Documentation](http://docs.xebialabs.com)** for background information on XL Deploy and deployment concepts.

## CI status

[![Build Status][xld-liquibase-plugin-travis-image] ][xld-liquibase-plugin-travis-url]
[![Codacy][xld-liquibase-plugin-codacy-image] ][xld-liquibase-plugin-codacy-url]
[![Code Climate][xld-liquibase-plugin-code-climate-image] ][xld-liquibase-plugin-code-climate-url]
[![License: MIT][xld-liquibase-plugin-license-image] ][xld-liquibase-plugin-license-url]
[![Github All Releases][xld-liquibase-plugin-downloads-image] ]()


[xld-liquibase-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-liquibase-plugin.svg?branch=master
[xld-liquibase-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-liquibase-plugin
[xld-liquibase-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/56e86b4f0faf4ca0a7ddfaf6c728d9c2
[xld-liquibase-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xld-liquibase-plugin
[xld-liquibase-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xld-liquibase-plugin/badges/gpa.svg
[xld-liquibase-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xld-liquibase-plugin
[xld-liquibase-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-liquibase-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-liquibase-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-liquibase-plugin/total.svg



## Overview

The Liquibase plugin provides a simple way to use Liquibase in XLD.

This plugin supports Liquibase 'roll back to' tag mode.

## Requirements

* **XL Deploy**: version 4.5.2+
* **Other XL Deploy Plugins**
	* [Overtherepy](https://github.com/xebialabs-community/overthere-pylib/releases/latest) version 0.3+

## Installation

You need to install Liquibase on a host accessible by the XLD server.

## Execution Logic

* CREATE Operation
	* Upload changelog folder
	* Tag Liquibase with an initial rollback tag.
	* Perform update of the changelog.
	* Tag Liquibase with the rollback tag specified on the deployed.
* DESTROY Operation
	* Upload changelog folder of previous deployed
	* Rollback to the initial rollback tag.
* MODIFY Operation
	* When the rollbackVersion of the new deployed is less than the previous deployed
		* Upload changelog folder of previous deployed
		* Rollback to new deployed rollbackVersion
	* Otherwise
		* Upload changelog folder of new deployed
		* Perform update of the changelog.
		* Tag Liquibase with the rollback tag specified on the deployed.

## Sample DARs

There are 2 versions of a sample dar available in the _test/resources/sample_dars_ directory that can be used to demonstrate plugin functionality.

## Configuration

### Container _liquibase.Runner_
A liquibase.Runner instance represents a liquibase installation. Below the configuration properties that needs to be set:

* *databaseUsername*: username for the database to connect to (when left out it will use the value in the properties file)
* *databasePassword*: password for the specified username (when left out it will use the value in the properties file)
* *databaseJDBCURL*: JDBC connection URL (when left out it will use the value in the properties file)
* *databaseJDBCDriver*: name of the JDBC driver to use (when left out it will use the value in the properties file)
* *liquibaseJarPath*: path to the main liquibase jar file, i.e. liquibase.jar
* *liquibaseConfigurationPath*: path to the liquibase configuration file, i.e liquibase.properties
* *javaCmd*: command that will be used to launch liquibase java process. Default is "java"
* *driverClasspath*: java classpath used to get database drivers

### Deployable _liquibase.Changelog_

*liquibase.Changelog* is a folder artifact that contains all the xml liquibase changelog 
files of the application package. 

__PLEASE NOTE__ this plugin requires that each changeset be marked with the logicalFilePath attribute set. This is so that Liquibase will not take the file name that contains the changeset into consideration when writing database log changes, e.g
<pre>
&lt;changeSet logicalFilePath="path-independent"  author="xxx" id="1403012036690-1"&gt;
</pre>
Properties :

* *changeLogFile* specifies the entry point xml changelog file for liquibase.
* *rollbackVersion* specifies the rollback version that will be used to apply a tag after successful changelog update.
* *rollbackVersionPrefix* specifies the prefix added to the tag. Default is 'v'. The tag is composed as follows: <rollbackVersionPrefix><rollbackVersion>, for example: "v1" or "abc-1".
