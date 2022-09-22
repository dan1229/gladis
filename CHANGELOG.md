# CHANGELOG for {project_name_capitalcase}
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹
##### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


-------------------------------------------------------

## [Released]



-------------------------------------------------------

## [Unreleased]

-----

### ci cd
- python lint
- python test


### security
- add webhook secret
    - add to github as well


### api app
- app for api endpoints


### client app
- app for client ui

-----

## MVP Features
1. post to slack once ci passes for 
	1. if ci fails ping the author and mark as a draft again
2. notify people of comments
	1. if someone comments -> ping author
	2. if author requests rereview -> ping reviewers


-----

### slack integration
- send messages on slack


### auth
- oauth? - https://docs.github.com/en/developers/apps/building-oauth-apps


### webhooks
- https://adamj.eu/tech/2021/05/09/how-to-build-a-webhook-receiver-in-django/


-------------------------------------------------------
### TODO
----
### 0.0.1



### [0.0.1] - 2022-MM-DD
- Initial release!
- Basic project setup
    - env file support
    - django apps
    - basic models

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)
##### Copyright 2022 © Daniel Nazarian.